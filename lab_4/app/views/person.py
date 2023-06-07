from flask import Blueprint, render_template, request, redirect, url_for
from app import func
from app import NAME_DATA_BASE, mongo_db

bp = Blueprint("person", __name__, url_prefix="/person")


@bp.route("/<uuid>", methods=["GET", "POST"])
def person(uuid):
    if request.method == "POST":
        func.person.delete_person(uuid)
        return redirect(url_for("person.person_all_desc"))
    person = func.person.serialize_person(uuid)
    pcolumns = func.person.serialize_person_columns()
    tests = func.test.serialize_test_all(uuid)
    tcolumns = func.test.serialize_test_columns()
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
        func.person.update_person(uuid, request.form)
        return redirect(url_for("person.person", uuid=uuid))
    columns = func.person.serialize_person_columns()
    person = func.person.serialize_person(uuid)
    options = func.person.serialize_person_options()
    return render_template(
        "person/person_edit.html",
        columns=columns,
        person=person,
        options=options,
    )

if NAME_DATA_BASE in ['postgres']:

    @bp.route("/asc", methods=["GET"])
    def person_all_asc():
        pagination = func.person.serialize_person_all_asc()
        columns = func.person.serialize_person_columns()
        return render_template(
            "person/person_all_asc.html", 
            pagination=pagination,
            columns=columns
        )

    @bp.route("/desc", methods=["GET"])
    def person_all_desc():
        pagination = func.person.serialize_person_all_desc()
        columns = func.person.serialize_person_columns()
        return render_template(
            "person/person_all_desc.html", 
            pagination=pagination,
            columns=columns
        )
    
if NAME_DATA_BASE in ['mongo']:

    @bp.route("/asc", methods=["GET"])
    def person_all_asc():
        pagination = func.person.serialize_person_all_asc()
        columns = func.person.serialize_person_columns()
        return render_template(
            "person/mongo_person_all_asc.html", 
            pagination=pagination,
            columns=columns
        )

    @bp.route("/desc", methods=["GET"])
    def person_all_desc():
        pagination = func.person.serialize_person_all_desc()
        columns = func.person.serialize_person_columns()
        return render_template(
            "person/mongo_person_all_desc.html", 
            pagination=pagination,
            columns=columns
        )

@bp.route("/add", methods=["GET", "POST"])
def person_add():
    if request.method == "POST":
        func.person.create_person(request.form)
        return redirect(url_for("person.person_all_desc"))
    columns = func.person.serialize_person_columns(exclude=["outid"])
    options = func.person.serialize_person_options()
    return render_template(
        "person/person_add.html",
        columns=columns,
        options=options,
    )