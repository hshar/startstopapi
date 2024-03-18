import boto3
import json

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    event1=json.loads(json.dumps(event))
    print(event1)
    # Extract instance ID from event
    instance_id = event1['queryStringParameters']['instance_id']
    
    # Extract action from event (start or stop)
    action = event1['queryStringParameters']['action']
    
    # Perform action based on trigger
    if action == 'start':
        # Start the EC2 instance
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Started EC2 instance with ID: {instance_id}")
        message = {'response': "Started wait for 1 min before describing"}
    
    # Constructing the response
    elif action == 'describe':
        hello = ec2.describe_instances(InstanceIds=[instance_id])
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        public_ip = hello['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(public_ip)
        message =  {'public_ip': public_ip}
    elif action == 'stop':
        # Stop the EC2 instance
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopped EC2 instance with ID: {instance_id}")
        message = {'response': "Instance Stopped!"}
    else:
        print("Invalid action provided. Supported actions are 'start' and 'stop'.")
        message = {'response': 'Give Correct Action Pls!'}
        
    response = {
        'statusCode': 200,
        'body': json.dumps(message),
        'headers': {'Content-Type': 'application/json'}
    }
    
    return response

# Example event:
# event = {
#     'instance_id': 'your_instance_id_here',
#     'action': 'start'  # or 'stop'
# }
