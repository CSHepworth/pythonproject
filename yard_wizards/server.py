from flask_app import app
from flask_app.controllers import employees, customers
import sql_to_csv

if __name__ == "__main__":
    app.debug=True
    app.run('0.0.0.0', port=5001)