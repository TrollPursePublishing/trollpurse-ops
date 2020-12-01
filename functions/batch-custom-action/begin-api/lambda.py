import os
import json
import uuid
import boto3
import traceback
from enum import Enum

# Environment Variables
JOB_NAME = os.environ["JOB_NAME"]
JOB_QUEUE = os.environ["JOB_QUEUE"]
JOB_DEFINITION = os.environ["JOB_DEFINITION"]

def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    # Handle only custom events
    if not should_process_event(event):
        return

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