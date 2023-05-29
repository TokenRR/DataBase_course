from flask import Blueprint, render_template, request, redirect, url_for
from app import service

bp = Blueprint("person", __name__, url_prefix="/person")


@bp.route("/<uuid>", methods=["GET", "POST"])
def person(uuid):
    if request.method == "POST":
        service.person.delete_person(uuid)
        return redirect(url_for("person.person_all_desc"))
    person = service.person.serialize_person(uuid)
    pcolumns = service.person.serialize_person_columns()
    tests = service.test.serialize_test_all(uuid)
    tcolumns = service.test.serialize_test_columns()
    return render_template(
        "person/person.html", 
        pcolumns=pcolumns,
        person=person,
        tcolumns=tcolumns,
        tests=tests
    )
    
@bp.route("/<uuid>/edit", methods=["GET", "POST"])
def person_edit(uuid):
    if request.method == "POST":
        service.person.update_person(uuid, request.form)
        return redirect(url_for("person.person", uuid=uuid))
    columns = service.person.serialize_person_columns()
    person = service.person.serialize_person(uuid)
    options = service.person.serialize_person_options()
    return render_template(
        "person/person_edit.html",
        columns=columns,
        person=person,
        options=options,
    )

@bp.route("/asc", methods=["GET"])
def person_all_asc():
    pagination = service.person.serialize_person_all_asc()
    columns = service.person.serialize_person_columns()
    return render_template(
        "person/person_all_asc.html", 
        pagination=pagination,
        columns=columns
    )

@bp.route("/desc", methods=["GET"])
def person_all_desc():
    pagination = service.person.serialize_person_all_desc()
    columns = service.person.serialize_person_columns()
    return render_template(
        "person/person_all_desc.html", 
        pagination=pagination,
        columns=columns
    )

@bp.route("/add", methods=["GET", "POST"])
def person_add():
    if request.method == "POST":
        service.person.create_person(request.form)
        return redirect(url_for("person.person_all_desc"))
    columns = service.person.serialize_person_columns(exclude=["outid"])
    options = service.person.serialize_person_options()
    return render_template(
        "person/person_add.html",
        columns=columns,
        options=options,
    )