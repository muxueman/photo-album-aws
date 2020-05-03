import json
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    print("啊！！！！！")
    print(event)
    if event['httpMethod'] == 'POST' : 
        print(event['body'])
        data = json.loads(event['body'])
        name = data['name']
        image = data['file']
        image = image[image.find(",")+1:]
        dec = base64.b64decode(image + "===")
        print(dec)
        # s3.put_object(Bucket='photo-album-hw3', Key=name, Body=dec)
        
        return {
            'statusCode': 200,
            'body': json.dumps('success')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }