#!/usr/bin/python
from flask import Flask, abort, jsonify, make_response, request
import docker

app = Flask(__name__)

# client = docker.from_env()
# container = client.containers.run("bfirsh/reticulate-splines", detach=True)

containers = [

]

@app.route('/')
def index():
    return  jsonify(
        {
            "msg":"Docker dashboard API."
        }
    )

@app.route('/api/list', methods=['GET'])
def get_containers():

    client = docker.from_env()

    for container in client.containers.list():
        temp_container = {
            "id":container.id,
            "name":container.name,
            "status":container.status
        }
        containers.append(temp_container)

    return  jsonify(
        {
            "msg":containers
        }
    )

@app.route('/api/new', methods=['POST'])
def new_container():
    if not request.json:
        return make_response(
            jsonify(
                {
                    "error":"No request!"
                }
            ), 
            400)

    return  jsonify(
        {
            "request":request.json
        }
    )

@app.route('/api/start/<string:container_name>', methods=['GET'])
def start_container(container_name):
    return jsonify(
        {
            "Name":"Starting " + container_name
        }
    )

@app.route('/api/stop/<string:container_name>', methods=['GET'])
def stop_container(container_name):
    return jsonify(
        {
            "Name":"Stopping " + container_name
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify(
            {
                "error":"Not found!"
            }
        ), 
        404
    )

if __name__ == '__main__':
    app.run(debug=True)