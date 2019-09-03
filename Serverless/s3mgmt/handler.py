import os
import os.path
import sys
 
## Select a specific version of Boto3
envLambdaTaskRoot = os.environ["LAMBDA_TASK_ROOT"]
print("LAMBDA_TASK_ROOT env var:"+os.environ["LAMBDA_TASK_ROOT"])
print("sys.path:"+str(sys.path))
sys.path.insert(0,envLambdaTaskRoot+"/botoVersion")
print("sys.path:"+str(sys.path))

import json
import boto3
import botocore

client = boto3.client('s3')

def putAccessBlock(bucket_name):
    response = client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
   )
    return response 

def new_bucket(event, context):
    print("boto3 version:"+boto3.__version__)
    print("botocore version:"+botocore.__version__)
    #print(event)
    if (event['detail']['eventName'] == "CreateBucket"): 
        ## Get the Bucket Name from the event
        bucketName = event['detail']['requestParameters']['bucketName']
        print("Securing ", bucketName)
        response = putAccessBlock(bucketName)    
    print(response)

   