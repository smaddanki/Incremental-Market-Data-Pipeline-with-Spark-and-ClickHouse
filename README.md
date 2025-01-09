# Incremental-Market-Data-Pipeline-with-Spark-and-ClickHouse

## Spark and Worker 

```yaml
version: '3.7'

networks:
  spark-network:

services:
  spark:
    image: bitnami/spark:latest
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    ports:
      - '8080:8080'
      - '7077:7077'
    extra_hosts:
      - "host.docker.internal:192.168.40.245"


  spark-worker:
    image: bitnami/spark:latest
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark:7077
      - SPARK_WORKER_MEMORY=4G
      - SPARK_WORKER_CORES=1
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
      - SPARK_USER=spark
    extra_hosts:
      - "host.docker.internal:192.168.40.245"
    depends_on:
      - spark
```

```bash
docker-compose up - d
```

## Test Job
```python
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Creating Spark session...")
        conf = SparkConf()
        
        SPARK_DRIVER_HOST = 'localhost'
        
        spark = SparkSession.builder \
            .appName("HelloSpark") \
            .master("spark://localhost:7077") \
            .getOrCreate()

        logger.info("Successfully created Spark session")

        logger.info("Creating RDD...")
        numbers_rdd = spark.sparkContext.parallelize(range(1, 1001))
        
        logger.info("Counting elements...")
        count = numbers_rdd.count()
        
        logger.info(f"Count of numbers from 1 to 1000 is: {count}")
        spark.stop()

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
```

## Add delta table using pyspark
```bash
pyspark --packages io.delta:delta-spark_2.12:3.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
```

