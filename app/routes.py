import docker, json
from flask import abort, jsonify, make_response, request, render_template
from app import app

client = docker.from_env() # docker.DockerClient(base_url='unix://var/run/docker.sock')

# Render the website template.
@app.route('/')
@app.route('/index')
def index():
    return  render_template('index.html')

# Return a list of all available images.
@app.route('/api/images', methods=['GET'])
def get_images():

    # client = docker.from_env()

    image_list = []
    for image in client.images.list():
        image_list.append(image.attrs)
    
    return jsonify(
        {
            "images":image_list
        }
    )

# Return a list of containers. [ok]
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

    # client = docker.from_env()
    container = client.containers.run(request.json['image_name'], detach=True)

    return  jsonify(
        {
            "id":container.id,
            "name":container.name
        }
    )

@app.route('/api/start', methods=['POST'])
def start_container():
    if not request.json:
        return make_response(
            jsonify(
                {
                    "error":"No request!"
                }
            ), 
            400)

    # temp_container = client.containers.get(request.json['name'])
    # if temp_container:
    #     container = client.containers.run(request.json['name'])
    #     return jsonify(
    #         {
    #             "Name":"Starting " + request.json['name']
    #         }
    #     )
    # else:
    #     container = client.containers.run(request.json['name'])
    #     return jsonify(
    #         {
    #             "error":"Error starting container"
    #         }
    #     )

    temp_out = []
    try:
        container = client.containers.run(request.json['name'])
        temp_out = [{
            "name":"Starting " + request.json['name']
        }]
        
    except Exception as e:
        # print str(e) # for error in e.
        temp_out = [{
            "name":"Error starting container "
        }]
    else:
        return jsonify(temp_out)
    

@app.route('/api/<string:container_name>/stop', methods=['GET'])
def stop_container(container_name):
    temp_container = client.containers.get(container_name)
    temp_container.stop()
    return jsonify(
        {
            "Name":"Stopping " + container_name
        }
    )

@app.route('/api/stop/all', methods=['GET'])
def stop_all():
    
    # client = docker.from_env()
    for container in client.containers.list():
        container.stop()

    return jsonify(
        {
            "msg":"Stoping all containers."
        }
    )

# Return client info [ok]
@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify(client.info())

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

