import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from pymongo import MongoClient

# Azure Document Intelligence setup
azure_endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')  # Replace with your Azure endpoint
azure_api_key = os.getenv('AZURE_FORM_RECOGNIZER_KEY') # Replace with your Azure API key

client = DocumentAnalysisClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_api_key))

# MongoDB setup
mongo_client = MongoClient("mongodb+srv://thiley:thileyPassword@cluster0.x3zrc.mongodb.net/")  # Replace with your MongoDB URI if remote
db = mongo_client["documentDatabase"]
collection = db["documentData"]

# Analyze document
document_path = "/Users/thiley/Desktop/Hackathon/index.pdf"  # Replace with your document's path

with open(document_path, "rb") as f:
    poller = client.begin_analyze_document("prebuilt-document", document=f.read())
    result = poller.result()

# Prepare extracted data
extracted_data = {
    "document_id": "12345",  # You can generate a unique ID for each document
    "pages": []
}

# Iterate through each page in the result
for idx, page in enumerate(result.pages):
    page_data = {
        "page_number": idx + 1,
        "lines": [],
        "tables": []
    }

    # Extract lines of text
    for line in page.lines:
        page_data["lines"].append({"text": line.content})

    # Extract table data
    for table in result.tables:
        table_data = {"rows": []}
        for cell in table.cells:
            table_data["rows"].append({
                "row": cell.row_index,
                "column": cell.column_index,
                "content": cell.content
            })
        page_data["tables"].append(table_data)

    extracted_data["pages"].append(page_data)

# Insert the extracted data into MongoDB
collection.insert_one(extracted_data)

# Optional: Print a success message
print("Document data has been successfully inserted into MongoDB.")
