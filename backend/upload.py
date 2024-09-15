from azure.storage.blob import BlobServiceClient

# Connection string to Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=vtpdfstorage;AccountKey=hz7qB4MVJEao2W0NFtpI7/9Nr4FKVLuGIyuYvxYqb+dqEHDKFq8M6TkEzJyXTxHivj5p7eUt1jfY+AStXR0now==;EndpointSuffix=core.windows.net"

# Define the blob container and file details
container_name = "pdfcontainer"
local_file_path = "/Users/thiley/Documents/GitHub/Simplifile/backend/index.pdf"
blob_name = "vtpdfstorage"

# Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# Upload the file to blob storage
with open(local_file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data)

print(f"PDF file '{local_file_path}' uploaded to container '{container_name}' as blob '{blob_name}'")
