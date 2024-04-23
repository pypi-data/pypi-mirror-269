"""API for compiling requirements."""
import os
import sys
import venv
import shutil

from pip._internal import main as pip_main
from fastapi import APIRouter, Depends
from piptools.scripts.compile import cli
from sqlalchemy.orm import Session

from utils.logger import CustomLogger
from schemas import environment
from models import environment as m_environment
from models.database import Database



class PipCompileRouter:
    """
    Router class for handling the Compile Requirements API endpoint.
    """


    def __init__(self):
        """
        Initializes the CompileRouter instance.
        """
        self.router = APIRouter()
        self.db_con = Database()
        self.logger = CustomLogger().get_logger()


    def get_db(self):
        """
        Dependency function to get a database session.

        Returns:
            Session: SQLAlchemy database session.
        """

        session = self.db_con.create_sessionlocal()
        db = session()
        try:
            yield db
        finally:
            db.close()


    def create_virtualenv(self):
        """
        Create a virtual environment for compiling requirements.
        """

        venv.create("temp", with_pip=True)


    def install_requirements(self):
        """
        Install requirements in the virtual environment.
        """

        activate_path = os.path.join("temp", "bin", "activate") if sys.platform != 'win32' else os.path.join("temp", "Scripts", "activate")
        activate_cmd = f"source {activate_path}"
        os.system(f"{activate_cmd}")


    def delete_virtualenv(self):
        """
        Delete the virtual environment.
        """

        venv_dir = "temp"

        try:
            if os.path.exists(venv_dir):
                shutil.rmtree(venv_dir)
                self.logger.info("Virtual environment deleted successfully.")
            else:
                self.logger.warning("Virtual environment not found.")

        except Exception as e:
            self.logger.error("Failed to delete virtual environment")


    def configure_routes(self):
        """
        Configures API routes.
        """

        @self.router.post("/pip_compile")
        async def compile_requirements(request: environment.Compile,db: Session=Depends(self.get_db)):

            """
            Compile requirements from input.

            Args:
                image_id (int): Image Id
                requirements_in (str): Input requirements.

            Returns:
                str: Compiled requirements.
            """
            image_id=request.image_id
            requirements_in=request.requirements_in

            success=False
            error=[]
            warning=[]

            try:
                self.create_virtualenv()

                query = db.query(m_environment.Environment)
                query_requirement = query.filter(m_environment.Environment.id==image_id).all()
                exist_requirements=query_requirement[0].py_requirements

                with open("pipcompile.in", "w",encoding="utf-8") as f:
                    if exist_requirements!="NULL":
                        requirements_in=requirements_in+"\n"+exist_requirements+"\n"
                    f.write(requirements_in)

                with open('pipcompile.in', 'r',encoding="utf-8") as file:
                    lines = file.readlines()
                    unique_lines = set(lines)

                    if len(lines)!=len(unique_lines):
                        warn="Duplicate requirements"
                        self.logger.warning(warn)
                        warning.append(warn)

                with open('pipcompile.in', 'w',encoding="utf-8") as file:
                    req_str="\n".join(unique_lines)
                    file.writelines(req_str)

                args = [
                    "--dry-run",
                    "pipcompile.in"
                ]

                sys.stdout = open(os.devnull, 'w', encoding="utf-8")
                sys.stderr = open(os.devnull, 'w', encoding="utf-8")

                cli.main(args)


            except SystemExit as e:
                # Check the exit code
                if e.code == 0:
                    self.logger.info("Compiled Successfully")
                    success=True

                else:
                    err="Error compiling requirements"

                    self.logger.error(err)
                    error.append(err)

            except Exception as e:
                if str(e)=="metadata generation failed":
                    err="pip subprocess to install build dependencies exited with 1"
                    self.logger.error(err)
                    error.append(err)

                elif str(e)=="ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts" :
                    err="Resolution Impossible dealing with dependency conflict"
                    self.logger.error(err)
                    error.append(err)

                elif str(e)=='list index out of range' :
                    err="Invalid Image Id"
                    self.logger.error(err)
                    error.append(err)

                elif "(from line 1 of pipcompile.in)" in str(e) :
                    err=str(e).replace('(from line 1 of pipcompile.in)','')
                    self.logger.error(err)
                    error.append(err)

                else:
                    self.logger.error(str(e))
                    error.append(str(e))

            try:
                self.delete_virtualenv()

            except Exception as e:
                self.logger.exception(str(e))

            return {"success":success,"error":error,"warning":warning}


# Instantiate the router object
pip_compile_requirement_router = PipCompileRouter()
# Configure the routes
pip_compile_requirement_router.configure_routes()
# Get the router object
router = pip_compile_requirement_router.router
