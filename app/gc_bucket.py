import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage

logger = logging.getLogger()
load_dotenv()
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')


class GCBucket():

    @staticmethod
    def save_to_google_cloud(image):
        # Create a Cloud Storage client.
        try:
            gcs = storage.Client()
        except DefaultCredentialsError as exc:
            logger.warning(f"{str(exc)} Image will not be saved.")
            return None

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Change filename to unique
        filename = uuid4().hex
        image.filename = filename

        # Create a new blob and upload the file's content.
        blob = bucket.blob(image.filename)

        blob.upload_from_string(
            image.read(),
            content_type=image.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url
