import argparse
import json
import os, sys
from badb.questionnaire import askQuestion


def importsAndConfigWrite(f, app_name, schema, secret):
    f.write("from flask import Flask, jsonify, request, session, redirect, url_for, render_template \n")
    f.write("from werkzeug.security import generate_password_hash, check_password_hash \n")
    f.write("import sqlite3 \n")
    f.write("import json\n")
    for i in schema:
        f.write("from Models."+i+" import "+str(i).capitalize()+"\n")
    f.write("\n")
    f.write("app = Flask(__name__) \n")
    f.write("app.secret_key = '"+secret+"' \n")
    f.write("DB_NAME = '"+app_name+".db' \n\n")

def initializedDatabaseWrite(f, schema):
    f.write("#Initialize database \n")
    f.write("def init_db():\n")
    f.write("\tconn = sqlite3.connect(DB_NAME) \n")
    f.write("\tc = conn.cursor() \n")
    for i in schema:
        tableString = ""
        f.write("\tc.execute('''CREATE TABLE IF NOT EXISTS "+i+" (")
        for j in schema[i]:
            tableString += j+" "+schema[i][j]+", "
        tableString = tableString[: len(tableString)-2]
        f.write(tableString+")''') \n")
    f.write("\tconn.commit() \n")
    f.write("\tconn.close() \n\n")

def authenticationWrite(f, auth, prefix):
    if(auth['auth']):
        f.write("#Authentication decorator \n")
        f.write("def login_required(f): \n")
        f.write("\tdef decorated_function(*args, **kwargs):\n")
        f.write("\t\tif '"+auth['email_field']+"' not in session:\n")
        f.write("\t\t\treturn jsonify({'message': 'Access denied to this route'})\n")
        f.write("\t\treturn f(*args, **kwargs)\n")
        f.write("\tdecorated_function.__name__ = f.__name__\n")
        f.write("\treturn decorated_function \n\n")

        f.write("#Login a User\n")
        f.write("@app.route(\"/"+(prefix+'/' if prefix else '')+"login\", methods=[\"POST\"])\n")
        f.write("def login():\n")
        f.write("\tdata = request.get_json()\n")
        f.write("\temail = data.get('"+auth['email_field']+"')\n")
        f.write("\tpassword = data.get('"+auth['pass_field']+"')\n")
        f.write("\n")
        f.write("\tconn = sqlite3.connect(DB_NAME)\n")
        f.write("\tc = conn.cursor()\n")
        f.write("\tc.execute('SELECT "+auth['email_field']+", "+auth['pass_field']+" FROM "+auth['table']+" WHERE "+auth['email_field']+" = ?', (email,))\n")
        f.write("\tuser = c.fetchone()\n")
        f.write("\tconn.close()\n\n")
        f.write("\tif user and check_password_hash(user[1], password):\n")
        f.write("\t\tsession['"+auth['email_field']+"'] = user[0]\n")
        f.write("\t\treturn jsonify({'message': 'Login successful'}), 200\n")
        f.write("\telse:\n")
        f.write("\t\treturn jsonify({'message': 'Invalid username or password'}), 401\n\n")
    
def getRouteWrite(f, auth, schema, routes, i, prefix):
    f.write("#Route for GET "+i+"\n")
    f.write("@app.route('/"+(prefix+'/' if prefix else '')+i+"', methods=['GET'])\n")
    if auth['auth'] and routes.__contains__('GET'):
        f.write("@login_required\n")
    f.write("def get_"+i+"():\n")
    f.write("\tconn = sqlite3.connect(DB_NAME)\n")
    f.write("\tc = conn.cursor()\n")
    f.write("\tc.execute('SELECT * FROM "+i+"')\n")
    f.write("\t"+i+"= ["+str(i).capitalize()+"(*row) for row in c.fetchall()]\n")
    f.write("\tconn.close()\n")
    f.write("\t"+i+"_json = []\n")
    f.write("\tfor i in "+i+":\n")
    f.write("\t\t"+i+"_json.append({\n")
    f.write("\t\t\t'id': i._id,\n")
    lineStr = ""
    for j in schema[i]:
        lineStr += "\t\t\t'"+j+"': i._"+j+",\n"
    lineStr = lineStr[:len(lineStr)-2]
    f.write(lineStr+"\n")
    f.write("\t\t})\n")
    f.write("\treturn jsonify("+i+"_json)\n\n")

