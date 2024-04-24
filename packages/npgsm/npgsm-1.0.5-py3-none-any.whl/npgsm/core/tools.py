import hashlib
import json
import logging
import os
from typing import Optional

import google.cloud.logging
from google.api_core import exceptions
from google.cloud import secretmanager, secretmanager_v1

_MY_RETRIABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)


class NPGSM(object):
    def __init__(self, project_id, gcp_service_account_path: Optional[str] = None):
        self.project_id = project_id
        self.path_json_key = gcp_service_account_path
        self.__add_environment()
        self.client = self.__get_client()

    def __add_environment(self):
        if self.path_json_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_client(self):
        client = google.cloud.logging.Client(project=self.project_id)
        client.setup_logging(log_level=logging.INFO)
        return secretmanager.SecretManagerServiceClient()

    # ================================= Utility functions =================================
    def create_secret(self, secret_id, region=""):
        """Create the secret_id in Google Cloud Secret Manager
        Args:
            secret_id (str): The secret name to store secret value
        """
        # Example input: create_secret("my_secret_value")
        # Create the Secret Manager client.
        # Build the resource name of the parent project.
        parent = f"projects/{self.project_id}"
        # Build a dict of settings for the secret
        if region:
            secret = {
                "replication": {"user_managed": {"replicas": [{"location": region}]}}
            }
        else:
            secret = {"replication": {"automatic": {}}}
        # Create the secret
        try:
            response = self.client.create_secret(
                secret_id=secret_id, parent=parent, secret=secret  # type: ignore
            )
        except Exception as e:
            print(f"Can not create the secret:{secret_id} with error {e}")
            return False
        else:
            print(f"Created secret: {response.name}")
            return True

    def add_secret_version(self, secret_id, payload):
        # add_secret_version("my_secret_value", "Hello Secret Manager")
        # add_secret_version("my_secret_value", "Hello Again, Secret Manager")
        # Build the resource name of the parent secret.
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        elif isinstance(payload, dict):
            payload = json.dumps(payload).encode("utf-8")
        # Add the secret version.
        response = self.client.add_secret_version(parent=parent, payload={"data": payload})  # type: ignore
        # Print the new secret version name.
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id, version_id="latest"):
        # view the secret value
        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        # Access the secret version.
        response = self.client.access_secret_version(name=name)
        # Return the decoded payload.
        payload = response.payload.data.decode("UTF-8")  # type: ignore
        return payload

    def get_versions(self, secret_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        request = secretmanager.ListSecretVersionsRequest(parent=name)
        page_result = self.client.list_secret_versions(request=request)
        # client.list_secret_versions(request={"parent": parent})
        # Handle the response
        versions = [v.name for v in page_result if v.state.name != "DESTROYED"]
        return versions

    def delete_secret(self, secret_id):
        name = self.client.secret_path(self.project_id, secret_id)
        print(f"Deleting Secret: {name}")
        self.client.delete_secret(request={"name": name})
        print(f"Deleted secret {secret_id}")

    def delete_secret_version(self, secret_name, version_id):
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version_id}"
        request = secretmanager.DestroySecretVersionRequest(
            name=name,
        )
        response = self.client.destroy_secret_version(request=request)
        print(response)

    def disable_secret_version(self, secret_name, version_id):
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version_id}"
        request = secretmanager.DisableSecretVersionRequest(
            name=name,
        )
        response = self.client.disable_secret_version(request=request)
        print(response)

    def list_secret(self, parent):
        # parent = "projects/586562253728"
        request = secretmanager_v1.ListSecretsRequest(
            parent=parent,
        )
        data = self.client.list_secrets(request)
        secrets = []
        for secret in data:
            secrets.append(secret.name.split("/")[-1])
        return secrets

    def secret_hash(self, secret_value):
        # return the sha224 hash of the secret value
        return hashlib.sha224(bytes(secret_value, "utf-8")).hexdigest()
