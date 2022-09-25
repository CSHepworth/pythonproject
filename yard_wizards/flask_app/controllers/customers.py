from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.employee import Employee
from flask_app.models.customer import Customer
import sql_to_csv


@app.route('/add_customer')
def add_customer():
    if 'employee_id' and 'employee_admin_status' not in session:
        flash('error')
        return redirect('/')
    if session['employee_admin_status'] != 1:
        flash('must be an admin to add customers')
        return redirect('/dashboard')
    data = {
        "id": session['employee_id']
    }
    employee = Employee.get_by_id(data)
    return render_template('add_customer.html', employee = employee)

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
    return redirect('/customers')

@app.route('/customers')
def customers_page():
    if 'employee_id' not in session:
        flash('Error')
        return redirect('/')
    data = {
        "id": session['employee_id']
    }
    employee = Employee.get_by_id(data)
    customers = Customer.get_all()
    return render_template('customers.html', employee = employee, customers = customers)

@app.route('/export_csv')
def export_csv():
    sql_to_csv.export()
    return redirect('/customers')