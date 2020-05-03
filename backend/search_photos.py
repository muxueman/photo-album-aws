import json
import boto3
import sys
sys.path.insert(1, '/opt')
import requests


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def lambda_handler(event, context):
    print(event)
    # q = event["currentIntent"]["slots"]["key"]
    q = event["q"]
    print("q: ", q)
    
    # Disambiguate the query using Lex
    lex = boto3.client('lex-runtime')

    lex_response = lex.post_text(
        botName='Query_bot',
        botAlias='prod',
        userId="search-photos",
        inputText=q
    )
    print("lex response: ", lex_response)
    q = q.split(" ")
    
    if 'and' in q:
        idx = q.index('and')
        keywords = [q[idx-1], q[idx+1]]
    else:
        keywords = [q[-1]]
    print("keywords: ", keywords)
    print(len(keywords))
    
    results = []
    result_msg = ""
    num_result = 0
    
    if len(keywords) <= 2:  # We only support 2 keywords. If there are more than 2, input is not valid.
        
        for keyword in keywords:
            print("start finding the keyword ", keyword, " in ElasticSearch")
            host = "https://vpc-photos-i4acvnujp35ajdjpsl5ymfepba.us-east-1.es.amazonaws.com"
            search_url = host + "/photos/_search?q=" + keyword
            response = requests.get(search_url)
            response = response.json()
            print("response of hits for", keyword, ":", response["hits"])
    
            if not response["hits"]["hits"]: #can't find in ES
                result_msg += "Sorry, we can't find relevant photos related to " + keyword+". "
                
            else:
                num_result += response["hits"]["total"]["value"]
                for hit in response["hits"]["hits"]:
                    _source = hit["_source"]
                    objectKey = _source["objectKey"]
                    bucket = _source["bucket"]
                    labels = _source["labels"]
                    result = {"url": "https://s3.amazonaws.com/" + bucket + "/" + objectKey, "labels": labels}
                    results.append(result)
                
                
                result_msg += "We have found "+str(num_result)+" photos related with "+ keyword+". "
         # results is photos (meet the requirement)
        print(results)
        # directly send response to Lex
        # return close(event['sessionAttributes'], 'Fulfilled', {'contentType': 'PlainText', 'content': result_msg})
        urls = []
        for i in results:
            if i['url'] not in urls:
                urls.append(i['url'])
        return urls
                    
      
    else:  # Something wrong inside Lex
        return {
            'statusCode': 400,
            # 'body': lex_response["message"]
            'body': 'Too many keywords'
        }