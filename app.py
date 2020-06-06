import boto3

region = 'ap-south-1'



ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()
print(response)