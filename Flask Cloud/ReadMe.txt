Source : https://rest-apis-flask.teclado.com/docs/first_rest_api/project_overview/

Create a virtual environment and activate it.

python3.10 -m venv .venv
source .venv/bin/activate

Install Flask.

pip install flask

Create a file for the Flask app (I like to call it app.py) Create the Flask app.

app.py
from flask import Flask

app = Flask(__name__)

Now you can run this app using the Flask Command-Line Interface (CLI):

flask run

We can use Flask to define dynamic endpoints for our routes, and then we can grab the value that the client put inside the URL.

This allows us to make URLs that make interacting with them more natural.

For example, it's nicer to make an item by going to POST /store/My Store/item, rather than going to POST /add-item and then pass in the store name in the JSON body.

To create a dynamic endpoint for our route, we do this:

@app.route("/store/<string:name>/item")

That makes it so the route function will use a name parameter whose value will be what the client put in that part of the URL.

How to run Linux containers on Windows or MacOS?
When you use Docker Desktop (which I'll show you in the next lecture), it runs a Linux Virtual Machine for you, which then is used to run your Linux containers.

But aren't you then doing this?

hardware -> macos -> hypervisor -> linux vm -> docker -> container -> container program

This is a Dockerfile, a definition of how to create a Docker image. Once you have this file, you can ask Docker to create the Docker image. Then, after creating the Docker image, you can ask Docker to run it as a container.

Dockerfile ---build--> docker image ---run--> docker container

Create your Docker image
Next, download the REST API code from Section 3. You can download it here.

If you want to use the code you wrote while following the videos, that's fine! Just make sure it works by running the Flask app locally and testing it with Insomnia REST Client or Postman.

Write the Dockerfile
In your project folder (i.e. the same folder as app.py), we're going to write the Dockerfile.

To do this, make a file called Dockerfile.

Open a terminal (in VSCode that's CMD+J or CTRL+J), and run this command:

docker build -t rest-apis-flask-python .

Run the Docker container
When we start a Docker container from this image, it will run the flask run command. Remember that by default, flask run starts a Flask app using port 5000.

But the container's ports are not accessible from outside the container by default. We need to tell Docker that when we access a certain port in our computer, those requests and responses should be forwarded to a certain port in our container.

So we'll run the container, but we must remember to forward a port (e.g. 5000) in our computer to port 5000 in the container

To do so, run this command:

docker run -d -p 5000:5000 rest-apis-flask-python

In-depth Docker Tutorial
Like I mentioned earlier on in this section, this course is not a Docker course!

You can access the official Docker tutorial (which is free and great) by running the tutorial image:

docker run -dp 80:80 docker/getting-started


Then build the image into a new container (the . below refers to the current directory, where Docker should find the Dockerfile). Optionally tag it:

docker build -t docker-image-tag .

How to run Docker as a daemon (background)
This prints out the container ID and runs it in the background.

docker run -d docker-image-tag

How to map ports from host machine to Docker container
This binds port 5000 of the Docker image to port 3000 of the host machine. This way you when you access 127.0.0.1:3000 with your browser, you'll access whatever the Docker image is serving in port 5000.

Docs: https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose

docker run -p 127.0.0.1:3000:5000 docker-image-tag

How to map a Named Volume from host to Docker container
docker run -v volume-name:/path/in/docker/image container-tag

For example for an app that needs port mapping and a volume:

docker run -dp 3000:3000 -v todo-db:/etc/todos getting-started

And to see where in the host machine the data is actually stored:

docker volume inspect volume-name

While running in Docker Desktop, the Docker commands are actually running inside a small VM on your machine. If you wanted to look at the actual contents of the Mountpoint directory, you would need to first get inside of the VM.

How to use a Bind Mount to provide your app code to a Docker container
docker run -dp 3000:3000 \
    -w /app -v "$(pwd):/app" \
    node:12-alpine \
    sh -c "apk add --no-cache python2 g++ make && yarn install && yarn run dev"

How to pass environment variables to a container
Use the -e ENV_NAME=env_value flag with docker run.

Networking between two containers
First create a network with:

docker network create network-name

Then pass the --network network-name flag to docker run.

You can also pass --network-alias to docker run to give the container you are running a DNS name within the network.

Then create your containers and pass the network to them. For example, this starts up a MySQL image on linux/amd64. It also creates a volume and passes in two environment variables which the image uses for configuring MySQL:

docker run -d \
    --network network-name --network-alias mysql --platform linux/amd64 \
    -v todo-mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password \
    -e MYSQL_DATABASE=todos \
    mysql:5.7

Then you could run another container on the same network:

docker run -dp 3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network network-name \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD_FILE=/run/secrets/mysql_password \
  -e MYSQL_DB=todos \
  node:12-alpine \
  sh -c "npm install && npm run dev"

How to run multiple containers using Docker Compose
Create a docker-compose.yml file in the root of your project.
Turn each of the docker run commands into a service in the docker-compose.yml file.
This is re-creating the flags passed to the docker run command, but in YAML format.
Example of the two docker runs above:

services:
  app:
    image: node:12-alpine
    command: sh -c "npm install && npm run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD_FILE: /run/secrets/mysql_password
      MYSQL_DB: todos
  mysql:
    image: mysql:5.7
    platform: linux/amd64
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/mysql_root_password
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:



