from flask import Flask, render_template, redirect, session, url_for

from app.college import college_blueprint
from app.program import program_blueprint
from app.student import student_blueprint
from app.home import home_blueprint
from app.user import user_blueprint
from app.database import init_app
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config")
    app.register_blueprint(college_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(student_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(home_blueprint)


    @app.route("/")
    def home():
        if "user_id" in session:
            user_name = session.get("username", "User")
            return render_template("home.html", user_name=user_name)
        return redirect(url_for("user.login"))

    init_app(app)
    
    return app
