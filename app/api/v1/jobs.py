from api.v1 import api_blueprint
from api.api_utils import Utils
from flask import jsonify, current_app


@api_blueprint.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = current_app.config["ENGINE"].all("jobs")
    return jsonify(jobs)


@api_blueprint.route("/jobs", methods=["POST"])
def post_jobs():
    errors = Utils.bulk_upload("jobs")
    return jsonify(errors=errors)
