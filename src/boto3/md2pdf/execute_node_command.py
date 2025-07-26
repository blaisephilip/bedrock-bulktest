import subprocess

def execute_node_command(command):
    """
    Executes a Node.js command using subprocess.
    
    Args:
        command (str): The Node.js command to execute.
    
    Returns:
        tuple: A tuple containing the return code, standard output, and standard error.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr
    except FileNotFoundError:
        return 1, "", "Error: Node.js not found. Please ensure Node.js is installed and in your system's PATH."
