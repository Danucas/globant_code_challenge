from api.v1 import api_blueprint
from api.api_utils import Utils
from flask import jsonify, current_app, request, send_file, after_this_request
from api.models import MostHiringDepartments
import uuid


@api_blueprint.route("/departments", methods=["GET"])
def get_departments():
    """Returns a list of departments
    ---
    produces:
      - application/json
      - text/csv

    parameters:
      - in: query
        name: format
        type: string

    definitions:
      department:
        type: object
        properties:
          id:
            type: integer
          department:
            type: string
      ListOfDepartments:
        type: object
        properties:
          departments:
            type: array
            items:
              $ref: '#/definitions/department'

    responses:
      200:
        description: A list of departments
        content:
          text/csv:
            schema:
              type: string

        content:
          application/json:
            schema:
              $ref: '#/definitions/ListOfDepartments'
            
    """
    departments = current_app.config["ENGINE"].all("departments")
    if request.args.get("format") == "csv":
        filename = f"{uuid.uuid4().hex}.csv"
        file_path = Utils.save_as_csv(filename, departments.get("departments"))

        @after_this_request
        def remove_file(response):
            Utils.delete_tmp(file_path)
            return response

        return send_file(file_path)
    return jsonify(departments)


@api_blueprint.route("/departments", methods=["POST"])
def post_departments():
    """
    Insert Departments from CSV file in Bulk Operation
    ---

    definitions:
      status:
        type: object
        properties:
          rows_writen:
            type: integer
          errors:
            type: array
            items:
              type: string
              description: Error Description, aling with the data that failed
          duplicates:
            type: array
            items:
              type: integer
          duplicates_description:
            type: string


    parameters:
        - name: file
          required: false
          in: formData
          type: file
          schema:
            $ref: '#/definitions/department'

    responses:
        '200':
            schema:
                $ref: '#/definitions/status'
            description: Status from process

    """
    status = Utils.bulk_upload("departments")
    return jsonify(status=status)


@api_blueprint.route("/departments/most_hiring")
def get_most_hiring_departments():
    """
    Calculate Most Hiring departments comparing mean average from 2021
    ---
    produces:
      - application/json
      - text/csv
    
    parameters:
      - in: query
        name: format
        type: string

    definitions:
      MostHiringDepartments:
        type: object
        properties:
          id:
            type: integer
          department:
            type: string
          hired:
            type: integer
    
      ListOfMostHiringDepartments:
        type: array
        items:
          $ref: '#/definitions/MostHiringDepartments'
    
    responses:
      200:
        content:
          application/json:
            schema:
              $ref: '#/definitions/ListOfMostHiringDepartments'
    """
    query = """
    WITH average AS (
        SELECT AVG(hired_co) AS mean
            FROM(
                SELECT COUNT(*) as hired_co
                FROM hired_employees em, departments dp
                WHERE em.department_id = dp.id AND em.datetime BETWEEN '2021-01-01' AND '2021-12-31'
                GROUP BY dp.id
            ) as hired_co
    ),

    hiredcount AS (
        SELECT COUNT(*) AS hired_count, dp.id AS id
        FROM hired_employees em, departments dp
        WHERE em.department_id = dp.id AND em.datetime BETWEEN '2021-01-01' AND '2021-12-31'
        GROUP BY dp.id
    )

    SELECT 
        dp.id,
        dp.department,
        hc.hired_count AS hired

    FROM hiredcount hc, average av, departments dp
    WHERE hc.id = dp.id AND hc.hired_count > av.mean
    ORDER BY hc.hired_count DESC
    """
    engine = current_app.config["ENGINE"]
    employees = engine.query(query)

    response = [MostHiringDepartments(*e).dict() for e in employees]

    if request.args.get("format") == "csv":
        filename = f"{uuid.uuid4().hex}.csv"
        file_path = Utils.save_as_csv(filename, response)

        @after_this_request
        def remove_file(response):
            Utils.delete_tmp(file_path)
            return response

        return send_file(file_path)

    return jsonify(departments=response)
