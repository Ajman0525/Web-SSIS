from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db

# @app.route("/colleges")
#     def colleges():
#         return render_template("colleges.html")