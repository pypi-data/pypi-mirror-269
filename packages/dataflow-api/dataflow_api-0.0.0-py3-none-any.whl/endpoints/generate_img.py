"""Dummy Api for generate Image"""
from fastapi import APIRouter



class GenerateImageRouter:
    """
    Router class for handling the Hello World API endpoint.
    """


    def __init__(self):
        """
        Initializes the GenerateImageRouter instance.
        """

        self.router = APIRouter()


    def configure_routes(self):
        """
        Configures API routes.
        """

        @self.router.get("/generate")
        async def generate_image():
            """
            FastAPI endpoint to generate image.
            """

            return {"message": "Generated Image"}


# Instantiate the router object
generate_image_router = GenerateImageRouter()
# Configure the routes
generate_image_router.configure_routes()
# Get the router object
router = generate_image_router.router
