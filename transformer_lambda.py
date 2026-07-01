import json
from datetime import datetime, UTC

def lambda_handler(event, context=None):
    print("⚙️ Lambda 2 (Transformer) Active... Normalizing structural schemas")
    raw_records = event.get('data', [])
    processed_records = []
    rejected_count = 0
    
    for item in raw_records:
        # Data Quality Filter
        if 'trip_id' not in item or not item['trip_id']:
            rejected_count += 1
            print("  ⚠️ Validation Failure: Skipping row missing mandatory 'trip_id'")
            continue
            
        clean_operator = str(item.get('operator', 'UNKNOWN')).upper()
        raw_time_str = item.get('trip_start_datetime', '')
        
        try:
            parsed_dt = datetime.strptime(raw_time_str, "%Y-%m-%d %H:%M:%S")
            iso_time = parsed_dt.isoformat() + "Z"
            hour = parsed_dt.hour
        except Exception:
            iso_time = datetime.now(UTC).isoformat().replace("+00:00", "Z")
            hour = datetime.now(UTC).hour
            
        # Business Logic Filter
        is_peak_hour = (7 <= hour <= 9) or (16 <= hour <= 18)
        
        clean_item = {
            'record_id': str(item['trip_id']), 
            'city': str(item.get('city', 'Unknown')),
            'operator': clean_operator,
            'trip_start_time': iso_time,
            'duration_minutes': int(item.get('duration_minutes', 0)) if item.get('duration_minutes') else 0,
            'is_peak_hour': is_peak_hour,
            'processed_at': datetime.now(UTC).isoformat().replace("+00:00", "Z")
        }
        processed_records.append(clean_item)
        
    print(f"✅ Transformer Task Completed. Valid: {len(processed_records)}, Rejected: {rejected_count}")
    return {"status": "Transformed", "data": processed_records}