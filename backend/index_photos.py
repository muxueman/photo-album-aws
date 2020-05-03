import json
import boto3
import logging
import sys 
sys.path.insert(1, '/opt')
import requests

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('got event{}'.format(event))
    
    image_name = event["Records"][0]["s3"]["object"]["key"]
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    upload_time = event["Records"][0]["eventTime"]

    
    print('begin detection')
    
    response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':image_name}}, MaxLabels=10, MinConfidence=70)
    print("recognition results are")
    logger.info(response)
  
    putlabel = []
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        putlabel.append(label['Name'])
    
    print('the labels are: ', putlabel)
    
    index = {"objectKey": image_name, "bucket": bucket_name,"createdTimestamp": upload_time, "labels": putlabel}
    print('the index is:', index)
    logger.info(index)
    
    # upload to Elastic Search
    host = "https://vpc-photos-i4acvnujp35ajdjpsl5ymfepba.us-east-1.es.amazonaws.com"
    post_url = host + "/photos/_doc"
    response = requests.post(post_url, json=index)
    response = response.text
    
    
    print('The response from ES is: ',response)
    return {
        'statusCode': 200,
        'body': "The images have been uploaded"
    }
     