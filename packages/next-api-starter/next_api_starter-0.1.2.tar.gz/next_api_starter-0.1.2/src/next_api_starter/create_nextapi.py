import os
import subprocess  # For using shell commands within Python
import argparse
import shutil


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),"template", "backened")

def create_backend_structure(backend_dir):
    """
    Creates the backend directory structure and files based on a template.

    Args:
        backend_dir: Path to the backend directory.
    """
    try:
        # Copy template files and directories to the backend directory
        print(TEMPLATE_DIR)
        shutil.copytree(TEMPLATE_DIR, backend_dir)
        print("Backend structure created successfully.")
    except Exception as e:
        print(f"Error creating the backend: {e}")
    

def create_nextapi_project(project_name):
    
    """
    Creates a new NextAPI project directory structure.

    Args:
        project_name: The desired name for the new project.
    """
    
    # try:
        
    # Create the project directory
    os.makedirs(project_name)

    # # Create the frontend directory using npx
    subprocess.run(["npx", "create-next-app", project_name + "/frontend"], check=True)

    # Optionally create a virtual environment (consider using venv)
    # ... (Add virtual environment creation logic here if desired)

    # Create the backend directory
    backend_dir = os.path.join(project_name, "backend")
    # os.makedirs(backend_dir)

    # Create an empty main.py file for the FastAPI app
    create_backend_structure(backend_dir)

    # Print a success message
    print(f"NextAPI project created successfully: {project_name}")
        
    # except subprocess.CalledProcessError:
    #     print("\033[91mNextAPI project creation canceled by the user\033[0m")  # ANSI escape codes for red color
    #     if os.path.exists(project_name):
    #         shutil.rmtree(project_name)
            
        
    # except Exception as e:
    #     print("Error creating the NextAPI project as : {e}")


def main():
    parser = argparse.ArgumentParser(description="Create a new NextAPI Project")
    parser.add_argument("project_name", help = "Name of the new NextAPI project")
    args = parser.parse_args()
    
    create_nextapi_project(args.project_name)
    
    
if __name__=="__main__":
    main()
