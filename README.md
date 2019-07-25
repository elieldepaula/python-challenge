# Python Challenge Project

The purpose of this project is to demonstrate some of my Python development skills. Includes a JSON-RPC API, which performs some actions for Docker management.

The project was developed in Python 2.7, using Flask on the back end, and a [very] simple front end, developed with Bootstrap and Jquery, just to trigger actions on the back end. Front end is not my specialty.

You will be able to create, start and stop your docker containers directly from the browser.

And yes, I had a lot of fun developing this project ;)

# Requirements

1. Ubuntu-like linux operating system.
2. Docker 19.03.0.
3. Python 2.7
4. PIP 9.0.1
5. Some patience skills.

# Instructions

1. Install the Docker SDK for python with the command:
```py
pip install docker
```

2. Install Flask Framework with the command:
```py
pip install flask
```

3. Clone the project on your computer.
```
git clone https://github.com/elieldepaula/python-challenge.git
```

4. Access the project folder.
```
cd python-cgallenge
```

5. Run Flask.
```
flask run
```

6. Log in to your browser: http://localhost:5000

You should have a result like this :)

![](./preview.png?raw=true)