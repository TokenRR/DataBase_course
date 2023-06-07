from flask import Blueprint, render_template, request
from app import func

bp = Blueprint("query", __name__, url_prefix="/query")


@bp.route("/", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        query_result = func.test.query(request.form)
        return  render_template(
            "query/query_result.html",
            query_result=query_result   
        )
    options = func.test.serialize_test_options()
    return render_template(
        "query/query.html",
        options=options
    )