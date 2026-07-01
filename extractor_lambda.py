import json
import csv
import urllib.parse

def parse_json_file(file_content):
    print("📋 [Extractor] Parsing: JSON format detected")
    raw_data = json.loads(file_content)
    return raw_data if isinstance(raw_data, list) else [raw_data]

def parse_csv_file(file_content):
    print("📋 [Extractor] Parsing: CSV format detected")
    records = []
    lines = file_content.splitlines()
    reader = csv.DictReader(lines)
    for row in reader:
        if 'duration_minutes' in row and row['duration_minutes']:
            row['duration_minutes'] = int(row['duration_minutes'])
        records.append(dict(row))
    return records

def lambda_handler(event, context=None):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        file_extension = key.split('.')[-1].lower()
        
        print(f"📥 Lambda 1 (Extractor) Triggered for Key: {key}")
        print("📂 Local Simulation Active: Bypassing AWS S3 Connection...")
        
        # Pure Local Mock Stream to completely isolate AWS Client initialization
        if file_extension == 'json':
            file_content = json.dumps([
                {"trip_id": "T101", "city": "Pune", "operator": "vogo", "trip_start_datetime": "2026-06-30 08:30:00", "duration_minutes": 15},
                {"trip_id": "T102", "city": "Pune", "operator": "bounce", "trip_start_datetime": "2026-06-30 14:15:00", "duration_minutes": 22},
                {"city": "Corrupted_Row_Missing_ID"}
            ])
            raw_records = parse_json_file(file_content)
            
        elif file_extension == 'csv':
            file_content = "trip_id,city,operator,trip_start_datetime,duration_minutes\nT201,Pune,yulu,2026-06-30 17:45:00,10\nT202,Mumbai,bounce,2026-06-30 22:00:00,35"
            raw_records = parse_csv_file(file_content)
            
        else:
            return {"statusCode": 400, "body": "Unsupported format"}
            
        print("➡️ Extractor Task Completed successfully.")
        return {"status": "Extracted", "file_processed": key, "data": raw_records}
        
    except Exception as e:
        print(f"❌ Extractor Error: {str(e)}")
        return {"status": "Error", "file_processed": "unknown", "data": []}