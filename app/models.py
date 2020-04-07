from app import db, login_manager
from datetime import date
from flask_login import LoginManager, UserMixin, login_required



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    date_created = db.Column(db.DateTime, default=date.today())

    def __repr__(self):
        return '<Comment %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname =  db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.BOOLEAN, nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    

    def check_email(self,  email_user):
        if self.email == email_user:
            return True
        return False
         


    def __repr__(self):
        return '<User %r>' % self.id
