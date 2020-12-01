import os
import json
import uuid
import boto3
import traceback
from enum import Enum

# Load necessary AWS SDK clients
code_pipeline = boto3.client('codepipeline')
step_functions = boto3.client('stepfunctions')

STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']
CUSTOM_ACTION_PROVIDER_NAME = os.environ['CUSTOM_ACTION_PROVIDER_NAME']
CUSTOM_ACTION_PROVIDER_CATEGORY = os.environ['CUSTOM_ACTION_PROVIDER_CATEGORY']
CUSTOM_ACTION_PROVIDER_VERSION = os.environ['CUSTOM_ACTION_PROVIDER_VERSION']

print(f'Loading function. '
      f'Provider name: {CUSTOM_ACTION_PROVIDER_NAME}, '
      f'category: Deploy, '
      f'version: {CUSTOM_ACTION_PROVIDER_VERSION}')

class JobFlowStatus(Enum):
    Running = 1
    Succeeded = 2
    Failed = 3

def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    try:
        jobs = get_active_jobs()

        for job in jobs:
            job_id = job['id']
            continuation_token = get_job_attribute(job, 'continuationToken', '')
            print(f'processing job: {job_id} with continuationToken: {continuation_token}')

            try:
                process_job(job, job_id, continuation_token)
            except Exception:
                print(f'error during processing job: {job_id}')
                traceback.print_exc()
                mark_job_failed(job_id, continuation_token)

    except Exception:
        traceback.print_exc()
        raise


def process_job(job, job_id, continuation_token):
    # inform CodePipeline about that
    code_pipeline.acknowledge_job(jobId=job_id, nonce=job['nonce'])
    if not continuation_token:
        print('this is a new job, start the flow')
        start_new_job(job, job_id)
    else:
        # Get current job flow status
        job_flow_status = get_job_flow_status(continuation_token)
        print('current job status: ' + job_flow_status.name)

        if job_flow_status == JobFlowStatus.Running:
            mark_job_in_progress(job_id, continuation_token)
        elif job_flow_status == JobFlowStatus.Succeeded:
            mark_job_succeeded(job_id, continuation_token)
        elif job_flow_status == JobFlowStatus.Failed:
            mark_job_failed(job_id, continuation_token)


def get_active_jobs():
    # Call DescribeJobs
    response = code_pipeline.poll_for_jobs(
        actionTypeId={
            'owner': 'Custom',
            'category': 'Deploy',
            'provider': CUSTOM_ACTION_PROVIDER_NAME,
            'version': CUSTOM_ACTION_PROVIDER_VERSION
        },
        maxBatchSize=10
    )
    jobs = response.get('jobs', [])
    return jobs


def start_new_job(job, job_id):
    # start job execution flow
    execution_arn = start_job_flow(job_id, job)
    # report progress to have a proper link on the console
    # and "register" continuation token for subsequent jobs
    code_pipeline.put_job_success_result(
        jobId=job_id,
        continuationToken=execution_arn,
        executionDetails={
            'summary': 'Starting Deploy from AWS Batch...',
            'externalExecutionId': execution_arn,
            'percentComplete': 0
        }
    )


def mark_job_failed(job_id, continuation_token):
    print('mark job as failed')

    failure_details = {
        'type': 'JobFailed',
        'message': 'Batch Job Failed...'
    }

    if continuation_token:
        failure_details['externalExecutionId'] = continuation_token

    code_pipeline.put_job_failure_result(jobId=job_id, failureDetails=failure_details)


def mark_job_succeeded(job_id, continuation_token):
    print('completing the job')
    code_pipeline.put_job_success_result(
        jobId=job_id,
        executionDetails={
            'summary': 'Ending Deploy from AWS Batch...',
            'externalExecutionId': continuation_token,
            'percentComplete': 100
        }
    )


def mark_job_in_progress(job_id, continuation_token):
    print('completing the job, preserving continuationToken')
    code_pipeline.put_job_success_result(
        jobId=job_id,
        continuationToken=continuation_token
    )


def get_job_attribute(job, attribute, default):
    return job.get('data', {}).get(attribute, default)


def get_job_flow_status(flow_id) -> JobFlowStatus:
    response = step_functions.describe_execution(executionArn=flow_id)
    status = response.get('status', 'FAILED')

    if status == 'RUNNING':
        return JobFlowStatus.Running
    elif status == 'SUCCEEDED':
        return JobFlowStatus.Succeeded
    else:
        return JobFlowStatus.Failed


def start_job_flow(job_id, job):
    # job model reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_job_details
    input_artifacts = get_job_attribute(job, 'inputArtifacts', [])
    input_artifact = get_first_artifact(input_artifacts)

    configuration = get_job_attribute(job, 'actionConfiguration', {}).get('configuration', {})
    job_queue = configuration.get('JobQueue')
    job_definition = configuration.get('JobDefinition')
    job_name = configuration.get('JobName')
    command = configuration.get('Command')
    pipeline_context = get_job_attribute(job, 'pipelineContext', {})
    pipeline_execution_id = pipeline_context.get('pipelineExecutionId')
    pipeline_arn = pipeline_context.get('pipelineArn')
    pipeline_name = pipeline_context.get('pipelineName')

    sfn_input = {
        "params": {
            "pipeline": {
                "jobId": job_id,
                "executionId": pipeline_execution_id,
                "arn": pipeline_arn,
                "name": pipeline_name
            },
            "artifacts": {
                "input": {
                    "bucketName": input_artifact.get('bucketName'),
                    "objectKey": input_artifact.get('objectKey')
                }
            },
            "job": {
                "jobQueue": job_queue,
                "jobDefinition": job_definition,
                "jobName": job_name,
                "command": command
            }
        }
    }

    sfn_results = step_functions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=uuid.uuid4().hex,
        input=json.dumps(sfn_input)
    )

    return sfn_results.get('executionArn', '')


def get_first_artifact(input_artifacts):
    input_artifact = {}
    if input_artifacts:
        input_artifact = input_artifacts[0].get('location', {}).get('s3Location', {})
    return input_artifact