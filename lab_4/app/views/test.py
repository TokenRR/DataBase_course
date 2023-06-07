from flask import Blueprint, render_template, request, redirect, url_for
from app import func

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/<person_uuid>/<id>", methods=["GET", "POST"])
def test(person_uuid, id):
    id = int(id)
    if request.method == "POST":
        func.test.delete_test(id)
        return redirect(url_for("person.person", uuid=person_uuid))
    test = func.test.serialize_test(id)
    columns = func.test.serialize_test_columns()
    return render_template(
        "test/test.html", 
        columns=columns,
        test=test
    )

@bp.route("/add/<person_uuid>", methods=["GET", "POST"])
def test_add(person_uuid):
    if request.method == "POST":
        func.test.create_test(person_uuid, request.form)
        return redirect(url_for("person.person", uuid=person_uuid))
    columns = func.test.serialize_test_columns(exclude=["id"])
    person = func.person.serialize_person(person_uuid)
    options = func.test.serialize_test_options()
    return render_template(
        "test/test_add.html",
        columns=columns,
        person=person,
        options=options,
    )

@bp.route("/edit/<person_uuid>/<id>", methods=["GET", "POST"])
def test_edit(person_uuid, id):
    id = int(id)
    if request.method == "POST":
        func.test.update_test(id, request.form)
        return redirect(url_for("person.person", uuid=person_uuid))
    columns = func.test.serialize_test_columns()
    test = func.test.serialize_test(id)
    options = func.test.serialize_test_options()
    return render_template(
        "test/test_edit.html",
        columns=columns,
        test=test,
        options=options,
    )