from django.core.files.storage import default_storage
# from google.cloud import storage as gcs_storage
from django.http import HttpRequest
from django.conf import settings
from .interfaces import ImageStorage 

class ImageLocalStorage(ImageStorage):
    def store(self, profile_image):
        if profile_image:
            # Store the image
            file_name = default_storage.save('uploaded_images/' + profile_image.name, profile_image)
            return default_storage.url(file_name)
        
# class ImageGCPStorage(ImageStorage):
#     def store(self, profile_image)        :
#         if profile_image:
#             client = gcs_storage.Client.from_service_account_json(settings.GCP_KEY_FILE)
#             bucket = client.bucket(settings.GCP_BUCKET)
#             blob = bucket.blob('images/test.png')
#             blob.upload_from_file(profile_image)        


class ImageProvider:
    def get_instance(self, storage_type):
        if storage_type == 'local':
            return ImageLocalStorage()
        # elif storage_type == 'gcp':
        #     return ImageGCPStorage()
        else:
            raise ValueError("Unsupported storage type: " + storage_type)

class ImagesLocalStorage():
    # Local storage
    def store(self, profile_image):
        if profile_image:
            # Store the image
            file_name = default_storage.save('uploaded_images/' + profile_image.name, profile_image)
            return(default_storage.url(file_name))
        
        return None
    
# class ImagesGCPStorage():
#     def store(self, profile_image)        :
#         if profile_image:
#             client = gcs_storage.Client.from_service_account_json(settings.GCP_KEY_FILE)
#             bucket = client.bucket(settings.GCP_BUCKET)
#             blob = bucket.blob('images/test.png')
#             blob.upload_from_file(profile_image)


    