from flask import request, current_app
import csv
import traceback


def bulk_upload(entity_type):
    headers = request.headers
    errors = []
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
                    try:
                        current_app.config["ENGINE"].insert(entity_type, row)
                    except Exception as e:
                        print(e)
                        print(traceback.format_exc())
                        if len(errors) > 2:
                            return errors
                        errors.append(f"Error: {e}, data: {row}")
    return errors


def save_as_csv(filename, data):
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data[0].keys())
        # Write each data row to the CSV file
        for row in data:
            writer.writerow([row[field] for field in row.keys()])
