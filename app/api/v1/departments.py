from api.v1 import api_blueprint
from api.v1.utils import bulk_upload, save_as_csv
from flask import jsonify, current_app, request, send_file
from api.models import MostHiringDepartments
import uuid



@api_blueprint.route("/departments", methods=["GET"])
def get_departments():
    departments = current_app.config["ENGINE"].all("departments")
    return jsonify(departments)


@api_blueprint.route("/departments", methods=["POST"])
def post_departments():
    errors = bulk_upload("departments")
    return jsonify(errors=errors)


@api_blueprint.route("/departments/most_hiring")
def get_most_hiring_departments():
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
        save_as_csv(filename, response)
        return send_file(filename)
    
    return jsonify(departments=response)
    
