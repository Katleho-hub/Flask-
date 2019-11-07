from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["DEBUG"] = True

""" Users dictionary """
users_dic = [{"id":1, "name":"Thabo", "age":23},
            {"id":2, "name":"Katleho", "age":23 },]

""" Mapping URL routes using the 'app.route' decorator"""
@app.route("/", methods=['GET'])  
def home():
    return "<h1>Title</h1><p>Paragraph.</p>"


""" Returning Users dictionary with GET request """
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users_dic)

""" Returning User by id with GET request """
@app.route("/user", methods=["GET"])
def get_user_by_id():
    # We get the "id" value/parameter from the request
    if "id" in request.args:   # At this point the request is checked to see if the string "id" is present
        id = int(request.args["id"])  # The parameter given to this string i.e. [id=1] is converted to a int value
    else:
        return "Error: No id field provided. Please specify an id."

    for user in users_dic:  # Go through the Users dictionary by user
        if user["id"] == id:  # Parameter from request matches value in user dictionary 
            return jsonify(user)
    return {}

""" Make use of Postman to Post [raw - JSON] """
@app.route("/user", methods=["POST"])
def post_users():  # Adding to Users dictionary using POST
    user = request.get_json()
    user["id"] = len(users_dic) + 1  # Auto creating id value 
    users_dic.append(user)

    return jsonify(user)


""" Running multiple queries in a single method"""
@app.route("/user_", methods=["GET"])   # TODO: add a condition to return an empty list if no arguments are parsed
def get_user():
    users = []
    for user in users_dic:  # For each user
        contProp = 0
        for arg in request.args:  # GO THROUGH ALL ARGUMENTS IN THE REQUEST
            val = user[arg]   # i.e. user['name'] - the arg is parsed as a Key
            param = request.args[arg]   # (request.args["id"])
            if isinstance(val, int):  
                param = int(param)  
            if isinstance(val, str):
                val = val.upper()
                param = param.upper()
            if val == param:
                contProp += 1
        if contProp == len(request.args):
            users.append(user)

    return jsonify(users)

""" To update a user, create the PUT method """
@app.route("/user", methods=["PUT"])
def put_users():
    user_ = request.get_json()   # Get the request you want to "PUT"
    for idx, user in enumerate(users_dic):
        if user["id"] == user_["id"]:   # Compare users in list to user to be updated. [in this instance they are compared by id]
            users_dic[idx] = user_  
    
    return {}

""" Delete user by id """
@app.route("/user/<id>", methods=["DELETE"])  # Input the route URL in Postman
def delete_users(id):
    for user in users_dic:
        if user["id"] == int(id):
            users_dic.remove(user)
    
    return {}

if __name__ == "__main__":
    app.run()
