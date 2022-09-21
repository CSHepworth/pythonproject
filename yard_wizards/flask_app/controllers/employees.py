from flask_app import app
from flask import render_template, redirect, request, session, flash
import re
from flask_app.models.employee import Employee
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session.clear()
    print(session)
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
    admin_status = Employee.get_by_email(data)
    if not employee:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(employee.password, request.form['password']):
        flash("Incorrect Password")
        return redirect('/')
    session['employee_id'] = employee.id
    session['employee_admin_status'] = admin_status.admin
    return redirect('/dashboard')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register_employee', methods = ["POST"])
def register():
    is_valid = Employee.validate_employee(request.form)
    if not is_valid:
        return redirect('/registration')
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
    admin_status = Employee.get_by_email(data)
    session['employee_admin_status'] = admin_status.admin
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        flash('Error')
        return redirect('/')
    data = {
        "id": session['employee_id'],
    }
    print(session)
    employee = Employee.get_by_id(data)
    return render_template('dashboard.html', employee = employee)
   
