import os
from openai import OpenAI
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Storage Blob credentials
connection_string = "DefaultEndpointsProtocol=https;AccountName=vtpdfstorage;AccountKey=hz7qB4MVJEao2W0NFtpI7/9Nr4FKVLuGIyuYvxYqb+dqEHDKFq8M6TkEzJyXTxHivj5p7eUt1jfY+AStXR0now==;EndpointSuffix=core.windows.net"  # Get this from Azure portal under Access keys
container_name = "pdfcontainer"
blob_name = "vtpdfstorage"
download_file_path = "/Users/thiley/Documents/GitHub/Simplifile/backend/downloaded.pdf"  # Path where the PDF will be saved locally

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# Download the blob
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

# Extract PDF contents into a single text variable
pdf_text = ""

if hasattr(result, 'pages'):
    for page in result.pages:
        if hasattr(page, 'lines'):
            for line in page.lines:
                pdf_text += line.content + "\n"
else:
    print("No pages detected in the document.")

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("AZURE_OPENAI_KEY"))

# Define the text to summarize
pdf_text = ""

# Create a chat completion request
response = client.chat.completions.create(
    messages=[
        {"role": "user", "content": f"Summarize the following text:\n\n{pdf_text}"}
    ],
    model="gpt-3.5-turbo",  # Use the appropriate model
    temperature=0.7,
    max_tokens=500
)

# Extract and print the summary
summary = response.choices[0].message['content'].strip()
print("Summary of the PDF:")
print(summary)