from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy
import os
import random
from flask import session


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://photogallery:asdasdasd123123123@someaddress:3306/photogallery"
)
db = SQLAlchemy(app)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Maximum file size: 16MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Dummy user model
# class User(UserMixin):
#     def __init__(self, id, username):
#         self.id = id
#         self.username = username


class User(UserMixin, db.Model):
    __tablename__ = "users"
    name = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(32), nullable=False)
    privilege = db.Column(db.String(5), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    is_active = True

    def __repr__(self):
        return f"<User {self.name}>"

    def get_id(self):
        return self.name


# In-memory user store
# users = {"user1": User(id=1, username="user1"), "user2": User(id=2, username="user2")}


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(name=username).first()
        # user.id =
        # Here you should add logic to verify username and password
        # For demonstration, we assume any password is correct
        if user:
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")


def get_user(username):
    user = User.query.filter_by(name=username).first()
    if user:
        return (
            jsonify(
                {
                    "name": user.name,
                    "password": user.password,
                    "privilege": user.privilege,
                    "email": user.email,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "User not found"}), 404


# def latest_user():
#     latest_user = User.query.order_by(desc(User.name)).first()
#     if latest_user:
#         return latest_user.id
#     else:
#         return 0


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle signup logic here
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        privilege = "user"
        # id = latest_user() + 1
        if not username or not email:
            return jsonify({"error": "Invalid input"}), 400

        new_user = User(
            name=username, password=password, privilege=privilege, email=email
        )
        db.session.add(new_user)
        db.session.commit()

    return render_template("signup.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("index"))


@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Image successfully uploaded")
            return redirect(url_for("manage"))
    images = os.listdir(app.config["UPLOAD_FOLDER"])
    image_urls = [url_for("static", filename="uploads/" + image) for image in images]
    return render_template("manage.html", images=image_urls)


@app.route("/explore")
def explore():
    return render_template("explore.html")


@app.route("/random_images")
def random_images():
    if "loaded_images" not in session:
        session["loaded_images"] = []

    all_images = set(os.listdir(app.config["UPLOAD_FOLDER"]))
    loaded_images = set(session["loaded_images"])
    available_images = list(all_images - loaded_images)

    if not available_images:
        session["loaded_images"] = []
        available_images = list(all_images)

    random_images = random.sample(available_images, min(len(available_images), 10))
    session["loaded_images"] += random_images
    image_urls = [
        url_for("static", filename="uploads/" + image) for image in random_images
    ]
    return jsonify(images=[{"url": url} for url in image_urls])


if __name__ == "__main__":
    app.run(debug=True)
