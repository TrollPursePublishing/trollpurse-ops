import boto3

batch_client = boto3.client('batch')

def lambda_handler(event, context):
  describe_response = batch_client.describe_jobs(
    jobs=[ event.get('jobId', '')]
  )
  
  return describe_response.get('jobs', [{}])[0].get('status', '')
