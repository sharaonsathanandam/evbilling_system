# evbilling_system
This project simulates an Electric Vehicle (EV) billing system using Kafka, Spark, that are containerized and run on Azure services.

## Components
- Azure Container registries: Stores the containerized image of the Kafka Producer program
- Azure Kubernetes services: Orchestrates the execution of the Kafka Producer program
- Azure Event Hubs: Acts as the Kafka broker and receives data sent by the Kafka Producer program.
- Azure Databricks: Consumes data from Event Hubs, processes it, and writes to Azure SQL Database.
- Azure Database for PostgreSQL: Stores processed data for querying and analysis.
- Azure Functions: To control scaling of Kafka producer pods on Azure Kubernetes Service (AKS).
- Azure Data Factory: To orchestrate the workflow.


### Prerequisites
- Azure Account.
- Python 3.x installed.
- Python packages: kafka-python, faker, pyspark,

## Technologies Used
- Python
- Apache Kafka (via Azure Event Hubs)
- Apache Spark (via Azure Databricks)
- Azure Event Hubs
- Azure Container registries
- Azure Kubernetes
- Azure Functions
- Azure Data Factory
- Azure Database for PostgreSQL
- Azure Databricks
- Azure CLI