import asyncio
from mlserver.settings import Settings, ModelSettings
from mlserver.server import MLServer
from model import ImgDetection


async def main():
    """Start the MLServer with the image detection model."""
    
    settings = Settings(
        debug=True,
        parallel_workers=0
    )
    
    model_settings = ModelSettings(
        name="img-detection",
        implementation=ImgDetection,
    )
    
    server = MLServer(settings)
    await server.start([model_settings])


def run_server():
    """Entry point for running the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run_server()