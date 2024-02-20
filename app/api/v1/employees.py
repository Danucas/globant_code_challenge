from api.v1 import api_blueprint
from api.api_utils import Utils
from flask import jsonify, current_app, request, send_file, after_this_request
from api.models import EmployeesByQuarters
import uuid


@api_blueprint.route("/hired_employees", methods=["GET"])
def get_hired_employees():
    """Returns a list of Hired Employees
    ---

    parameters:
      - in: query
        name: format
        type: string

    definitions:
      hired_employee:
        type: object
        properties:
            id:
                type: string
            name:
                type: string
            datetime:
                type: string
                description: ISO format string
            department_id:
                type: integer
                description: Foreign Key for departments
            job_id:
                type: integer
                description: Foreign Key for jobs
    responses:
      200:
        description: List of Hired Employees
        schema:
          $ref: '#/definitions/hired_employee'
        examples:
          department: [
                {"id": 1, "department": "Test Department"}
          ]
    """
    hired_employees = current_app.config["ENGINE"].all("hired_employees")
    if request.args.get("format") == "csv":
        filename = f"{uuid.uuid4().hex}.csv"
        file_path = Utils.save_as_csv(filename, hired_employees.get("hired_employees"))

        @after_this_request
        def remove_file(response):
            Utils.delete_tmp(file_path)
            return response

        return send_file(file_path)
    return jsonify(hired_employees)


@api_blueprint.route("/hired_employees", methods=["POST"])
def post_hired_employees():
    """
    Insert Hired Employees from CSV file in Bulk Operation
    ---
    definitions:
      hired_employee:
        type: object
        properties:
            id:
                type: string
            name:
                type: string
            datetime:
                type: string
                description: ISO format string
            department_id:
                type: integer
                description: Foreign Key for departments
            job_id:
                type: integer
                description: Foreign Key for jobs

    parameters:
        - name: file
          required: false
          in: formData
          type: file
          schema:
            $ref: '#/definitions/hired_employee'

    responses:
        '200':
            description: Status from process
            schema:
                $ref: '#/definitions/status'

    """
    status = Utils.bulk_upload("hired_employees")
    return jsonify(status=status)


@api_blueprint.route("/hired_employees/by_quarter")
def get_hired_employees_by_quarter():
    """
    Calculate Hired Employees by Quarters in 2021
    ---
    produces:
      - application/json
      - text/csv
    
    parameters:
      - in: query
        name: format
        type: string

    definitions:
      EmployeesByQuarters:
        type: object
        properties:
          department:
            type: string
          job:
            type: string
          q1:
            type: integer
          q2:
            type: integer
          q3:
            type: integer
          q4:
            type: integer
    
      EmployeesByQuartersArray:
        type: array
        items:
          $ref: '#/definitions/EmployeesByQuarters'
    
    responses:
      200:
        content:
          application/json:
            schema:
              $ref: '#/definitions/EmployeesByQuartersArray'
    """
    quarters = [
        ("2021-01-01", "2021-03-31"),
        ("2021-04-01", "2021-06-30"),
        ("2021-07-01", "2021-09-30"),
        ("2021-10-01", "2021-12-31"),
    ]

    query = f"""
    SELECT d.department, j.job, 
    COUNT(CASE WHEN he.datetime BETWEEN '{quarters[0][0]}' AND '{quarters[0][1]}' THEN he.name END),
    COUNT(CASE WHEN he.datetime BETWEEN '{quarters[1][0]}' AND '{quarters[1][1]}' THEN he.name END),
    COUNT(CASE WHEN he.datetime BETWEEN '{quarters[2][0]}' AND '{quarters[2][1]}' THEN he.name END),
    COUNT(CASE WHEN he.datetime BETWEEN '{quarters[3][0]}' AND '{quarters[3][1]}' THEN he.name END)
    FROM hired_employees he, jobs j, departments d
    WHERE he.job_id=j.id AND he.department_id=d.id
    GROUP BY d.id, j.id
    ORDER BY d.department ASC, j.job ASC
    """
    engine = current_app.config["ENGINE"]
    employees = engine.query(query)
    response = [EmployeesByQuarters(*e).dict() for e in employees]

    if request.args.get("format") == "csv":
        filename = f"{uuid.uuid4().hex}.csv"
        file_path = Utils.save_as_csv(filename, response)

        @after_this_request
        def remove_file(response):
            Utils.delete_tmp(file_path)
            return response

        return send_file(file_path)

    return jsonify(data=response)
