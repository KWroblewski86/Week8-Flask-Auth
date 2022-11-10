from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import User
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/api/signup', methods=["POST"])
def signMeUpAPI():
            data = request.json
            username = data['username']
            email = data['email']
            password = data['password']
            u1 = User.query.filter_by(username=username).first()
            u2 = User.query.filter_by(email=email).first()
            if u1 and u2:
                return {
                    'status': 'not ok',
                    'message': 'That username AND email already belong to an acount.'
                    }
            elif u1:
                return {
                    'status': 'not ok',
                    'message': 'That username already belongs to an acoount'
                    }  
            elif u2:
                return {
                    'status': 'not ok',
                    'message': 'That email already belongs to an acoount'
                    }
            else:

                #add user to database
                user = User(username, email, password)
                
                #add instance to SQL
                user.saveToDB()
                return {
                    'status': 'ok',
                    'message': 'Successfully created a user',
                }



@auth.route('/api/login', methods=["POST"])
def logMeInAPI():
    data = request.json
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': f'Succesfully logged in. Welcome back, {user.username}!',
                'user': user.to_dict()
            }
            
            login_user(user)
            return redirect(url_for('homePage'))
        else:
            return {
            'status': 'not ok',
            'message': 'Incorrect password.'
        }

    else:
        return {
            'status': 'not ok',
            'message': 'A user with that username does not exist.'
        }


from ..apiauthhelper import basic_auth
@auth.route('/api/token', methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': f'Succesfully logged in. Welcome back, {user.username}!',
                'user': user.to_dict()
            }