def postRouteWrite(f, auth, routes, schema, i, prefix):
    f.write("#Route for POST "+i+"\n")
    f.write("@app.route('/"+(prefix+'/' if prefix else '')+i+"', methods=['POST'])\n")
    if auth['auth'] and routes.__contains__('POST'):
        f.write("@login_required\n")
    f.write("def add_"+i+"():\n")
    f.write("\tdata = request.get_json()\n")
    for j in schema[i]:
        f.write("\t"+j+" = data.get('"+j+"')\n")
    f.write("\t"+auth['pass_field']+" = generate_password_hash(data.get('"+auth['pass_field']+"'))\n")
    f.write("\tconn = sqlite3.connect(DB_NAME)\n")
    f.write("\tc = conn.cursor()\n")
    newStr = ""
    qStr = ""
    for j in schema[i]:
        newStr += j+", "
        qStr += "?, "
    newStr = newStr[:len(newStr)-2]
    qStr = qStr[:len(qStr)-2]
    f.write("\ttry:\n")
    f.write("\t\tc.execute('INSERT INTO "+i+" ("+newStr+") VALUES ("+qStr+")', ("+newStr+"))\n")
    f.write("\t\tconn.commit()\n")
    f.write("\t\tresponse = jsonify({'message': '"+i+" added successfully'}), 201\n")
    f.write("\texcept sqlite3.IntegrityError as e:\n")
    f.write("\t\tprint('Invalid Data entry', e)\n")
    f.write("\t\tresponse = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400\n")
    f.write("\tfinally:\n")
    f.write("\t\tconn.close()\n\n")
    f.write("\treturn response\n\n")

def putRouteWrite(f, auth, schema, routes, i, prefix):
    f.write("# Route for PUT "+i+"\n")
    f.write("@app.route('/"+(prefix+'/' if prefix else '')+i+"/<int:"+i+"_id>', methods=['PUT'])\n")
    if auth['auth'] and routes.__contains__('PUT'):
        f.write("@login_required\n")
    f.write("def update_"+i+"("+i+"_id):\n")
    f.write("\tdata = request.get_json()\n")
    string = ""
    for j in schema[i]:
        string += j+" = ?, "
        f.write("\t"+j+" = data.get('"+j+"')\n")
    string = string[:len(string)-2]
    f.write("\n")
    f.write("\tconn = sqlite3.connect(DB_NAME)\n")
    f.write("\tc = conn.cursor()\n")
    f.write("\ttry:\n")
    newStr = ""
    for j in schema[i]:
        newStr += j+", "
    newStr = newStr[:len(newStr)-2]
    f.write("\t\tc.execute('UPDATE "+i+" SET "+string+" WHERE id = ?', ("+newStr+", "+i+"_id))\n")
    f.write("\t\tconn.commit()\n")
    f.write("\t\tresponse = jsonify({'message': '"+i+" updated successfully'}), 201\n")
    f.write("\texcept sqlite3.IntegrityError as e:\n")
    f.write("\t\tprint('Invalid Data entry', e)\n")
    f.write("\t\tresponse = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400\n")
    f.write("\tfinally:\n")
    f.write("\t\tconn.close()\n\n")
    f.write("\treturn response\n\n")

def deleteRouteWrite(f, auth, routes, i, prefix):
    f.write("# Route for DELETE "+i+"\n")
    f.write("@app.route('/"+(prefix+'/' if prefix else '')+i+"/<int:"+i+"_id>', methods=['DELETE'])\n")
    if auth['auth'] and routes.__contains__('DELETE'):
        f.write("@login_required\n")
    f.write("def delete_"+i+"("+i+"_id):\n")
    f.write("\tconn = sqlite3.connect(DB_NAME)\n")
    f.write("\tc = conn.cursor()\n")
    f.write("\tc.execute('DELETE FROM "+i+" WHERE id = ?', ("+i+"_id,))\n")
    f.write("\tconn.commit()\n")
    f.write("\tconn.close()\n\n")
    f.write("\treturn jsonify({'message': '"+i+" deleted successfully'}), 201\n\n")

def customRouteWrite(f, prefix, custom_routes):
    if custom_routes:
        for i,_ in enumerate(custom_routes):
            route = custom_routes[i]
            f.write("# Custom routes "+route['route_method']+" "+route['route']+"\n")
            f.write("@app.route('/"+(prefix+'/' if prefix else '')+route['route']+"', methods=['"+route['route_method']+"'])\n")
            if route['auth']:
                f.write("@login_required\n")
            f.write("def "+route['route']+"():\n")
            if route['url_param']:
                qstr = ""
                for j in route['url_param']:
                    qstr += j+", "
                    f.write("\t"+j+" = request.args.get('"+j+"')\n")
                qstr = qstr[: len(qstr) - 2]
            f.write("\tconn = sqlite3.connect(DB_NAME)\n")
            f.write("\tc = conn.cursor()\n")
            if route['url_param']:
                f.write("\t"+route['route']+" = c.execute('"+route['query']+"', ("+qstr+")).fetchall()\n")
            else:
                f.write("\t"+route['route']+" = c.execute('"+route['query']+"').fetchall()\n")
            f.write("\tconn.commit()\n")
            f.write("\tconn.close()\n\n")
            # f.write("\t"+route['route']+"_json"+" = json.dumps( [dict(ix) for ix in "+route['route']+"] )\n")
            f.write("\treturn jsonify("+route['route']+")\n\n")

