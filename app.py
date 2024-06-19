from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from forms import UserForm
from models import db, User, init_db
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=('GET', 'POST'))
def add():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        dob = form.dob.data
        gender = form.gender.data
        image = form.image.data

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User(name=name, email=email, dob=dob, gender=gender, image=filename)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.dob = form.dob.data
        user.gender = form.gender.data
        image = form.image.data

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.image = filename

        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('index'))

    return render_template('update.html', form=form, user=user)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        query = request.form['query']
        users = User.query.filter(User.name.like(f'%{query}%')).all()
        return render_template('index.html', users=users)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
