from api.v1 import api_blueprint
from api.api_utils import Utils
from flask import jsonify, current_app


@api_blueprint.route("/jobs", methods=["GET"])
def get_jobs():
    """Returns a list of jobs
    ---
    produces:
      - application/json
      - text/csv

    parameters:
      - in: query
        name: format
        type: string

    definitions:
      Job:
        type: object
        properties:
          id:
            type: integer
          job:
            type: string
      JobArray:
        type: object
        properties:
          jobs:
            type: array
            items:
              $ref: '#/definitions/Job'

    responses:
      200:
        description: A list of Jobs
        content:
          text/csv:
            schema:
              type: string

        content:
          application/json:
            schema:
              $ref: '#/definitions/JobArray'
            
    """
    jobs = current_app.config["ENGINE"].all("jobs")
    return jsonify(jobs)


@api_blueprint.route("/jobs", methods=["POST"])
def post_jobs():
    """
    Insert Jobs from CSV file in Bulk Operation
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
            $ref: '#/definitions/job'

    responses:
        '200':
            schema:
                $ref: '#/definitions/status'
            description: Status from process

    """
    status = Utils.bulk_upload("jobs")
    return jsonify(status=status)
