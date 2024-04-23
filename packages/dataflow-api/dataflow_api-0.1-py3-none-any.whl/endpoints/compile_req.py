"""API for compiling requirements."""
import os
import sys

from fastapi import APIRouter, Body,HTTPException
from piptools.scripts.compile import cli
from utils.logger import CustomLogger



class CompileRouter:
    """
    Router class for handling the Compile Requirements API endpoint.
    """

    def __init__(self):
        """
        Initializes the CompileRouter instance.
        """
        self.router = APIRouter()
        self.logger = CustomLogger().get_logger()


    def configure_routes(self):
        """
        Configures API routes.
        """

        @self.router.post("/compile")
        async def compile_requirements(requirements_in: str = Body(...)):
            """
            Compile requirements from input.

            Args:
                requirements_in (str): Input requirements.

            Returns:
                str: Compiled requirements.
            """

            try:
                with open("compile.in", "w",encoding="utf-8") as f:
                    f.write(requirements_in)

                sys.stdout = open(os.devnull, 'w', encoding="utf-8")
                sys.stderr = open(os.devnull, 'w', encoding="utf-8")
                args = [
                    "compile.in",
                    "--output-file", "compile.txt",
                ]

                cli.main(args)

            except SystemExit as err:
                # Check the exit code
                if err.code == 0:
                    with open("compile.txt", "r",encoding="utf-8") as f:
                        compiled_requirements = f.readlines()

                    # Filter out comments and docstrings
                    compiled_requirements = [
                        line.strip() for line in compiled_requirements
                        if not line.strip().startswith("#") and "#" not in line.strip()
                    ]

                    # Join the filtered lines into a single string
                    compiled_requirements_str = "\n".join(compiled_requirements)

                    return compiled_requirements_str

                raise HTTPException(status_code=500, detail="Error compiling requirements")

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error compiling requirements: {str(err)}")

# Instantiate the router object
compile_requirement_router = CompileRouter()
# Configure the routes
compile_requirement_router.configure_routes()
# Get the router object
router = compile_requirement_router.router
