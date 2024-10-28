import logging
import json
import os
import azure.functions as func
from kubernetes import client, config
from azure.identity import ClientSecretCredential
import yaml

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to scale Kafka producer.')

    try:
        # Get request body
        req_body = req.get_json()
        replica_count = req_body.get('replicaCount')
        if replica_count is None:
            return func.HttpResponse(
                "Please pass 'replicaCount' in the request body",
                status_code=400
            )

        # Get environment variables for AKS authentication
        TENANT_ID = os.environ['TENANT_ID']
        CLIENT_ID = os.environ['CLIENT_ID']
        CLIENT_SECRET = os.environ['CLIENT_SECRET']
        SUBSCRIPTION_ID = os.environ['SUBSCRIPTION_ID']
        RESOURCE_GROUP = os.environ['RESOURCE_GROUP']
        AKS_CLUSTER_NAME = os.environ['AKS_CLUSTER_NAME']

        # Authenticate with AKS using Azure Identity
        credentials = ClientSecretCredential(
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

        # Get AKS cluster credentials
        from azure.mgmt.containerservice import ContainerServiceClient
        container_client = ContainerServiceClient(credentials, SUBSCRIPTION_ID)
        aks_cluster = container_client.managed_clusters.get(RESOURCE_GROUP, AKS_CLUSTER_NAME)
        access_profile = container_client.managed_clusters.list_cluster_admin_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
        kubeconfig = access_profile.kubeconfigs[0].value.decode()

        # Load Kubernetes config
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig))

        # Create Kubernetes API client
        apps_v1 = client.AppsV1Api()

        # Scale the deployment
        namespace = 'default'  # Change if using a different namespace
        deployment_name = 'kafka-producer'
        body = {
            'spec': {
                'replicas': replica_count
            }
        }
        response = apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=namespace,
            body=body
        )

        logging.info(f"Scaled deployment '{deployment_name}' to {replica_count} replicas.")
        return func.HttpResponse(
            f"Scaled deployment '{deployment_name}' to {replica_count} replicas.",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error scaling Kafka producer: {e}")
        return func.HttpResponse(
            f"Error scaling Kafka producer: {e}",
            status_code=500
        )
