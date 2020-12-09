import boto3

batch_client = boto3.client('batch')

def handler(event, context):
  if event.get('jobState', '') != 'SUCCEEDED':
    batch_client.terminate_job(
      jobId=[event.get('status').get('jobId', '')],
      reason='Cancelled or failed'
    )