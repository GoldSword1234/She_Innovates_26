from flask import Flask, jsonify, request
from collections import defaultdict
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies
)
from sqlalchemy import create_engine, text
import bcrypt
from datetime import timedelta
from datetime import datetime
from flask_cors import CORS

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
app.config["JWT_COOKIE_SECURE"] = True      # True in HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_COOKIE_DOMAIN"] = ".jgao.cc"

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
engine = create_engine(
    database_url,
    pool_size=10,          # how many connections to keep open
    max_overflow=20,       # extra temporary connections under load
    pool_timeout=30,       # seconds to wait for a free connection
    pool_recycle=1800,     # recycle connections every 30 min (avoids idle disconnect issues)
    pool_pre_ping=True,    # checks connection health before using it (fixes "server closed the connection")
)

# Create Flask app
app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://white-moss-0a8ef8f0f.1.azurestaticapps.net",
        "https://white-moss-0a8ef8f0f.1.azurestaticapps.net",
        "https://maddadskills.jgao.cc"

    ]}}
)

app.config["JWT_SECRET_KEY"] = "8c4f6d2c9f5e0d6a3a2d9e41f8e5b9f8b6d9e7f1c5a3b4d8e6c2a9f1d3e7b4"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# --- IMPORTANT FOR SUBDOMAIN FRONTEND <-> API COOKIE ---
app.config["JWT_COOKIE_DOMAIN"] = ".jgao.cc"     # share across api.jgao.cc + jgao.cc
app.config["JWT_COOKIE_SAMESITE"] = "None"       # cross-site cookie
app.config["JWT_COOKIE_SECURE"] = True           # requires HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True

jwt = JWTManager(app)
# ======================
# Register User
# ======================
# @app.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")
#     firstname = data.get("firstname")
#     lastname = data.get("lastname")
#     dateofbirth = data.get("dateofbirth")  # Expecting 'YYYY-MM-DD' format

#     # Validate required fields
#     if not all([username, password, firstname, lastname, dateofbirth]):
#         return jsonify({"error": "All fields are required"}), 400

#     # Convert date string to date object
#     try:
#         dob = datetime.strptime(dateofbirth, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

#     # Hash password
#     password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#     # SQL queries
#     insert_auth_user = text("""
#         INSERT INTO "MadDadSkills".auth_users (username, password_hash)
#         VALUES (:username, :password_hash)
#         RETURNING id
#     """)

#     insert_user = text("""
#         INSERT INTO "MadDadSkills".users (auth_user_id, firstname, lastname, dateofbirth)
#         VALUES (:auth_user_id, :firstname, :lastname, :dateofbirth)
#     """)

#     try:
#         with engine.begin() as conn:  # Transaction begins
#             # Insert into auth_users
#             result = conn.execute(insert_auth_user, {
#                 "username": username,
#                 "password_hash": password_hash
#             })
#             auth_user_id = result.scalar()  # Get new auth_user ID

#             # Insert into users table
#             conn.execute(insert_user, {
#                 "auth_user_id": auth_user_id,
#                 "firstname": firstname,
#                 "lastname": lastname,
#                 "dateofbirth": dob
#             })

