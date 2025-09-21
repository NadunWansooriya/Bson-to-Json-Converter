import os
import bson
import json
from bson import ObjectId
from datetime import datetime

# Custom JSON Encoder for MongoDB/BSON types
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO string
        return super().default(obj)

# Path where your BSON files are stored
INPUT_DIR = r"C:\Users\nadun\neurocore\neurocoredb_backup\neurocoredb_backup\neurocoredb"

# Path for converted JSON files (separate folder)
OUTPUT_DIR = r"C:\Users\nadun\neurocore\neurocoredb_backup\neurocoredb_backup\json_output"

# Create output folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through all files in the directory
for file_name in os.listdir(INPUT_DIR):
    if file_name.endswith(".bson"):
        bson_file = os.path.join(INPUT_DIR, file_name)
        json_file = os.path.join(OUTPUT_DIR, file_name.replace(".bson", ".json"))

        print(f"Converting {file_name} -> {os.path.basename(json_file)}")

        with open(bson_file, "rb") as bf:
            try:
                # Decode all BSON documents
                data = bson.decode_all(bf.read())

                # Write JSON with pretty formatting using custom encoder
                with open(json_file, "w", encoding="utf-8") as jf:
                    json.dump(data, jf, cls=JSONEncoder, ensure_ascii=False, indent=2)

            except Exception as e:
                print(f"ERROR converting {file_name}: {e}")

print("\nConversion finished! ✅ All JSON files are in:", OUTPUT_DIR)
