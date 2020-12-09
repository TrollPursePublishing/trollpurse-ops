import boto3
import json

batch_client = boto3.client('batch')

def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    job_configuration = event.get('job', {})
    artifact_configuration = event.get('artifact', {})
    
    job_name = job_configuration.get('name', '')
    job_definition = job_configuration.get('definition', '')
    job_queue = job_configuration.get('queue', '')
    job_parameters = job_configuration.get('parameters', '')
    
    job_parameters['InputBucketName'] = artifact_configuration.get('bucketName', '')
    job_parameters['InputObjectKey'] = artifact_configuration.get('objectKey', '')
    
    submit_response = batch_client.submit_job(
      jobName = job_name,
      jobQueue = job_queue,
      jobDefinition = job_definition,
      parameters=job_parameters
    )
    
    describe_response = batch_client.describe_jobs(
      jobs=[ submit_response.get('jobId', '')]
    )
    
    return {
        'jobArn': submit_response.get('jobArn', ''),
        'jobName': submit_response.get('jobName', ''),
        'jobId': submit_response.get('jobId', ''),
        'jobState': describe_response.get('jobs', [{}])[0].get('status', '')
    }
