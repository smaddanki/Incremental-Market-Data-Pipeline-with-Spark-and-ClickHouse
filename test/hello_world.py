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
    