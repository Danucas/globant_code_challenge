from api.v1 import api_blueprint
from flask import jsonify, request
import csv
import json



def bulk_upload(entity_type):
    headers = request.headers
    data = []
    if "multipart/form-data" in headers.get("Content-Type"):
        print(request.files.keys())
        for key in request.files.keys():
            file = request.files[key]
            file_path = file.filename
            print(dir(file))
            file.save(file_path)
            with open(file_path, "r") as csv_file:
                csv_content = csv.reader(csv_file)
                for row in csv_content:
                    data.append(row)
    print(json.dumps(data, indent=4))




@api_blueprint.route("/departments", methods=["GET"])
def get_departments():
    return jsonify(data={})


@api_blueprint.route("/departments", methods=["POST"])
def post_departments():
    
    bulk_upload("departments")

    return jsonify(data={})
