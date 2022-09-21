from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.employee import Employee
from flask_app.models.customer import Customer

@app.route('/add_customer')
def add_customer():
    return render_template('add_customer.html')

@app.route('/create_customer', methods = ["POST"])
def create_customer():
    is_valid = Customer.validate_customer(request.form)
    if not is_valid:
        return redirect('/add_customer')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "address_line1": request.form['address_line1'],
        "address_line2": request.form['address_line2'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zip": request.form['zip'],
        "lawn_sqft": request.form['lawn_sqft']
    }
    customer = Customer.save(data)
    return redirect('/dashboard')

@app.route('/customers')
def customers():
    if 'employee_id' not in session:
        flash('Error')
        return redirect('/')
    all_customers = Customer.get_all()
