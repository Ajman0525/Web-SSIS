from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/students")
    def students():
        return render_template("students.html")

    @app.route("/programs")
    def programs():
        return render_template("programs.html")

    @app.route("/colleges")
    def colleges():
        return render_template("colleges.html")
    
    return app
