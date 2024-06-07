from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
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

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://albumy:asdasdasd123123123@pursuecode.cn:3306/photogallery'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Dummy user model
# class User(UserMixin):
#     def __init__(self, id, username):
#         self.id = id
#         self.username = username

class User(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    privilege = db.Column(db.String(5), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    is_active = False
    def __repr__(self):
        return f'<User {self.name}>'

# In-memory user store
# users = {"user1": User(id=1, username="user1"), "user2": User(id=2, username="user2")}


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(name=username).first()
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
        return jsonify({
            "name": user.name,
            "password": user.password,
            "privilege": user.privilege,
            "email": user.email
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle signup logic here
        username = request.form["username"]
        password = request.form["password"]
        email = request.form['email']
        privilege = "user"
        if not username or not email:
            return jsonify({"error": "Invalid input"}), 400

        new_user = User(name=username, password=password, privilege=privilege, email=email)
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
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # Save image info to database here
            pass
    images = []  # Replace with logic to retrieve user's images from database
    return render_template("manage.html", images=images)


@app.route("/explore")
def explore():
    return render_template("explore.html")


@app.route("/random_image")
def random_image():
    # Logic to retrieve a random image from the database
    image_url = url_for(
        "static", filename="uploads/sample.jpg"
    )  # Replace with actual logic
    return jsonify(url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
