# tools- write_file,read_file,list_files,remove_file,create_folder

import os
import subprocess as sb


def write_file(path, filename: str, content: str):
    """Create or overwrite a file with *content*.

    Parameters
    ----------
    path : str
        Directory path where the file will be stored.  If the directory does
        not exist it will be created.
    filename : str 
    
        Name of the file, including its extension. 
    
    content : str
        Text to write into the file.

    Returns
    -------
    str
        Success message or error description.
    """
    try:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write(content)
        return "File written successfully"
    except Exception as e:
        return f"Something went wrong: {e}"


def read_file(path: str):
    """Read the entire content of *path*.

    Returns
    -------
    str | Exception
        File contents or an error message.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Something went wrong {e}"


def run_command(command: str):
    """execute a shell command and return its output.

    Parameters
    ----------
    command : str
        The shell command to run.

    Returns
    -------
    dict
        Contains ``stdout``, ``stderr`` and ``returncode``.

    Raises
    ------
    RuntimeError
        If the command fails to execute.
    """
    permission = input(f"Do you want to run this command:{command} (y/N) ")
    if permission.lower() != "y" or permission != "":
        return
    print(f"Running: {command}\n")
    try:
        result = sb.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to run command '{command}': {e}")
