# evbilling_system
Create a realtime simulated EV Charging station billing system using Kafka, Spark, and Azure services.

## Components

- Kafka Producer: Simulates EV charging data and sends it to Azure Event Hubs configured for Kafka.
- Spark Streaming Job: Consumes data from Event Hubs, processes it to calculate billing amounts using Azure Databricks.
- PostgreSQL DB: Stores the log data of each charging session
- Azure account with Event Hubs and Databricks set up.
- Python 3.11
- Python packages: `kafka-python`, `faker`.
