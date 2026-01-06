import boto3
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine


# S3 configuration

bucket_name = "athena-query-result45"
file_key = "db406b2c-0b55-4ff7-afd4-92453bbbb032.csv"

s3 = boto3.client("s3")

obj = s3.get_object(Bucket=bucket_name, Key=file_key)
data = obj["Body"].read().decode("utf-8")

df = pd.read_csv(StringIO(data))
print(df.head())


# PostgreSQL configuration 


db_user = "postgres" #default user i dont have to create it 
db_password = "root123"
db_host = "localhost"
db_port = "5432"
db_name = "superset" #this is the actual database name

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


# Load to PostgreSQL
table_name = "s3_data"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",  # change to "replace" if needed
    index=False
)

print("Data loaded successfully")
