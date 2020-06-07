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




ec2 = boto3.client('ec2', region_name=config.region)
cloudfront = boto3.client('cloudwatch', region_name=config.region)



# def instancedetails():
#     response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
#     return render_template('index.html', ip=(response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')))

    


@app.route('/')
def cpucredit():
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
    return render_template('index.html',score= int(credit.get('Datapoints', [{}])[0].get('Average')))
    # return (int(credit.get('Datapoints', [{}])[0].get('Average')))
    

@app.route('/details/' , methods=['GET','POST'])
def instancedetails():
    response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
    b=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('PublicIpAddress')
    c=response.get('Reservations', [{}])[0].get('Instances',[{}])[0].get('InstanceId')
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
    jso= { "Instance Id" : c, "Instance Ipv4" : b,"CPU Credits" : d
        } 
    return jsonify(results = jso)

@app.route('/d/')
def instdetails():
    response = ec2.describe_instances(InstanceIds=[config.InstanceIds])
    return response
    





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
