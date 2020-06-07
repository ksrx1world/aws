from flask import Flask , render_template,request, jsonify
import boto3
import os
from dotenv import load_dotenv
import json
from datetime import datetime,timedelta


app = Flask(__name__)


load_dotenv()


class config:
    access_key = os.getenv('aws_access_key_id')
    secret_key = os.getenv('aws_secret_access_key')
    region = os.getenv('region')
    InstanceIds= os.getenv('InstanceId')



res = boto3.resource('ec2',region_name=config.region)
ec2 = boto3.client('ec2', region_name=config.region)
cloudfront = boto3.client('cloudwatch', region_name=config.region)


response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
instanceip=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')
instanceid=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('InstanceId')
instancetype=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('InstanceType')
instanceloc=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('KeyName')
volumeid=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('BlockDeviceMappings', [{}])[0].get('Ebs').get('VolumeId')
volumesize=0
# def instancedetails():
#     response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
#     return render_template('index.html', ip=(response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')))

defvol = res.Volume(volumeid)
  


@app.route('/')
def cpucredit():
    instance = res.Instance(instanceid)
    volumes = instance.volumes.all()
    for volume in volumes:
        volumesize =+ volume.size
    # volumesize=40       
    volleft=30-volumesize
    return render_template('index.html',volumesize=volumesize,volleft=volleft)
    # return (int(credit.get('Datapoints', [{}])[0].get('Average')))
    

@app.route('/details/' , methods=['GET','POST'])
def instancedetails():
    credit = cloudfront.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUCreditBalance',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': config.InstanceIds
                },
            ],
            StartTime=datetime.utcnow()-timedelta(minutes = 15),
            EndTime=datetime.utcnow(),
            Period=900,
            Statistics=[
                'Average',
            ]
        )
    d=str(int(credit.get('Datapoints', [{}])[0].get('Average')))+" /144"        
    jso= {"CPU Credits" : d,"Instance Id" : instanceid,"Instance Ipv4" : instanceip, "Instance type" : instancetype ,"Instance location" : instanceloc
        } 
    return jsonify(results = jso)

@app.route('/d/')
def instdetails():
    response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
    return response
    
@app.route('/lsl')
def shows():
    instance = res.Instance(instanceid)
    volumes = instance.volumes.all()
    for volume in volumes:
        volumesize =+ volume.size

        return str(volumesize)



if __name__ == "__main__" :
    app.run(debug=True)







# print(cpucredit())
# print(instancedetails())



# starttime= datetime.datetime.strftime((datetime.datetime.utcnow() - datetime.timedelta(minutes = 15)), '%Y, %m, %d, %H, %M, %S')
# endtime=datetime.datetime.strftime((datetime.datetime.utcnow()), '%Y, %m, %d, %H, %M, %S')

# response = ec2.describe_instances(InstanceIds=[config.InstanceIds])

# res = ec2.describe_instance_credit_specifications(
#     DryRun=False,
#     InstanceIds=[
#         config.InstanceIds,
#     ])



# print(respons)


# for k, value in response.items():
#     print(k, value)
