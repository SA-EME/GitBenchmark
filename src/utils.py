import subprocess

def execute_command(command: str) -> str:
    """
    Execute a command and return the output.
    """
    process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.decode('utf-8').strip()