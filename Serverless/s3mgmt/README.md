
# Event Driven S3 Security

This Lambda Function, implemented via the Serverless Framework, is triggered from a CloudWatch Event and will update the public_access_block of a newly created bucket.  
Public Access for ACL's will be blocked while Public Access for Bucket Policies will still be allowed.   While you can block all Public Access at the account level or at S3 bucket creation, it is sometimes beneficial to set access via policies.   This is particularly beneficial if you are hosting S3 Static sites, as static sites require access.   An example could be when hosting a dev/test static site you require access only to a specific CIDR Block.   Add this access via bucket policy to mitigate security gaps. 

## Prerequisites and Infrastructure Setup

The below assets are required for this solution.   A terraform project has been provided that will create these assets.  

Setup a Cloud Trail

    Enable Logging
    Management Events -  at a minimum Write Only


Configure an S3 Role for Lambda with the below policy: 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": [
                "*"
            ],
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutBucketPublicAccessBlock",
                "s3:PutBucketPolicy",
                "s3:DeleteBucketPolicy"
            ],
            "Resource": "*"
        }
    ]
}


## Configure

This project has been configured to use the following versions:

Python: 3.6
boto3: 1.9.156
botocore: 1.12.156

As of 8/13/2019 the default version of boto3 and botocore does not contain the S3 client put_public_access_block attribute.
This function uses put_public_access_block to lock down public ACL access and therefore requires a newer version of boto3.
Hopefully AWS will update this soon, until then, we can package our own boto3 and botocore for use. 

Update the resources/customVars.yml with the Lambda S3 Role Arn that you have configured.  

### Install boto3 and botocore
  -  As this project uses Python3, ensure to install via python3-pip
     pip3 boto3

  - Add to the botoVersion folder by running the below command in /botoVersion
    - pip3 install -r requirements.txt -t .


## Test Locally
Update the test/testevent.json to reflect your target account
serverless invoke local --function secure_bucket --path test/testevent.json

## Test via Lambda
Add the testevent.json into a test event on Lambda.  