import os
import subprocess
import argparse
import shutil
import time
from venv import EnvBuilder

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template", "backend")

def create_virtualenv(service_dir):
    """
    Create a virtual environment in the specified directory

    Args:
        venv_dir (str): Path to the virtual environment
    """
    orignial_dir = os.path.abspath(os.getcwd())
    print(service_dir)
    os.chdir(service_dir)
    
    # os.mkdir(venv_dir)
    subprocess.run(["python","-m","venv","venv"], check=True)
    os.chdir(orignial_dir)

def install_dependencies(service_dir):
    """
    Install dependencies from a requirements file into the virtual environment.

    Args:
        venv_dir (str): Path to the virtual environment directory.
        requirements_file (str): Path to the requirements file.
    """
    
    # original_dir = os.path.abspath(os.getcwd())

    subprocess.run(["/bin/bash", "-c", "source deactivate"])
    subprocess.run(["/bin/bash", "-c", f"source {service_dir}/venv/bin/activate"])

    
    subprocess.run([f"{service_dir}/venv/bin/pip","install","-r",f"{service_dir}/requirements.txt"])
    
    subprocess.run(["/bin/bash", "-c", "source deactivate"])



def print_directory_tree(directory):
    """
    Print the complete directory tree.

    Args:
        directory (str): Path to the directory.
    """
    directory = os.path.abspath(directory)  # Convert to absolute path
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print('{}{}'.format(sub_indent, file))


def initialize_alembic(service_dir):
    """
    Initialize Alembic for a service.

    Args:
        service_dir (str): Path to a service directory.
    """
    current_dir = os.path.abspath(os.getcwd())
    service_dir = os.path.abspath(service_dir)
    os.chdir(service_dir)
    try:
        subprocess.run(["alembic", "init", "alembic"], check=True)
        env_file = os.path.join(service_dir, "alembic", "env.py")

        # Wait for file system updates to take effect
        timeout = 10  # Timeout in seconds
        start_time = time.time()
        while not os.path.exists(env_file):
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout: env.py file not found.")
            time.sleep(1)

        # Update env.py with correct target metadata
        with open(env_file, "r") as file:
            env_contents = file.read()
        env_contents = env_contents.replace("target_metadata = None", "target_metadata = models.Base.metadata")
        env_contents = "from app import models\n" + env_contents
        with open(env_file, "w") as file:
            file.write(env_contents)

        print("Alembic initialized successfully.")

    except Exception as e:
        print(f"Error initializing Alembic: {e}")
    finally:
        os.chdir(current_dir)


def create_backend_structure(backend_dir):
    """
    Create the backend directory structure and files based on a template.

    Args:
        backend_dir (str): Path to the backend directory.
    """
    try:
        while True:
            service_name = input("Please enter the name of the service (do not include 'service' in the name): ").strip().lower()
            if not service_name:
                print("Service name cannot be empty. Please try again.")
                continue

            service_dir = os.path.join(backend_dir, f"{service_name}-service")

            if os.path.exists(service_dir):
                print(f"The service '{service_name}' already exists. Please choose a different name.")
                continue

            shutil.copytree(TEMPLATE_DIR, service_dir)
            replace_placeholder(service_dir=service_dir, service_name=service_name + '-service')
            initialize_alembic(service_dir)
            
            create_virtualenv(service_dir)
            
            requirements_file = os.path.join(service_dir, "requirements.txt")
            if os.path.exists(requirements_file):
                install_dependencies(service_dir=service_dir)

            print(f"{service_name} successfully created")

            inp = input("Do you want to add more services? (y/n): ").strip().lower()
            if inp != "y":
                break

    except Exception as e:
        print(f"Error creating the backend: {e}")


def replace_placeholder(service_dir, service_name):
    """
    Replace placeholders in main.py with actual service name.

    Args:
        service_dir (str): Path to the service directory.
        service_name (str): Name of the service.
    """
    main_py_path = os.path.join(service_dir, "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as file:
            filedata = file.read()

        # Replace placeholders with service name
        filedata = filedata.replace("{service_name}", service_name)

        with open(main_py_path, "w") as file:
            file.write(filedata)


def create_nextapi_project(project_name):
    """
    Create a new NextAPI project directory structure.

    Args:
        project_name (str): The desired name for the new project.
    """
    try:
        # Create the project directory
        os.makedirs(project_name)

        # Create the backend directory
        backend_dir = os.path.join(project_name, "backend")

        # Create backend structure
        create_backend_structure(backend_dir)

        print(f"NextAPI project created successfully: {project_name}")

    except Exception as e:
        print(f"Error creating the NextAPI project: {e}")


def main():
    parser = argparse.ArgumentParser(description="Create a new NextAPI Project")
    parser.add_argument("project_name", help="Name of the new NextAPI project")
    args = parser.parse_args()

    create_nextapi_project(args.project_name)


if __name__ == "__main__":
    main()
