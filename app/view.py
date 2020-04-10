from app import app, db
from flask import request, redirect, render_template, flash, url_for, Response
import requests
from datetime import datetime, date
from werkzeug.datastructures import MultiDict
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from models import *
from forms import *
import wtforms
import json



login_manager.login_view = 'login'


@app.route('/login/', methods=['POST',  'GET'])
def login():
    form = LoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        try:

            user = db.session.query(User).filter(User.name == form.name.data).first()
            user_email = db.session.query(User).filter(user.email == form.email.data).first()

            if user and user_email :
                login_user(user)
                return redirect('/')

            flash("Invalid name/email.")
            return render_template('login.html', form=form)
        except:
            flash("Invalid name/email.")
            return render_template('login.html', form=form)
    else:
        
        return render_template('login.html', form=form)
    
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/adduser/', methods=['POST',  'GET'])
def add_user():
    form = AddForm()
    if request.method == 'POST' and form.validate_on_submit() :
        new_name = form.name.data 
        new_surname = form.surname.data
        new_email = form.email.data  
        new_birthday = form.birthday.data
        user = db.session.query(User).filter(User.email == new_email).first()
        if not user:
            if form.gender.data == "u":
                new_gender = None
            else:
                new_gender = bool(int(form.gender.data))

            if new_birthday == date.today():
                new_birthday = None

            new_user = User(name=new_name, surname=new_surname, email=new_email, gender=new_gender, birthday=new_birthday)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login/')
            except:
                flash("Error with adding new user.")
                return render_template('adduser.html', form=form, message="") 
        else:
            flash("Error with adding new user.")
            return render_template('adduser.html', form=form, message="")
    
    return render_template('adduser.html', form=form)   


@app.route('/feedback/',methods=['POST', 'GET'])
@login_required
def feedback():
    form = AddFeedback()
    if request.method == 'POST' and form.validate_on_submit(): 
            user = db.session.query(User).filter(current_user.email == form.email.data and current_user.name == form.name.data).first()
            if user:
                content = form.feedback.data
                new_comment = Comment(user_id=current_user.id,content=content)
                try:
                    db.session.add(new_comment)
                    db.session.commit()
                    return redirect('/comments/')
                except:
                    flash("Error with adding new comment")
                    return render_template('addfeedback.html', form=form)
            else:
                flash("Invalid name/email or they aren't yours ")
                return render_template('addfeedback.html', form=form)
    return render_template('addfeedback.html', form=form)


@app.route('/comments/',methods=['POST', 'GET'])
@login_required
def comment():
    comments = db.session.query(User, Comment).outerjoin(Comment, User.id == Comment.user_id).all()
    return render_template('comments.html', comments=comments)


   

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Comment.query.get_or_404(id)
    if db.session.query(User).filter(current_user.id == task_to_delete.user_id).first():
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/comments/')
        except:
            return flash("Delete error")
    else:
        flash("It is not your comment")
        return redirect('/comments/')

@app.route('/user/')
@login_required
def user_info():
    return render_template('user.html', user=current_user)


@app.route('/',methods=['GET'])
@login_required
def index():
    params ={
        'spider_name': 'weather_spider',
        'start_requests': True,
    }
    response = requests.get('http://localhost:9080/crawl.json',params)
    data = json.loads(response.text)
    data=[data['items'][0]['Temperature'],
    data['items'][0]['Sky'],
    data['items'][0]['Wind'],
    data['items'][0]['Rainfall'],
    data['items'][0]['Sky_middle'],
    data['items'][0]['Date']]

    time = [i for i in range(0,22,3) ]

    return render_template('index.html', 
    data=data, l_data=len(data[0][2]),
    time=time)



