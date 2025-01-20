import os
import sys
import subprocess

should_install = input("Should requirements be installed? ('Yes' or 'No'): ")

if should_install == "Yes":
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

import platform
import docker 
import time
import signal

import docker.errors

OPEN_TERMINALS = []

def build_image(client, image_name, dockerfile_path="."):
    print(f"Building Docker image '{image_name}'...")
    client.images.build(path=dockerfile_path, tag=image_name)
    print(f"Image '{image_name}' built successfully.")

def ensure_container_exists(client, container_name, image_name, ports):
    try:
        container = client.containers.get(container_name)
        print(f"Container '{container_name}' already exists.")
        return container
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found. Creating it...")
        container = client.containers.run(
            image_name,
            name=container_name,
            ports=ports,
            detach=True
        )
        print(f"Container '{container_name}' created and running.")
        return container

def is_docker_installed():
    try:
        result = subprocess.run(
            ["docker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("Docker is installed.")
            print("Docker Version:", result.stdout.strip())
            return True
        else:
            print("Docker is not installed or not in PATH.")
            print("Error:", result.stderr.strip())
            return False
    except FileNotFoundError:
        print("Docker executable not found in PATH.")
        return False

def get_port(prompt: str, default_port: int) -> int:
    user_input = input(prompt)

    if user_input == "":
        return default_port
    
    user_choice = int(user_input)

    if not isinstance(user_choice, int)  or user_choice > 9999 or user_choice < 1000:
        print("Please enter an integer between 1000-9999")
        get_port(prompt, default_port)

    return user_choice

def user_preferance_picker(prompt: str, err_msg: str) -> int:
    user_choice = int(input(prompt))

    if user_choice != 1 and user_choice != 2:
        print(err_msg)
        user_preferance_picker(prompt, err_msg)
    
    return user_choice

def get_options() -> dict:
    m = user_preferance_picker(
        "Please dictate how to run the code, [1] for running on this machine and [2] for docker. \n",
        "Please enter either [1] or [2] without brackets and nothing else. \n")
    
    s = user_preferance_picker(
        "Please select which functionalities to run: [1] (Reccomended) for both server and the example microservices, and [2] for server only (Message Queue). \n",
        "Please enter either [1] or [2] without brackets and nothing else. \n")

    return {"machine preferance": m, "server preferance": s}

def run_docker():
    if is_docker_installed() == False:
        print("Please install docker first and re-run the script. Download using sudo on linux or install and setup docker desktop for windows.")
        quit()

    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        print("Please make sure docker is running.")
        quit()
        
    image_name = "interview-mq-image"
    container_name = "interviewmq-instance"
    port_mapping = {'8000/tcp': 8000}

    # Check if image exists
    try:
        client.images.remove(image=image_name, force=True)
        print(f"Deleted existing image '{image_name}'.")
    except docker.errors.ImageNotFound:
        print(f"Image '{image_name}' not found. No need to delete.")

    print(f"Building a fresh image '{image_name}'...")
    image, _ = client.images.build(path=".", tag=image_name) #, nocache=True)
    print("Image built successfully.")

    # Check if container exists and remove if running
    try:
        container = client.containers.get(container_name)
        print(f"Container '{container_name}' already exists. Removing...")
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found. Proceeding to run a new container.")

    client.images.prune()
    client.containers.prune()

    # Run the container
    container = client.containers.run(image_name, name=container_name, ports=port_mapping, detach=True)
    print(f"Container '{container_name}' is running.")   

def run_microservice(service_type: str):
    terminal = subprocess.Popen(["start", "cmd", "/c", "python ./examples/" + service_type + "/main.py "], shell=True)
    OPEN_TERMINALS.append(terminal)

def linux_setup(option) -> dict:
    ...

def windows_setup(option):
    machine = option["machine preferance"]
    services = option["server preferance"]
    
    if services == 1:
        if machine == 1:
            server_port = get_port(
            "A new terminal will be opened to run InterviewMQ, enter a port you wish to run or press enter for default 8000: ",
            8000
            )
            command = "uvicorn InterviewMQ:app --host 0.0.0.0 --port " + str(server_port) + " --reload"
            message_queue = subprocess.Popen(["start", "cmd", "/c", command], shell=True)
            OPEN_TERMINALS.append(message_queue)
            time.sleep(1) 
        elif machine == 2:
            server_port = 8000
            run_docker()

        port = get_port(
            "A new terminal will be opened to run frontend, enter a port you wish to run or press enter for default 8080: ",
            8080
            )
        terminal = subprocess.Popen(["start", "cmd", "/c", "python ./examples/Frontend/main.py", str(port), str(server_port)], shell=True)
        OPEN_TERMINALS.append(terminal)

        time.sleep(1)

        input("Lastly backend will run on this terminal, open localhost on your browser to publish a message here, press enter to run backend.")
        print(f"You can visit http://localhost:{port} to view the frontent.")
        subprocess.run(["python", "./examples/Backend/main.py", str(server_port)])
    elif services == 1:
        server_port = get_port(
            "Enter a port you wish to run or press enter for default 8000: ",
            8000
            )
        command = "uvicorn InterviewMQ:app --host 0.0.0.0 --port " + str(server_port) + " --reload"
        subprocess.Popen(["start", "cmd", "/c", command], shell=True)
    

if __name__ == "__main__":
    os_name = platform.system()
    option = get_options()

    if os_name == "Windows":
        windows_setup(option)
    elif os_name == "Linux":
        print("Linux is not supported at the moment, we highy reccomend to run on windows")
    else:
        print("This platform is not supported. Please select either windows or manualy setup.")

    for terminal in OPEN_TERMINALS:
        try:
            os.kill(terminal.pid, signal.SIGTERM)
        except PermissionError:
            print("Please manually close the terminals now.")
            break