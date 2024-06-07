# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

def create_app_with_ctx():
    with app.app_context():
        db.create_all()

# 将路由注册移动到这里
@app.route('/')
def index():
    return render_template('main/index.html')

@app.route('/explore')
def explore():
    with app.app_context():
        images = Image.query.all()
        return render_template('main/explore.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        new_image = Image(filename=file.filename)
        with app.app_context():
            db.session.add(new_image)
            db.session.commit()
        file.save('uploads/' + file.filename)
        return redirect(url_for('explore'))
    return render_template('upload.html')

@app.route('/delete/<int:image_id>')
def delete(image_id):
    with app.app_context():
        image_to_delete = Image.query.get_or_404(image_id)
        db.session.delete(image_to_delete)
        db.session.commit()
        # 删除对应的文件
        return redirect(url_for('explore'))

if __name__ == '__main__':
    app.run(debug=True)
