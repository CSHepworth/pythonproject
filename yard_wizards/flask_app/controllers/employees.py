from flask_app import app
from flask import render_template, redirect, request, session, flash
import re
from flask_app.models.employee import Employee
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login_employee', methods = ["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    employee = Employee.get_by_email(data)
    if not employee:
        flash("Invalid Email/Password")
        return redirect('/')
    session['employee_id'] = employee.id
    return redirect('/dashboard')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register_employee', methods = ["POST"])
def register():
    is_valid = Employee.validate_employee(request.form)
    if not is_valid:
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "dob": request.form['dob'],
        "applicator_id": request.form['applicator_id'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    address = {
        "email": request.form['email']
    }
    email = Employee.get_by_email(address)
    if email:
        flash('email already in use!')
        return redirect('/registration')
    id = Employee.save(data)
    session['employee_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
   
