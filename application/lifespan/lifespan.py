from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up: Initializing the database")
        await init_db()  # Initialize the database
        print("Database initialization completed")
        load_dotenv("/.env")
        yield  # Control is handed over to the app
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    finally:
        print("Shutting down: Perform cleanup if necessary")
