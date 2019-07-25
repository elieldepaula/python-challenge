
# Python dev challenge!
# Created by Eliel de Paula <dev@elieldepaula.com.br>

import docker, json
from flask import abort, jsonify, make_response, request, render_template
from app import app

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# Render the website template.
@app.route('/')
@app.route('/index')
def index():
    return  render_template('index.html')

# Return a list of all available images.
@app.route('/api/images', methods=['GET'])
def get_images():
    image_list = []
    for image in client.images.list():
        image_list.append(image.attrs)
    return jsonify(
        {
            "images":image_list
        }
    )

# Return a list of containers.
@app.route('/api/list', methods=['GET'])
def get_containers():
    out_containers = []
    temp_containers = []
    for container in client.containers.list(all=True):
        temp_container = {
            "id":container.id,
            "name":container.name,
            "status":container.status
        }
        out_containers.append(temp_container)
    return  jsonify(
        {
            "containers":out_containers
        }
    )

# Create a new container.
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
    temp_out = []
    try:
        container = client.containers.run(request.json['image_name'], detach=True)
        container.start()
        temp_out = [{
            "id":container.id,
            "name":container.name
        }]
    except:
        temp_out = [{
            "name":"Error creating container "
        }]
    else:
        return jsonify(temp_out)

# Start a single container.
@app.route('/api/<string:container_name>/start', methods=['GET'])
def start_container(container_name):
    temp_out = []
    try:
        temp_container = client.containers.get(container_name)
        temp_container.start()
        temp_out = [{
            "name":"Starting " + container_name
        }]
    except Exception as e:
        temp_out = [{
            "name":"Error starting container "
        }]
    else:
        return jsonify(temp_out)
    
# Stop a single running container.
@app.route('/api/<string:container_name>/stop', methods=['GET'])
def stop_container(container_name):
    temp_container = client.containers.get(container_name)
    temp_container.stop()
    return jsonify(
        {
            "Name":"Stopping " + container_name
        }
    )

# Stop all running containers.
@app.route('/api/stop/all', methods=['GET'])
def stop_all():
    for container in client.containers.list():
        container.stop()
    return jsonify(
        {
            "msg":"Stoping all containers."
        }
    )

# Return docker client info.
@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify(client.info())

# Handle routes error.
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

