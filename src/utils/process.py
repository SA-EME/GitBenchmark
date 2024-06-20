import subprocess

def execute_command(command: str) -> str:
    """
    Execute a command and return the output.
    """
    try:
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8').strip()