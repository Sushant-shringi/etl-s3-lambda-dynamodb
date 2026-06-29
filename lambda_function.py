import json
import urllib.parse
from datetime import datetime
import boto3

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("clean_records")

def lambda_handler(event, context):
    total_input = 0
    inserted_records = 0
    rejected_records = 0
    
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        raw_data = json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(json.dumps({"status": "Failed", "error": str(e)}))
        return {"statusCode": 500, "body": "Extraction Failure"}

    records = raw_data if isinstance(raw_data, list) else [raw_data]
    total_input = len(records)
    
    for item in records:
        try:
            if 'trip_id' not in item:
                rejected_records += 1
                continue
            
            clean_operator = str(item.get('operator', 'UNKNOWN')).upper()
            raw_time_str = item.get('trip_start_datetime', '')
            
            try:
                parsed_dt = datetime.strptime(raw_time_str, "%Y-%m-%d %H:%M:%S")
                iso_time = parsed_dt.isoformat() + "Z"
                hour = parsed_dt.hour
            except Exception:
                iso_time = datetime.utcnow().isoformat() + "Z"
                hour = datetime.utcnow().hour
            
            is_peak_hour = (7 <= hour <= 9) or (16 <= hour <= 18)
            
            clean_item = {
                'record_id': str(item['trip_id']), 
                'city': str(item.get('city', 'Unknown')),
                'operator': clean_operator,
                'trip_start_time': iso_time,
                'duration_minutes': int(item.get('duration_minutes', 0)),
                'is_peak_hour': is_peak_hour,
                'processed_at': datetime.utcnow().isoformat() + "Z"
            }
            
            table.put_item(Item=clean_item)
            inserted_records += 1
            
        except Exception:
            rejected_records += 1

    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pipeline_status": "Success",
        "metrics": {
            "total_input_records": total_input,
            "inserted_records": inserted_records,
            "rejected_records": rejected_records
        }
    }
    print(json.dumps(summary))
    return {"statusCode": 200, "body": json.dumps(summary)}