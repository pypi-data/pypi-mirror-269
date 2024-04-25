import os
import subprocess
import argparse
import sqlalchemy
import alembic
def update_database(service_dir):
    """
    Update the database schema for a service

    Args:
        service_dir (str): Path to the service directory
    """
    
    currrent_dir = os.path.abspath(os.getcwd())
    try:
        os.chdir(service_dir)
        # alembic_ini = os.path.join(service_dir,"alembic.ini")
        
        # if not os.path.exists(alembic_ini):
        #     print(f"No Alembic configuration found for {service_dir}")
            
        #     return
        
        subprocess.run(['alembic', 'revision', "--autogenerate", "-m", "Updating database schema"])
        
        subprocess.run(["alembic","upgrade", "head"])
    except sqlalchemy.exc.NoSuchModuleError:
        print("Please edit the sqlalchemy.url = driver://user:pass@localhost/dbname in your alembic.ini file")
    finally:
        os.chdir(currrent_dir)
    
    
    
def update_all_services(backened_dir):
    """
    Update the database schema for all services in the backened directory

    Args:
        backened_dir (str): Path to backened directory.
    """
    
    backened_dir = os.path.join(backened_dir, "backend")
    
    for service_name in os.listdir(backened_dir):
        service_dir = os.path.join(backened_dir, service_name)
        if os.path.isdir(service_dir):
            models_py = os.path.join(service_dir,"app", "models.py")
            
            if os.path.exists(models_py):
                print(f'Updating database for {service_name}...')
                update_database(service_dir)
                
            else:
                print(f"No models.py found for {service_name}")
                
def main():
    parser = argparse.ArgumentParser(description="Update NextAPI Project")
    parser.add_argument("project_name", help="Name of the new NextAPI project")
    args = parser.parse_args()

    update_all_services(args.project_name)


if __name__ == "__main__":
    main()
