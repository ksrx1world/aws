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



res = boto3.resource('ec2', region_name=config.region)
ec2 = boto3.client('ec2', region_name=config.region)
cloudfront = boto3.client('cloudwatch', region_name=config.region)
cost = boto3.client('ce', region_name=config.region)


def reini():
    response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
    instanceip=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')
    instanceid=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('InstanceId')
    instancetype=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('InstanceType')
    instanceloc=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('KeyName')
    volumeid=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('BlockDeviceMappings', [{}])[0].get('Ebs').get('VolumeId')
    statuscode=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('State', {}).get('Code')
    appy=[response, instanceip,instanceid,instancetype,instanceloc,volumeid,statuscode]
    return appy
volumesize=0
# def instancedetails():
#     response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
#     return render_template('index.html', ip=(response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')))

  


@app.route('/')
def cpucredit():
    ab=reini()
    instance = res.Instance(ab[2])
    volumes = instance.volumes.all()
    for volume in volumes:
        volumesize =+ volume.size
    # volumesize=40       
    volleft=30-volumesize
    return render_template('index.html',volumesize=volumesize,volleft=volleft, statuscode=ab[6])
    # return (int(credit.get('Datapoints', [{}])[0].get('Average')))
    

@app.route('/details/' , methods=['GET','POST'])
def instancedetails():
    ab=reini()
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
    if len(credit.get('Datapoints',[])) < 1 :
        d="start your server"
    else:        
        d=str(int(credit.get('Datapoints', [{}])[0].get('Average')))+" /169"        
    jso= {"CPU Credits" : d,"Instance Id" : ab[2],"Instance Ipv4" : ab[1], "Instance type" : ab[3] ,"Instance location" : ab[4]
        } 
    return jsonify(results = jso)

# @app.route('/d/')
# def instdetails():
#     ab=reini()
#     return ab[0]
    
@app.route('/stop/', methods=['GET','POST'])
def stop():
    try:
        ec2.stop_instances(InstanceIds=[config.InstanceIds])
        status="true"
        return status
    except Exception as e:
        print(e)
        status='false'
        return status
        

@app.route('/start/')
def start():
    try:
        ec2.start_instances(InstanceIds=[config.InstanceIds])
        status="true"
        return status
    except Exception as e:
        print(e)
        status='false'
        return status
       

if __name__ == "__main__" :
    app.run(debug=True)


#  response = cost.get_cost_and_usage_with_resources(
#         Granularity='DAILY',
#         Metrics=[
#         'AmortizedCost', 'UsageQuantity'
#         ],
#         TimePeriod={
#         'Start': '2020-06-06',
#         'End': '2020-06-07'
#         },
#         Filter = list(
#         Or = list(
#         list()
#         ),
#         And = list(
#         list()
#         ),
#         Not = list(),
#         Dimensions = list(
#         Key = "REGION",
#         Values = list(
#             config.region
#         )
#         ),
#         Tags = list(
#         Key = "alphabeta",
#         Values = list(
#             "alphavbeta"
#         )
#         ),
#         CostCategories = list(
#         Key = "string",
#         Values = list(
#             "string"
#         )
#         )
#         ),
#         GroupBy = list(
#         list(
#         Type = "DIMENSION"|"TAG"|"COST_CATEGORY",
#         Key = "string"
#         )
#         ),
#         NextPageToken = "s"
#             )





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
