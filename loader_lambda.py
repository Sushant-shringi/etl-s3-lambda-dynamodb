import json

def lambda_handler(event, context=None):
    print("💾 Lambda 3 (Loader) Active... Preparing simulation database commit")
    clean_records = event.get('data', [])
    inserted_count = 0
    
    if not clean_records:
        print("  ℹ️ No valid records found to load.")
        return {"statusCode": 200, "body": "No data to load"}
        
    for record in clean_records:
       
        print(f"  🔬 [DynamoDB Mock Save] Key: '{record['record_id']}' | Op: {record['operator']} | PeakHour: {record['is_peak_hour']}")
        inserted_count += 1
            
    print(f"🚀 Loader Task Completed. Target states synced safely. Total items inserted: {inserted_count}")
    return {
        "statusCode": 200,
        "body": f"Successfully loaded {inserted_count} records."
    }
