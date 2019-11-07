from flask import request, jsonify, Flask
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config["DEBUG"]=True

database = r".\test.db"  # Tried r"app/test.db" the backslash causes an error - Its not the backslash

"""Create the database"""
def create_connection():
    c = None 
    try:
        c = sqlite3.connect(database)
        print(sqlite3.version)

        return c
    except Error as e:
        print("create_connection: %s" % e)


"""Create Tables"""
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("create_table: %s" %e)
    finally:
        if c:
            c.close()


"""Execute the operations"""
def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def execute(sql, isSelect=True):
    conn = sqlite3.connect(database)
    conn.row_factory = dic_factory
    cur = conn.cursor()
    if isSelect:
        return cur.execute(sql).fetchall()
    else:
        result = cur.execute(sql)
        conn.commit()
        return result


"""Start the database, run this before ["app.run()"]"""
def start_db():
    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        user_table_sql = """CREATE TABLE IF NOT EXISTS user(
            [id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [age] INTEGER NOT NULL,
            [name] TEXT NOT NULL
        );"""
        create_table(conn, user_table_sql)
    else:
        print("Error! cannot create the datebase connection")

""" HTTP functions """


@app.route("/", methods=['GET'])
def home():
    return "<h1>Title</h1><p>Local database</p>"


""" Post modified for database """
# Add new user
@app.route("/user", methods=["POST"])
def post_users():  # Adding to Users dictionary using POST
    user = request.get_json()
    _age = user["age"]
    _name = user["name"]
    # Note that the Post method refers to inserting values into a database
    sql = f"INSERT INTO user ([age], [name]) VALUES ({_age}, '{_name}');"

    result = execute(sql, False)

    # returns the last row of a modified by a query
    user["id"] = result.lastrowid

    return jsonify(user)


""" Put modified for database """
# Update user
@app.route("/user", methods=["PUT"])
def put_users():
    user = request.get_json()   # Get the request you want to "PUT"
    _id = user['id']
    _age = user['age']
    _name = user['name']

    sql = f"UPDATE user SET [age] = {_age}, [name] = '{_name}' WHERE [id] = {_id}:" 
    execute(sql, False)

    return {}


""" Get modified for database """
# List all users
@app.route("/users", methods=["GET"])
def get_users():    
    _id = request.args['id'] if 'id' in request.args else 0
    _age = request.args['age'] if 'age' in request.args else 0
    _name = request.args['name'] if 'name' in request.args else ''

    sql = f""" SELECT * FROM user WHERE 
            ({_id} = 0 OR [id] = {_id})
            AND ({_age} = 0 OR [age] = {_age})
            AND ('{_name}' = '' OR UPPER([name]) = UPPER('{_name}'));"""

    users = execute(sql)

    return jsonify(users)


""" Delete user by id modified for database """
@app.route("/user/<_id>", methods=["DELETE"])  # Input the route URL in Postman
def delete_users(_id):
    sql = f"DELETE FROM user WHERE id = {int(_id)};"
    execute(sql, False)

    return {}

if __name__ == "__main__":
    start_db()
    app.run()
