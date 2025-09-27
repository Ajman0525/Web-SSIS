from flask import Flask, render_template

from app.college import college_blueprint
from app.program import program_blueprint
from app.student import student_blueprint
from app.database import init_app
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config")
    app.register_blueprint(college_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(student_blueprint)


    @app.route("/")
    def home():
        return render_template("home.html")

    # @app.route("/students")
    # def students():
    #     return render_template("students.html")

    # @app.route("/programs")
    # def programs():
    #     return render_template("programs.html")

    # @app.route("/colleges")
    # def colleges():
    #     return render_template("colleges.html")



    init_app(app)
    
    return app
