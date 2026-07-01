# etl-s3-lambda-dynamodb
# ⚡ Serverless Serverless: Decoupled ETL Data Pipeline
> A Production-Grade Microservices Architecture built with Python & AWS Serverless Design Patterns.

![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=aws-lambda&logoColor=white)
![Amazon DynamoDB](https://img.shields.io/badge/Amazon_DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-brightgreen?style=for-the-badge)

---

## 🗺️ System Architecture & Data Flow

Below is the live execution flowchart of how data moves asynchronously through our decoupled layers without causing a single point of failure (Monolithic Bottleneck).

```mermaid
graph TD
    A[📥 S3 Bucket: Raw Upload Log] -->|Triggers Trigger| B(⚙️ Lambda 1: Extractor Layer)
    
    subgraph Layer 1: Extraction & Routing
        B -->|Detects Extension| B1{JSON or CSV?}
        B1 -->|Parse Array| B2[Raw JSON Payload]
        B1 -->|Parse Rows| B3[Raw CSV Payload]
    end

    B2 -->|Passes Payload| C(🚀 Lambda 2: Transformer Layer)
    B3 -->|Passes Payload| C

    subgraph Layer 2: Compute & Validation
        C -->|Data Quality Scan| C1{Has trip_id?}
        C1 -->|No| C2[⚠️ Drop & Log Corrupted Row]
        C1 -->|Yes| C3[Transform: UPPERCASE operator]
        C3 -->|Time Check| C4{Is Peak Hour?}
        C4 -->|7-9 AM / 4-6 PM| C5[Set flag: True]
        C4 -->|Off Peak| C6[Set flag: False]
    end

    C3 -->|Passes Structured Payload| D(💾 Lambda 3: Loader Layer)

    subgraph Layer 3: Storage Commit
        D -->|Safe Write Request| D1[(Storage Table: DynamoDB)]
    end

    style A fill:#ff9900,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#0073bb,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#0073bb,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#0073bb,stroke:#333,stroke-width:2px,color:#fff
    style D1 fill:#4053D6,stroke:#333,stroke-width:2px,color:#fff
📂 Project Directory StructurePlaintextetl-s3-lambda-dynamodb/
├── 📥 extractor_lambda.py       # Layer 1: Ingests raw storage data log metrics
├── ⚙️ transformer_lambda.py     # Layer 2: Runs analytical schemas & compliance rules
├── 💾 loader_lambda.py          # Layer 3: Dispatches batched commits into databases
├── 🎮 main_pipeline_runner.py   # Hybrid Central Test Harness & Layer Controller
└── 📝 README.md                 # System Manual & Architecture Blueprint
🛠️ Operational Specs & Transformation LawsMetric PillarOperation Execution RuleOutput Result StandardData Quality FilterCheck if explicit trip_id exists in the record.Drops missing rows automatically without breaking pipeline state.Schema NormalizationConvert string sequences under the operator column.vogo ➡️ VOGO, bounce ➡️ BOUNCE, yulu ➡️ YULUBI Flag ComputationVerify timestamp boundary cycles against rush hours.Assigns an is_peak_hour: True flag during 07-09 & 16-18 intervals.🚀 Execution Simulation (Local Diagnostics)We utilize a centralized controller to evaluate decoupled responses without wasting live cloud network computing time. Run this diagnostic test locally inside your terminal:PowerShellpython main_pipeline_runner.py
Flawless Live Logs Preview:JSON==========================================================
 🔥 RUNNING DECOUPLED MICROSERVICES PIPELINE CONTROLLER   
==========================================================

--- 🏁 STARTING JSON LIFE-CYCLE INTERACTION ---
📥 Lambda 1 (Extractor) Triggered for Key: raw/sample_raw_data.json
📂 Local Simulation Active: Bypassing AWS S3 Connection...
📋 [Extractor] Parsing: JSON format detected
➡️ Extractor Task Completed successfully.

⚙️ Lambda 2 (Transformer) Active... Normalizing structural schemas
  ⚠️ Validation Failure: Skipping row missing mandatory 'trip_id'
✅ Transformer Task Completed. Valid: 2, Rejected: 1

💾 Lambda 3 (Loader) Active... Preparing simulation database commit
  🔬 [DynamoDB Mock Save] Key: 'T101' | Op: VOGO | PeakHour: True
  🔬 [DynamoDB Mock Save] Key: 'T102' | Op: BOUNCE | PeakHour: False
🚀 Loader Task Completed. Target states synced safely. Total items inserted: 2

JSON Pipeline Output: Successfully loaded 2 records.
==========================================================
