# evbilling_system
This project simulates an Electric Vehicle (EV) billing system using Kafka, Spark, and Azure services.

## Components
- Kafka Producer: Generates simulated EV charging session data and sends it to Azure Event Hubs.
- Azure Event Hubs: Acts as the Kafka broker.
- Spark Structured Streaming: Consumes data from Event Hubs, processes it, and writes to Azure SQL Database.
- Azure Database for PostgreSQL: Stores processed data for querying and analysis.

### Prerequisites
- Azure Account.
- Python 3.x installed.
- Python packages: kafka-python, faker, pyspark,

## Technologies Used
- Python
- Apache Kafka (via Azure Event Hubs)
- Apache Spark (via Azure Databricks)
- Azure Event Hubs
- Azure Database for PostgreSQL
- Azure Databricks
- Azure CLI