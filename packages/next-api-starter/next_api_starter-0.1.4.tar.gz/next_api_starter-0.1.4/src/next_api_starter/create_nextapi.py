import os
import subprocess
import argparse
import shutil
import time
from venv import EnvBuilder
from alembic import command
from alembic.config import Config
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


# def initialize_alembic(service_dir):
#     """
#     Initialize Alembic for a service.

#     Args:
#         service_dir (str): Path to a service directory.
#     """
#     current_dir = os.path.abspath(os.getcwd())
#     service_dir = os.path.abspath(service_dir)
#     os.chdir(service_dir)
#     try:
#         subprocess.run(["alembic", "init", "alembic"], check=True)
#         env_file = os.path.join(service_dir, "alembic", "env.py")

#         # Wait for file system updates to take effect
#         timeout = 10  # Timeout in seconds
#         start_time = time.time()
#         while not os.path.exists(env_file):
#             if time.time() - start_time > timeout:
#                 raise TimeoutError("Timeout: env.py file not found.")
#             time.sleep(1)

#         # Update env.py with correct target metadata
#         with open(env_file, "r") as file:
#             env_contents = file.read()
#         env_contents = env_contents.replace("target_metadata = None", "target_metadata = models.Base.metadata")
#         env_contents = "from app import models\n" + env_contents
#         with open(env_file, "w") as file:
#             file.write(env_contents)

#         print("Alembic initialized successfully.")

#     except Exception as e:
#         print(f"Error initializing Alembic: {e}")
#     finally:
#         os.chdir(current_dir)


def setup_alembic(service_dir,database_uri):
    shutil.rmtree('alembic', ignore_errors=True)
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', f'{service_dir}/alembic')  # Update with your actual script location
    alembic_cfg.set_main_option('sqlalchemy.url', database_uri)

    alembic_cfg.config_file_name = f"{service_dir}/alembic.ini"
    # Initialize Alembic with the provided configuration object
    command.init(config=alembic_cfg, directory=f'{service_dir}/alembic')
    env_file = f'{service_dir}/alembic/env.py'
    with open(env_file, "r") as file:
        env_contents = file.read()
        env_contents = env_contents.replace("target_metadata = None", "target_metadata = models.Base.metadata")
        env_contents = "from app import models\n" + env_contents
        with open(env_file, "w") as file:
            file.write(env_contents)
    
    if os.path.exists(alembic_cfg.config_file_name):
        with open(alembic_cfg.config_file_name, "r") as file:
            filedata = file.read()

        # Replace {service_name} placeholder with actual service name
        filedata = filedata.replace("sqlalchemy.url = driver://user:pass@localhost/dbname", f"sqlalchemy.url = {database_uri}")

        with open(alembic_cfg.config_file_name, "w") as file:
            file.write(filedata)
    
    

    create_database(database_uri=database_uri)
    # Generate and apply the initial migration
    command.revision(config=alembic_cfg, autogenerate=True, message='Initial migration')
    command.upgrade(config=alembic_cfg, revision='head')


def create_database(database_uri):
    try:
        # Extract database name and password from URI
        username, password, host, database_name = extract_database_details(database_uri)

        # Create engine to connect to the PostgreSQL server
        engine = create_engine(database_uri)

        # Attempt to connect to the engine
        try:
            engine.connect()
        except OperationalError:
            # If connection fails, it means the database doesn't exist
            print(f"Database '{database_name}' does not exist. Creating...")
            
            # Construct the psql command with secure password handling
            command = f"psql -h {host} -U {username} -c \"CREATE DATABASE {database_name}\""

            # Execute the psql command with error handling
            try:
                subprocess.run(command, check=True, shell=True, env={'PGPASSWORD': password})
                print(f"Database '{database_name}' created successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error creating database '{database_name}': {e}")
            return

        # If the database already exists
        print(f"Database '{database_name}' already exists.")
        
    except Exception as e:
        print(f"Error: {e}")

def extract_database_details(database_uri):
    # Remove the "postgresql://" prefix
    uri_without_prefix = database_uri.replace("postgresql://", "")
    print(uri_without_prefix)
    
    # Split the remaining URI at the "@" symbol

    user_password_and_host, database_name = uri_without_prefix.split("@")
    
    
    # Split the user, password, and host

    username, password = user_password_and_host.split(":")
    
    host , database_name = database_name.split("/")
        
        # password, host = password_and_host.split("@")
    
    return username, password, host, database_name
def create_backend_structure(backend_dir):
    """
    Create the backend directory structure and files based on a template.

    Args:
        backend_dir (str): Path to the backend directory.
    """
    try:
        while True:
            service_name = input("Please enter the name of the service (do not include 'service' in the name): ").strip().lower()
            print("I need some info for creating the database.Each microservice shall have there own separate database, but if you want to use the same database for multiple microservce that is also fine. I will be setting up your postgresql database.")
            user_name = input("Please enter the username: ")
            password = input("Please enter the password: ")
            host = input("Please enter the host address: ")
            database_name = input("Please enter the database name")
            
            DATA_BASE_URI = f"postgresql://{user_name}:{password}@{host}/{database_name}"
            
            
            
            
            if not service_name:
                print("Service name cannot be empty. Please try again.")
                continue

            service_dir = os.path.join(backend_dir, f"{service_name}-service")

            if os.path.exists(service_dir):
                print(f"The service '{service_name}' already exists. Please choose a different name.")
                continue

            shutil.copytree(TEMPLATE_DIR, service_dir)
            replace_placeholder(service_dir=service_dir, service_name=service_name + '-service', database_uri = DATA_BASE_URI)
            setup_alembic(service_dir=service_dir,database_uri=DATA_BASE_URI)
            
            # create_virtualenv(service_dir)
            
            # requirements_file = os.path.join(service_dir, "requirements.txt")
            # if os.path.exists(requirements_file):
            #     install_dependencies(service_dir=service_dir)

            print(f"{service_name} successfully created")

            inp = input("Do you want to add more services? (y/n): ").strip().lower()
            if inp != "y":
                break

    except Exception as e:
        print(f"Error creating the backend: {e}")


def replace_placeholder(service_dir, service_name, database_uri):
    """
    Replace placeholders in main.py and database.py with actual service name and database URI.

    Args:
        service_dir (str): Path to the service directory.
        service_name (str): Name of the service.
        database_uri (str): Database URI.
    """
    main_py_path = os.path.join(service_dir,"app", "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as file:
            filedata = file.read()

        # Replace {service_name} placeholder with actual service name
        filedata = filedata.replace("{service_name}", service_name)

        with open(main_py_path, "w") as file:
            file.write(filedata)
            
    database_py_path = os.path.join(service_dir,"app", "database.py")
    print(database_py_path)
    
    if os.path.exists(database_py_path):
        with open(database_py_path, "r") as file:
            database_filedata = file.read()
            
        print(database_filedata)

        # Replace placeholder SQLALCHEMY_DATABASE_URL = "example_db" with actual database URI
        database_filedata = database_filedata.replace('SQLALCHEMY_DATABASE_URL = "example_db"', f'SQLALCHEMY_DATABASE_URL = "{database_uri}"')

        with open(database_py_path, "w") as file:
            file.write(database_filedata)
            
    else:
        print("file not found")


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
