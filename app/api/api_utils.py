from flask import request, current_app
import csv
import traceback
import os


class Utils:
    request = request
    app = current_app

    @classmethod
    def delete_tmp(cls, filename):
        try:
            os.remove(filename)
        except Exception as e:
            print(e)
            pass

    @classmethod
    def bulk_upload(cls, entity_type):
        headers = cls.request.headers

        errors = []

        if "multipart/form-data" in headers.get("Content-Type"):
            print(cls.request.files.keys())
            for key in cls.request.files.keys():
                file = cls.request.files[key]
                file_path = file.filename
                

                if not os.path.exists('imported'):
                    os.mkdir('imported')
                
                file_path = f"imported/{file_path}"

                file.save(file_path)
                with open(file_path, "r") as csv_file:
                    csv_content = csv.reader(csv_file)
                    for row in csv_content:
                        try:
                            cls.app.config["ENGINE"].insert(entity_type, row)
                        except Exception as e:
                            print(e)
                            print(traceback.format_exc())
                            errors.append(f"Error: {e}, data: {row}")
                os.remove(file_path)
        return errors

    @classmethod
    def save_as_csv(cls, filename, data):
        tmp_path = "tmp_files"

        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        with open(f"{tmp_path}/{filename}", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data[0].keys())
            # Write each data row to the CSV file
            for row in data:
                writer.writerow([row[field] for field in row.keys()])
        return f"{tmp_path}/{filename}"