def invocationWrite(f):
    f.write("if __name__ == '__main__':\n")
    f.write("\tinit_db()\n")
    f.write("\tapp.run(debug=True)\n\n")

def createEndpoints(app_name, auth, schema, secret, prefix, custom_routes):
    f = open(app_name+"/app.py", 'a')
    importsAndConfigWrite(f=f, app_name=app_name, schema=schema, secret=secret)
    initializedDatabaseWrite(f=f, schema=schema)
    authenticationWrite(f=f,auth=auth, prefix=prefix)
    for i in schema:
        routes = []
        if auth['auth']:
            routes = auth['auth_routes'][i].split(', ') if auth['auth_routes'][i] else []
        
        print("GET route for "+i)
        getRouteWrite(f=f, auth=auth, schema=schema, routes=routes, i=i, prefix=prefix)

        print("POST route for "+i)
        postRouteWrite(f=f, auth=auth, routes=routes, schema=schema, i=i, prefix=prefix)

        print("PUT route for "+i)
        putRouteWrite(f=f, auth=auth, schema=schema, routes=routes, i=i, prefix=prefix)

        print("DELETE route for "+i)
        deleteRouteWrite(f=f, auth=auth, routes=routes, i=i, prefix=prefix)

    customRouteWrite(f=f, custom_routes=custom_routes, prefix=prefix)
    invocationWrite(f)
    f.close()


def createModels(app_name, schema):
    os.mkdir(os.path.join(app_name, "Models"))
    s = open(app_name+"/Models/__init__.py","a")
    s.write("")
    s.close()
    for i in schema:
        f = open(app_name+"/Models/"+i+".py", 'a')
        f.write("class "+str(i).capitalize()+":\n")
        params = ""
        for j in schema[i]:
            params += j+", "
        params = params[: len(params)-2]
        # Write constructor
        f.write("\tdef __init__(self, "+params+"):\n")
        # f.write("\t\tself._id = id\n")
        for var in schema[i]:
            f.write("\t\tself._"+var+" = "+var+"\n")
        f.write("\n")
        # f.write("\tdef get_id(self):\n")
        # f.write("\t\treturn self._id\n\n")
        # Write getter methods
        for var in schema[i]:
            f.write("\tdef get_"+var+"(self):\n")
            f.write("\t\treturn self._"+var+"\n\n")
        
        # f.write("\tdef set_id(self, id):\n")
        # f.write("\t\tself._id = id\n\n")
        # Write setter methods
        for var in schema[i]:
            f.write("\tdef set_"+var+"(self, "+var+"):\n")
            f.write("\t\tself._"+var+" = "+var+"\n\n")
    f.close()

def createBackendAPI(app_name, auth, schema, secret, prefix, custom_routes):
    print("Creating "+app_name+"...")
    try:
        os.mkdir(app_name)
        print("Creating Models...")
        createModels(app_name=app_name, schema=schema)
        print("Creating Endpoints...")
        createEndpoints(app_name, auth, schema, secret, prefix, custom_routes)
    except OSError as errors:
        print(errors)

def create_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to badB file to create APIs")
    args = parser.parse_args()

    file_path = args.file

    try: 
        file = open(file_path)
        data = json.load(file)
        keys = []
        for i in data.items():
            keys.append(i[0])
        app_name = data["name"] if keys.__contains__('name') else "example_app"
        auth_config = data["auth_config"] if keys.__contains__('auth_config') else None
        schema = data["schema"] if keys.__contains__('schema') else None
        secret = data["secret"] if keys.__contains__('secret') else None
        prefix = data["prefix"] if keys.__contains__('prefix') else None
        custom_routes = data["custom_routes"] if keys.__contains__('custom_routes') else None
        # Closing file
        file.close()

        createBackendAPI(app_name, auth_config, schema, secret, prefix, custom_routes)
    except KeyError as err:
        print("Error opening file : " + err)

def init():
    askQuestion()
