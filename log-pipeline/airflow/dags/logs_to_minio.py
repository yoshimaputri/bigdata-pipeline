import datetime
from pyspark.sql import SparkSession
import pytz

tz = pytz.timezone('Asia/Seoul')
now = datetime.datetime.now(tz)
day_str = now.strftime("%Y%m%d")
hour_str = now.strftime("%H")
print("Schedule: ", day_str, ' hour=', hour_str)

spark = SparkSession.builder \
    .appName("NginxLogToMinIO") \
    .config("spark.jars.packages", ",".join(["org.apache.hadoop:hadoop-aws:3.3.5", "org.apache.hadoop:hadoop-common:3.3.5"])) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio_admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minio_password") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

print("Read logs from Nginx...")
df = spark.read.option("multiLine", "true").json("/var/log/nginx")
df.show()

print("Parse to parquet and put into Minio...")
minio_path = f"s3a://parquet/day={day_str}/hour={hour_str}"
df.write.mode("overwrite").parquet(minio_path)

spark.stop()

print("SUCCESSFULLY WRITE PARQUET TO MINIO!")

