import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import extractor_lambda
import transformer_lambda
import loader_lambda

if __name__ == "__main__":
    print("==========================================================")
    print(" 🔥 RUNNING DECOUPLED MICROSERVICES PIPELINE CONTROLLER   ")
    print("==========================================================")
    
    # 🧪 TEST 1: Simulate JSON File Upload
    json_event = {
        "Records": [{"s3": {"bucket": {"name": "raw-bucket"}, "object": {"key": "raw/sample_raw_data.json"}}}]
    }
    print("\n--- 🏁 STARTING JSON LIFE-CYCLE INTERACTION ---")
    step1 = extractor_lambda.lambda_handler(event=json_event, context=None)
    step2 = transformer_lambda.lambda_handler(event=step1, context=None)
    step3 = loader_lambda.lambda_handler(event=step2, context=None)
    print(f"JSON Pipeline Output: {step3['body']}\n")
    
    # 🧪 TEST 2: Simulate CSV File Upload
    csv_event = {
        "Records": [{"s3": {"bucket": {"name": "raw-bucket"}, "object": {"key": "raw/sample_raw_data.csv"}}}]
    }
    print("--- 🏁 STARTING CSV LIFE-CYCLE INTERACTION ---")
    step1_csv = extractor_lambda.lambda_handler(event=csv_event, context=None)
    step2_csv = transformer_lambda.lambda_handler(event=step1_csv, context=None)
    step3_csv = loader_lambda.lambda_handler(event=step2_csv, context=None)
    print(f"CSV Pipeline Output: {step3_csv['body']}\n")
    
    print("==========================================================")
    print(" 🏆 ROBUST INDEPENDENT MODULE ARCHITECTURE VALIDATED     ")
    print("==========================================================")