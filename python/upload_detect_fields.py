import requests
import base64
import json

# Your Anvil API Key
ANVIL_API_KEY = "F03Q8GC5E8aiKXCutHuatbBFdTDTcG6W"
ANVIL_API_URL = "https://app.useanvil.com/graphql"

# Encode API Key for Basic Auth
encoded_auth = base64.b64encode(f"{ANVIL_API_KEY}:".encode("ascii")).decode("ascii")

headers = {
    "Authorization": f"Basic {encoded_auth}"
}

def upload_pdf_and_detect_fields(pdf_path):
    """ Upload a PDF dynamically and detect relevant fields. """
    query = """
    mutation ($file: Upload!) {
      createCast(
        file: $file,
        detectFields: true,        # Enables basic field detection
        advancedDetectFields: true # Enables AI-powered detection
      ) {
        eid
        fieldInfo
      }
    }
    """

    operations = json.dumps({
        "query": query,
        "variables": {"file": None}
    })

    file_map = json.dumps({"0": ["variables.file"]})

    with open(pdf_path, "rb") as pdf_file:
        files = {
            "operations": (None, operations, "application/json"),
            "map": (None, file_map, "application/json"),
            "0": (pdf_path, pdf_file, "application/pdf"),
        }

        print("📡 Uploading PDF and requesting field detection...")

        response = requests.post(ANVIL_API_URL, headers=headers, files=files)

        print(f"🔍 Status Code: {response.status_code}")

        try:
            response_json = response.json()
            print(f"✅ Detected Fields JSON: {json.dumps(response_json, indent=2)}")
            return response_json
        except requests.exceptions.JSONDecodeError:
            print("❌ Failed to decode JSON response")
            print(f"🔍 Raw Response: {response.text}")
            return {"error": "Invalid JSON response"}


# Example Usage (Dynamically uploads and processes any PDF)
pdf_file_path = "Real_Estate_Brokerage_Fee_Sharing_Agreement.pdf"  # Change this to your dynamic file path
detected_fields = upload_pdf_and_detect_fields(pdf_file_path)