# Import necessary libraries
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType
import urllib

# Event Hubs connection string (without EntityPath)
event_hubs_connection_string = 'Endpoint=sb://XXX.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XXX'

# Encode the connection string
eh_connection_string = urllib.parse.quote(event_hubs_connection_string, safe="")

# Event Hubs configuration
eh_conf = {
    'eventhubs.connectionString': "XXX",
    'eventhubs.consumerGroup': '$Default'
}

# Read from Event Hubs
df = (spark.readStream
      .format("eventhubs")
      .options(**eh_conf)
      .load())

# Define the schema of the incoming data
schema = StructType([
    StructField("charger_id", StringType(), True),
    StructField("start_time", StringType(), True),
    StructField("end_time", StringType(), True),
    StructField("duration_minutes", IntegerType(), True),
    StructField("energy_consumed", FloatType(), True),
    StructField("phone_number", StringType(), True),
    StructField("email", StringType(), True)
])

# Parse the JSON data and extract fields
parsed_df = (df.select(from_json(col("body").cast("string"), schema).alias("data"))
             .select("data.*"))

# Convert time fields to TimestampType
parsed_df = (parsed_df.withColumn("start_time", col("start_time").cast(TimestampType()))
             .withColumn("end_time", col("end_time").cast(TimestampType())))

# Define billing rate
billing_rate = 0.20  # $0.20 per kWh

# Calculate billing amount
billing_df = parsed_df.withColumn("billing_amount", col("energy_consumed") * billing_rate)

# Select relevant columns and rename them to match PostgreSQL table
result_df = billing_df.select(
    col("charger_id").alias("ChargerID"),
    col("phone_number").alias("PhoneNumber"),
    col("email").alias("Email"),
    col("start_time").alias("StartTime"),
    col("end_time").alias("EndTime"),
    col("duration_minutes").alias("DurationMinutes"),
    col("energy_consumed").alias("EnergyConsumed"),
    col("billing_amount").alias("BillingAmount")
)

# JDBC connection properties
jdbc_url = "jdbc:postgresql://XXX.postgres.database.azure.com:5432/evbilling?sslmode=require"
connection_properties = {
    "user": "XXX",
    "password": "XXX",
    "driver": "org.postgresql.Driver"
}

# Function to write each micro-batch to Azure Database for PostgreSQL
def write_to_postgres(batch_df, batch_id):
    batch_df.write.jdbc(url=jdbc_url,
                        table='public."ChargingSessions"',
                        mode="append",
                        properties=connection_properties)

# Write stream using foreachBatch
query = (result_df.writeStream
         .outputMode("append")
         .foreachBatch(write_to_postgres)
         .option("checkpointLocation", "/tmp/checkpoints/ev_billing")
         .start())

query.awaitTermination()
