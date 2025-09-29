from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/users")
def users():
    pass