#         return jsonify({"message": "User registered successfully"}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    dateofbirth = data.get("dateofbirth")

    if not all([username, password, firstname, lastname, dateofbirth]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        dob = datetime.strptime(dateofbirth, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    insert_auth_user = text("""
        INSERT INTO "MadDadSkills".auth_users (username, password_hash)
        VALUES (:username, :password_hash)
        RETURNING id
    """)

    insert_user = text("""
        INSERT INTO "MadDadSkills".users (auth_user_id, firstname, lastname, dateofbirth)
        VALUES (:auth_user_id, :firstname, :lastname, :dateofbirth)
        RETURNING userid
    """)

    get_not_started_status = text("""
        SELECT taskstatusid
        FROM "MadDadSkills".task_status
        WHERE status = 'Not Started'
    """)

    insert_tasks = text("""
        INSERT INTO "MadDadSkills".tasks (userid, lessonid, taskstatusid)
        SELECT :user_id, lessonid, :status_id
        FROM "MadDadSkills".lesson
    """)

    try:
        with engine.begin() as conn:
            # 1️⃣ Create auth user
            auth_result = conn.execute(insert_auth_user, {
                "username": username,
                "password_hash": password_hash
            })
            auth_user_id = auth_result.scalar()

            # 2️⃣ Create user
            user_result = conn.execute(insert_user, {
                "auth_user_id": auth_user_id,
                "firstname": firstname,
                "lastname": lastname,
                "dateofbirth": dob
            })
            user_id = user_result.scalar()

            # 3️⃣ Get "Not Started" status ID
            status_result = conn.execute(get_not_started_status).fetchone()
            if not status_result:
                raise Exception("Task status 'Not Started' not found")

            not_started_id = status_result[0]

            # 4️⃣ Create tasks for ALL lessons
            conn.execute(insert_tasks, {
                "user_id": user_id,
                "status_id": not_started_id
            })

        return jsonify({"message": "User registered and tasks initialized"}), 201

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
        SELECT id AS auth_user_id, password_hash
        FROM "MadDadSkills".auth_users
        WHERE username = :username
    """)

    with engine.begin() as conn:
        user = conn.execute(query, {"username": username}).fetchone()

    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    auth_user_id, password_hash = user

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(auth_user_id))

    response = jsonify({"message": "Login successful","username": username,"auth_user_id": auth_user_id })
    set_access_cookies(response, access_token)
    return response, 200










@app.route('/GetUsers', methods=['GET'])
@jwt_required()
def get_users():
    # SQL query to fetch users from the database
    query = text('SELECT * FROM "MadDadSkills".users')
    auth_user_id = get_jwt_identity()
    #query = text('SELECT * FROM "MadDadSkills".task_overview WHERE auth_user_id = :user_id')


    
    try:
        # Execute the query and fetch results
        with engine.begin() as connection:
            # result = connection.execute(query, {"user_id": user_id})
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
        
@app.route('/GetUser', methods=['GET'])
@jwt_required()
def get_user():
    # SQL query to fetch users from the database
    # query = text('SELECT * FROM "MadDadSkills".users')
    auth_user_id = get_jwt_identity()
    query = text('SELECT * FROM "MadDadSkills".users WHERE auth_user_id = :user_id')
    

    
    try:
        # Execute the query and fetch results
        with engine.begin() as connection:
            result = connection.execute(query, {"user_id": auth_user_id})
            # result = connection.execute(query)
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
    
    user_id = get_jwt_identity()
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

@app.route('/GetModules', methods=['GET'])
@jwt_required()
def get_modules():
    # SQL query to fetch users from the database
    
    user_id = get_jwt_identity()
    query = text('SELECT * FROM "MadDadSkills"."Get_Modules"')
    try:
        # Execute the query and fetch results
        with engine.begin() as connection:
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
    query = text('SELECT * FROM "MadDadSkills".overall_status WHERE auth_user_id = :user_id')
    user_id = get_jwt_identity()
    
    try:
        # Execute the query and fetch results
        with engine.connect() as connection:
            # result = connection.execute(query)
            result = connection.execute(query, {"user_id": user_id})
            rows = result.fetchall()

        # Convert the rows to dictionaries using column names
        column_names = result.keys()  # Get column names
        users = [dict(zip(column_names, row)) for row in rows]

        # Return the users as a JSON response
        return jsonify(users)
    
    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({"error": str(e)}), 500

@app.route('/GetTasks', methods=['GET'])
@jwt_required()
def get_tasks():
    
    user_id = get_jwt_identity()
    moduletype = request.args.get("moduletype")  # e.g. "Finance"

    base_sql = '''
        SELECT *
        FROM "MadDadSkills".task_overview
        WHERE auth_user_id = :user_id
    '''

    params = {"user_id": user_id}

    if moduletype:
        base_sql += ' AND moduletype = :moduletype'
        params["moduletype"] = moduletype

    query = text(base_sql)

    try:
        with engine.connect() as connection:
            result = connection.execute(query, params)
            rows = result.fetchall()
            column_names = result.keys()

        rows_dict = [dict(zip(column_names, row)) for row in rows]

        grouped_by_user = defaultdict(lambda: defaultdict(lambda: {"tasks": []}))

        for row in rows_dict:
            user = row["fullname"]
            lesson_key = (row["lessonid"], row["modulename"])

            if "lessonid" not in grouped_by_user[user][lesson_key]:
                grouped_by_user[user][lesson_key].update({
                    "lessonid": row["lessonid"],
                    "lesson_description": row["lesson_description"],
                    "modulename": row["modulename"],
                    "module_description": row["module_description"],
                    "moduletype": row["moduletype"],
                })

            grouped_by_user[user][lesson_key]["tasks"].append({
                "taskid": row["taskid"],
                "name": row["name"],
                "sequence": row["sequence"],
                "status": row["status"],
                "taskstatusid": row["taskstatusid"]
            })

        result_list = []
        for user, lessons in grouped_by_user.items():
            result_list.append({
                "fullname": user,
                "lessons": list(lessons.values())
            })

        return jsonify(result_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/', methods=['GET'])
def home():
    
    return "Welcome to the User API! Use /GetUsers, /GetLessons, or /GetOverAllStatus to fetch data."

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
