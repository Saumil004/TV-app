import subprocess

def run_command():
    command = "cd ~ && cd Desktop && cd tv-program && source project/bin/activate && python3 app.py"
    subprocess.run(command, shell=True, executable="/bin/bash")

if __name__ == "__main__":
    run_command()

