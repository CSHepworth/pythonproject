from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import pandas as pd

def export():
    db = 'yard_wizard_schema'


    sql_query = pd.read_sql_query('''SELECT first_name, last_name, address_line1, address_line2, city, state, zip, lawn_sqft FROM customers''', connectToMySQL(db).connection)
    sql_query.to_csv(r'C:\Users\coope\GitHub\pythonproject\yard_wizards\customer_data.csv', index = False)