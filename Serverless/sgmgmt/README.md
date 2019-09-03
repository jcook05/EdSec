
# Event Driven Security Group Security

This Lambda Function, implemented via the Serverless Framework, is triggered from a CloudWatch Event and will ensure that Security Groups do not contain SSH, TCP, or UDP ports that are open to the public.   


## Configuration

SSH, TCP and UDP port remediation is configured via the Environment Variables located within the serverless.yml file.   To activate auto-remediation of these ports simply set the environment variable for the desired protocol to true.  Alternatively, set to false to deactivate.  

## Prerequisites

   CloudWatch Event:  A Cloud Watch Event with the AuthorizeSecurityGroupIngress event pattern to trigger the Lambda Function. 

       Event Pattern:  

            {
              "source": [
                "aws.ec2"
              ],
              "detail-type": [
                "AWS API Call via CloudTrail"
              ],
              "detail": {
                "eventSource": [
                  "ec2.amazonaws.com"
                ],
                "eventName": [
                  "AuthorizeSecurityGroupIngress"
                ]
              }
            }

  Lambda Role:    A role for the Lambda Function that gives appropriate Cloud Watch Logs and Ec2 Security Group privileges.  An example has been provided as LambdaPolicy.json
  
## Test Locally
serverless invoke local --function secure_sg --path test/testevent.json

## Test via Lambda
Add the testevent.json into a test event on Lambda.  