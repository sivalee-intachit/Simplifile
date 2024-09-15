import os
import requests
import json
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Storage Blob credentials
connection_string = "DefaultEndpointsProtocol=https;AccountName=vtpdfstorage;AccountKey=hz7qB4MVJEao2W0NFtpI7/9Nr4FKVLuGIyuYvxYqb+dqEHDKFq8M6TkEzJyXTxHivj5p7eUt1jfY+AStXR0now==;EndpointSuffix=core.windows.net"
container_name = "pdfcontainer"
home_directory = os.path.expanduser("~")
download_file_path = os.path.join(home_directory, "Downloads", "downloaded.pdf")

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# List blobs and get the most recent one
blobs = list(container_client.list_blobs())
most_recent_blob = max(blobs, key=lambda b: b['last_modified'])

# Download the blob
blob_name = most_recent_blob['name']
with open(download_file_path, "wb") as download_file:
    blob_data = container_client.download_blob(blob_name)
    download_file.write(blob_data.readall())

print("Downloaded the PDF from Blob Storage.")

# Azure Document Intelligence credentials
endpoint = "https://simplifile.cognitiveservices.azure.com/"
api_key = "4fb70f90ac3443fab9b9f7844f6a5d27"

# Create a Document Analysis client
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Open the downloaded PDF file
with open(download_file_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
    result = poller.result()
    
# Extract content
extracted_text = ""
for page in result.pages:
    for line in page.lines:
        extracted_text += f"{line.content}\n"

# Print the extracted content
print("Extracted text from PDF:")
print(extracted_text)

#Getter for other files
def getExtracted_Text():
    return extracted_text
