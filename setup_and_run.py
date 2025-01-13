import os
import sys
import platform
import subprocess

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

def user_preferance_picker(promt: str, err_msg: str) -> int:
    user_choice = int(input(promt))

    if user_choice != 1 or user_choice != 2:
        print(err_msg)
        user_preferance_picker()
    
    return user_choice

def get_options() -> dict:
    m = user_preferance_picker(
        "Please dictate how to run the code, [1] for running on this machine and [2] for docker.",
        "Please enter either [1] or [2] without brackets and nothing else.")
    
    s = user_preferance_picker(
        "Please select which functionalities to run; [1] for server only (Message Queue), and [2] for both server and the example microservices.",
        "Please enter either [1] or [2] without brackets and nothing else.")


    return {"machine preferance": m, "server preferance": s}

def run_docker():
    if is_docker_installed() == False:
        print("Please install docker first and re-run the script. Download using sudo on linux or install and setup docker desktop for windows.")
        quit()

    print("docker build -t interview-mq-image .")
    print("docker run -d -p 8000:8000 --name interviewmq-instance interview-mq-image")
    

def linux_setup(option) -> dict:
    ...

def windows_setup(option):
    machine = option["machine preferance"]
    if machine == 1:
        run_docker()
    elif machine == 2:
        sys.run("uvicorn InterviewMQ.Queue:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("Something went wrong.")

if __name__ == "__main__":
    os_name = platform.system()
    option = get_options()

    if os_name == "Windows":
        windows_setup(option)
    elif os_name == "Linux":
        linux_setup(option)
    else:
        print("This platform is not supported. Please select either linux or windows or manualy setup.")