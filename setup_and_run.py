import os
import sys

def get_option():
    result = str(input("Please dictate how to run the code, [1] for running on this machine and [2] for docker."))
    if result != "1" or result != "2":
        print("Please enter either [1] or [2] without brackets and nothing else.")
        get_option()
    return result


if __name__ == "__main__":
    option = get_option()

    if option == "1":
        ...
    elif option == "2":
        sys.run("uvicorn InterviewMQ.Queue:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("Something went wrong.")