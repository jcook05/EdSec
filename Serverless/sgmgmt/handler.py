import os
import os.path
import sys
import json
import boto3
import botocore

client = boto3.client('ec2')
ssh = []
tcp = []
udp = []

def getSg(group_id):
    response = client.describe_security_groups(
    Filters=[
        {
            'Name': 'group-id',
            'Values': [
                group_id,
            ]
        },
    ],
    DryRun=False,
    MaxResults=123
    )
    return response

def revokeIngressCidr(sg_id, ip_permissions):
    response = client.revoke_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=ip_permissions
    )
    return response    

def revokeIngress(sg_id):
    if os.environ['ssh'] == "true":
        print("ssh is true " + "removing " +  str(len(ssh)) + " ingress rules")
        if len(ssh) > 0:
            print(revokeIngressCidr(sg_id, ssh))
    if os.environ['tcp'] == "true":
        print("tcp is true " + "removing " +  str(len(tcp)) + " ingress rules")
        if len(tcp) > 0:
            print(revokeIngressCidr(sg_id, tcp))
    if os.environ['udp'] == "true":
        print("udp is true " + "removing " +  str(len(tcp)) + " ingress rules")
        if len(udp) > 0:
            print(revokeIngressCidr(sg_id, udp))
  

def authorizeIngressCidr(sg_id, ip_permissions):
    print("getSome")
    
def sg_security(event, context): 
    sg_id = event["detail"]["requestParameters"]["groupId"]
    group_name = getSg(event["detail"]["requestParameters"]["groupId"])["SecurityGroups"][0]["GroupName"]
    ip_permissions = getSg(event["detail"]["requestParameters"]["groupId"])["SecurityGroups"][0]["IpPermissions"]


## May want to dynamically generate these.   Future iteration may remove all authorizations excluding specified cidrs
    removeCidr = [{'CidrIp': '0.0.0.0/0'}]
    removeCidrIpv6 = [{'CidrIpv6': '::/0'}]
    
    ## Setup IP Permissions
    for x in ip_permissions:
       
        for v in x["IpRanges"]:
           
            if v["CidrIp"] == "0.0.0.0/0":
                x["IpRanges"] = removeCidr
                for v in x["Ipv6Ranges"]:
                    if["CidrIpv6"] == "::/0":
                        x["Ipv6Ranges"] = removeCidrIpv6
                print("Open Port Found")
               
                if x["FromPort"] == 22 and x["ToPort"] == 22:
                    ssh.append(x)
                elif x["FromPort"] != 22 and x["IpProtocol"] == "tcp":
                    tcp.append(x)
                elif x["IpProtocol"] == "udp":
                    udp.append(x)

    for x in ssh:
        print(x)
    for x in tcp:
        print(x)
    for x in udp:
        print(x)

    revokeIngress(sg_id)
    
  