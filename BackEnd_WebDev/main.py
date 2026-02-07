from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies
)
from sqlalchemy import create_engine, text
import bcrypt
from datetime import timedelta
from datetime import datetime
# 1. Define your database connection details
DB_USER = "python"
DB_PASSWORD = "$HxiCRmKRd3P"
DB_HOST = "192.168.60.110"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "She_Innovates"

# *Important: URL-encode the password if it contains special characters*
database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Create the engine
engine = create_engine(database_url)

# Create Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'sdawadvasdadwawd'  # Change this to a secure secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False      # True in HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
jwt = JWTManager(app)

# ======================
# Register User
# ======================
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies
)
from sqlalchemy import create_engine, text
import bcrypt
from datetime import timedelta
from datetime import datetime
# 1. Define your database connection details
DB_USER = "python"
DB_PASSWORD = "$HxiCRmKRd3P"
DB_HOST = "192.168.60.110"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "She_Innovates"

database_url = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?sslmode=disable&connect_timeout=10"
)
engine = create_engine(database_url)

# Create Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'sdawadvasdadwawd'  # Change this to a secure secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False      # True in HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
jwt = JWTManager(app)

# ======================
# Register User
# ======================
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    dateofbirth = data.get("dateofbirth")  # Expecting 'YYYY-MM-DD' format

    # Validate required fields
    if not all([username, password, firstname, lastname, dateofbirth]):
        return jsonify({"error": "All fields are required"}), 400

    # Convert date string to date object
    try:
        dob = datetime.strptime(dateofbirth, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    # Hash password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # SQL queries
    insert_auth_user = text("""
        INSERT INTO "MadDadSkills".auth_users (username, password_hash)
        VALUES (:username, :password_hash)
        RETURNING id
    """)

    insert_user = text("""
        INSERT INTO "MadDadSkills".users (auth_user_id, firstname, lastname, dateofbirth)
        VALUES (:auth_user_id, :firstname, :lastname, :dateofbirth)
    """)

    try:
        with engine.begin() as conn:  # Transaction begins
            # Insert into auth_users
            result = conn.execute(insert_auth_user, {
                "username": username,
                "password_hash": password_hash
            })
            auth_user_id = result.scalar()  # Get new auth_user ID

            # Insert into users table
            conn.execute(insert_user, {
                "auth_user_id": auth_user_id,
                "firstname": firstname,
                "lastname": lastname,
                "dateofbirth": dob
            })

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# Login User
# ======================
@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    query = text("""
        SELECT id, password_hash
        FROM "MadDadSkills".auth_users
        WHERE username = :username
    """)

    with engine.connect() as conn:
        user = conn.execute(query, {"username": username}).fetchone()

    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    user_id, password_hash = user

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user_id))

    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)
    return response, 200











@app.route('/GetUsers', methods=['GET'])
@jwt_required()
def get_users():
    # SQL query to fetch users from the database
    query = text('SELECT * FROM "MadDadSkills".users')
    
    try:
        # Execute the query and fetch results
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        # Convert the rows to dictionaries using column names
        column_names = result.keys()  # Get column names
        users = [dict(zip(column_names, row)) for row in rows]

        # Return the users as a JSON response
        return jsonify(users)
    
    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({"error": str(e)}), 500
    
@app.route('/GetLessons', methods=['GET'])
@jwt_required()
def get_Lessons():
    # SQL query to fetch users from the database
    query = text('SELECT * FROM "MadDadSkills".lesson')
    
    try:
        # Execute the query and fetch results
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        # Convert the rows to dictionaries using column names
        column_names = result.keys()  # Get column names
        users = [dict(zip(column_names, row)) for row in rows]

        # Return the users as a JSON response
        return jsonify(users)
    
    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({"error": str(e)}), 500
    


@app.route('/GetOverAllStatus', methods=['GET'])
@jwt_required()
def get_OverAllStatus():
    # SQL query to fetch users from the database
    query = text('SELECT * FROM "MadDadSkills".overall_status')
    
    try:
        # Execute the query and fetch results
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        # Convert the rows to dictionaries using column names
        column_names = result.keys()  # Get column names
        users = [dict(zip(column_names, row)) for row in rows]

        # Return the users as a JSON response
        return jsonify(users)
    
    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    
    return "Welcome to the User API! Use /GetUsers, /GetLessons, or /GetOverAllStatus to fetch data."

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
