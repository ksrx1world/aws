import boto3
import os
from dotenv import load_dotenv

load_dotenv()
class config:
    access_key = os.getenv('aws_access_key_id')
    secret_key = os.getenv('aws_secret_access_key')
    region = os.getenv('region')





# ec2 = boto3.client('ec2', region_name='ap-south-1')
# response = ec2.describe_instances()
# print(response)
print(config.access_key)
