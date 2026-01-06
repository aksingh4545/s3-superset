# 📊 Automated Analytics Pipeline: Amazon S3 to Apache Superset

This repository contains a **production-style data analytics pipeline** built on AWS. The solution demonstrates how raw data stored in Amazon S3 can be transformed, queried, and visualized using a combination of **serverless AWS services** and **open-source BI tooling**.

The focus of this project is not just functionality, but architectural clarity, automation, and real-world data engineering practices.

---

## 🎯 Objective

Raw datasets stored in object storage are rarely ready for direct analysis. They often contain:

* Inconsistent schemas
* Missing or null values
* Duplicate records
* No metadata for querying

This project addresses those issues by designing a pipeline that:

* Transforms raw data into analytics-ready format
* Automates ETL execution
* Enables SQL-based analysis
* Persists curated data for BI tools
* Serves interactive dashboards

All without provisioning or managing servers.

---

## 🧱 System Architecture

```
S3 (Raw Data)
   ↓
AWS Glue ETL Job
   ↓
S3 (Curated Data)
   ↓
AWS Glue Crawler
   ↓
Glue Data Catalog
   ↓
Amazon Athena
   ↓
Athena Results (S3)
   ↓
PostgreSQL
   ↓
Apache Superset
```

🔁 ETL execution is orchestrated automatically using AWS Lambda.

---

## 🛠️ Tools and Services

| Category       | Technology            |
| -------------- | --------------------- |
| Object Storage | Amazon S3             |
| ETL Processing | AWS Glue              |
| Metadata Store | AWS Glue Data Catalog |
| Query Engine   | Amazon Athena         |
| Automation     | AWS Lambda            |
| Analytics DB   | PostgreSQL            |
| Visualization  | Apache Superset       |
| Language       | Python, SQL           |

---

## 📁 Storage Layout

| Bucket                  | Purpose              |
| ----------------------- | -------------------- |
| `source-etl-file-ak45`  | Raw input datasets   |
| `target-etl-file-ak45`  | Transformed datasets |
| `athena-query-result45` | Athena query outputs |

---

## Step 1: Raw Data Ingestion (Amazon S3)

Source datasets are uploaded to the raw data bucket:

```
source-etl-file-ak45
```

These files typically contain uncleaned data and are not suitable for direct analytics.

📸 *Raw data stored in S3*

---

## Step 2: Data Transformation with AWS Glue

An AWS Glue ETL job performs the core data processing tasks.

### Responsibilities of the Glue Job

* Clean invalid or null records
* Normalize column structure
* Remove duplicates
* Write structured output to target S3

### Why Glue

* Serverless Spark environment
* Automatic scaling
* Native integration with AWS analytics stack

📸 *Glue ETL job configuration*

---

## Step 3: Curated Data Storage

Transformed datasets are written to:

```
target-etl-file-ak45
```

This bucket contains data that is consistent, structured, and ready for querying.

---

## Step 4: Metadata Discovery with Glue Crawler

The Glue Crawler scans the transformed data and:

* Detects schema
* Creates tables automatically
* Registers metadata in the Glue Data Catalog

This step is critical because Athena relies entirely on catalog metadata.

---

## Step 5: Glue Data Catalog

The Data Catalog acts as the **metadata backbone** for the pipeline.

It stores:

* Table definitions
* Column data types
* S3 locations

This metadata is shared across Glue, Athena, and BI tools.

---

## Step 6: SQL Analytics using Amazon Athena

Athena enables interactive SQL queries directly on S3-based datasets.

Example query:

```sql
SELECT gender, AVG(final_percentage)
FROM student_performance
GROUP BY gender;
```

📸 *Athena query execution and results*

---

## Step 7: Athena Query Outputs

Athena query results are written to:

```
athena-query-result45
```

Each query generates:

* CSV output files
* Metadata files for execution context

These outputs are used for downstream ingestion.

---

## Step 8: Persisting Analytics Data in PostgreSQL

PostgreSQL is used as the analytics database for Superset.

### Rationale

* Faster dashboard performance
* Persistent storage
* Native Superset compatibility

### Python Loader Example

```python
import boto3
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine

s3 = boto3.client("s3")
obj = s3.get_object(
    Bucket="athena-query-result45",
    Key="query_output.csv"
)

data = obj["Body"].read().decode("utf-8")
df = pd.read_csv(StringIO(data))

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/superset"
)

df.to_sql("analytics_data", engine, if_exists="replace", index=False)
```

---

## Step 9: Visualization with Apache Superset

Apache Superset connects to PostgreSQL and provides rich interactive dashboards.

Dashboards include:

* Performance distributions
* Trend analysis
* Category-based aggregations

📸 *Superset dashboards*

---

## Step 10: Automation with AWS Lambda

AWS Lambda is used to trigger the Glue ETL job automatically.

```python
import boto3

glue = boto3.client("glue")

def lambda_handler(event, context):
    glue.start_job_run(JobName="jobak-45")
    return "ETL job triggered"
```

This removes the need for manual job execution.

---

## 🔁 End-to-End Flow Summary

1. Raw data uploaded to S3
2. Lambda triggers Glue job
3. Glue transforms data
4. Clean data stored in S3
5. Crawler updates metadata
6. Athena runs SQL queries
7. Results stored in S3
8. Data loaded into PostgreSQL
9. Superset serves dashboards

---

## ⚠️ Key Engineering Challenges Addressed

* Cross-service IAM permissions
* Schema evolution handling
* Athena result file management
* Database connectivity
* BI metadata synchronization

---

## 🧠 Design Considerations

* Fully serverless execution
* Cost-efficient analytics
* Scalable and modular design
* Separation of compute, storage, and visualization

---

## 🚀 Possible Extensions

* EventBridge-based scheduling
* Incremental and partitioned ETL
* Data quality checks
* Role-based access in Superset
* CI/CD for analytics pipelines

---

## ✅ Conclusion

This project reflects how modern analytics platforms are designed in real environments. It combines AWS-native services with open-source tools to deliver a scalable, automated, and maintainable analytics pipeline.

Understanding this architecture provides a strong foundation in **cloud data engineering and analytics systems**.
