import json
import boto3  # <--- Boto3 import karna hoga

def lambda_handler(event, context=None):
    try:
        print("📥 Lambda 2 (Transformer) Triggered...")
        
        # 1. Extractor se aaya hua data nikalna
        input_data = event.get('data', [])
        file_processed = event.get('file_processed', 'unknown')
        
        # ... Aapka purana transformation ka logic (clean_records wala) yahan chalega ...
        # maan lete hain aapka final data 'cleaned_data' variable mein hai:
        cleaned_data = clean_records(input_data) 
        
        print("➡️ Transformer Task Completed successfully.")
        
        # 2. Final Payload taiyar karo
        output_payload = {
            "status": "Transformed",
            "file_processed": file_processed,
            "data": cleaned_data
        }
        
        # 🎯 AWS Environment Check aur Loader ko Trigger karna
        if context and hasattr(context, 'function_name'):
            print("🚀 AWS Environment Detected! Triggering loader-service...")
            lambda_client = boto3.client('lambda', region_name='us-east-1') # Apni region check kar lena bhai
            
            # Ye line AWS par Loader Lambda ko trigger karegi
            lambda_client.invoke(
                FunctionName='loader-service',
                InvocationType='Event', # Asynchronous call
                Payload=json.dumps(output_payload)
            )
            print("✅ Successfully triggered loader-service asynchronously.")
            
        return output_payload
        
    except Exception as e:
        print(f"❌ Transformer Error: {str(e)}")
        return {"status": "Error", "file_processed": "unknown", "data": []}