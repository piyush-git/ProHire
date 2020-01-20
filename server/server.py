from flask import Flask
from flask import request, make_response, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import hashlib
import os
import jwt

app = Flask(__name__)
CORS(app)

app.config['MYSQL_USER'] = 'piyush'
app.config['MYSQL_PASSWORD'] = 'piyush'
app.config['MYSQL_DB'] = 'ProHire'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

def add_customer():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    driving_license = request.json["driving_license"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO Customer (first_name, last_name, driving_license) values (%s, %s, %s)""", (first_name, last_name, driving_license,) 
    )
    mysql.connection.commit()
    cursor.close()
    return {"message": "customer added successfully", "status": 200}


def add_booking():
    registration_number = request.json["registration_number"]
    from_date = request.json["from_date"]
    to_date = request.json["to_date"]
    driving_license = request.json["driving_license"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO Booking (from_date, to_date, car_id, customer_id) values (%s, %s, (SELECT id from Car where registration_number = %s), (SELECT id from Customer where driving_license = %s))""", (from_date, to_date, registration_number, driving_license,) 
    )
    mysql.connection.commit()
    cursor.close()
    return {"message": "booking successful", "status": 200}


@app.route('/add-cars', methods=["POST"])
def add_car():
    model = request.json["model"]
    car_type = request.json["type"]
    number_of_seats = request.json["number_of_seats"]
    color = request.json["color"]
    registration_number  = request.json["registration_number"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO Car (model, type, number_of_seats, color, registration_number) values (%s, %s, %s, %s, %s)""", (model, car_type, number_of_seats, color, registration_number,) 
    )
    mysql.connection.commit()
    cursor.close()
    return {"message": "car added successfully", "status": 200}

@app.route('/search', methods=["POST"])
def search_cars():
    from_date = request.json["from_date"]
    to_date = request.json["to_date"]
    print(from_date)
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * from Car where (from_date = NULL AND to_date = NULL) OR (from_date < %s AND to_date < from_date) OR (to_date > %s AND from_date > to_date) """, (from_date, to_date,)
        # """select * from Car where from_date IS NULL and to_date is NULL""",
    )
    results = cursor.fetchall()
    # print(results)
    cursor.close()
    return {"cars": results, "status": 200}

@app.route('/car-details/<id>', methods=["GET"])
def get_car_details(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * from Car where id = %s """, (id,)
    )
    results = cursor.fetchone()
    cursor.close()
    return {"car_details": results, "status": 200}

if __name__ == "__main__":
   app.run()




# {
# 	"model" : "Maruti Swift",
#     "type" : "Hatchback",
#     "number_of_seats" : 5,
#     "color" : "white",
#     "registration_number"  : "KA34X2101"
# }