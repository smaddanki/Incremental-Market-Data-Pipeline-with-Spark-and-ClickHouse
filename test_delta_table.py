from pyspark.sql import SparkSession
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Creating Spark session with Delta support...")
        spark = SparkSession.builder \
            .appName("DeltaTest") \
            .master("spark://localhost:7077") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "2g") \
            .getOrCreate()

        # Create a sample DataFrame
        data = [("John", 30), ("Alice", 25)]
        df = spark.createDataFrame(data, ["name", "age"])

        # Write as Delta table using the shared location
        df.write.format("delta").mode("overwrite").save("file:///spark-data/delta-test")

        # Read from Delta table
        df_read = spark.read.format("delta").load("file:///spark-data/delta-test")
        df_read.show()

        spark.stop()

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()