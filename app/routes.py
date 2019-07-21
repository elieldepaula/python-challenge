import docker, json
from flask import abort, jsonify, make_response, request
from app import app


containers = [

]

@app.route('/')
def index():
    return  jsonify(
        {
            "msg":"Docker dashboard API."
        }
    )

# Return a list of all available images.
@app.route('/api/images', methods=['GET'])
def get_images():

    client = docker.from_env()

    image_list = []
    for image in client.images.list():
        image_list.append(image.attrs)
    
    return jsonify(
        {
            "images":image_list
        }
    )

# Return alist of all running containers.
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

    client = docker.from_env()
    container = client.containers.run(request.json['image_name'], detach=True)

    return  jsonify(
        {
            "id":container.id,
            "name":container.name
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

@app.route('/api/stop/all', methods=['GET'])
def stop_all():
    
    client = docker.from_env()
    for container in client.containers.list():
        container.stop()

    return jsonify(
        {
            "msg":"Stoping all containers."
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

