# backend/app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
from contextlib import asynccontextmanager


# Import our new service functions
from . import services
from .core.config import IMAGE_DIR


# --- LIFESPAN MANAGEMENT ---
# This is the modern way in FastAPI to handle startup and shutdown logic.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs on startup
    print("API starting up...")
    # You can add more startup logic here if needed
    yield
    # Code here runs on shutdown
    print("API shutting down...")
    services.close_connections()  # Properly close Weaviate connection


# Create the FastAPI app instance with the lifespan manager
app = FastAPI(title="StyleSeeker API", lifespan=lifespan)

# --- NEW: ADD THE CORS MIDDLEWARE ---
# This is the "welcome" sign for our security guard.
origins = [
    "http://localhost:5173",  # The address of our React frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from the origins list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# --- END OF NEW PART ---
# This is the new part. It tells FastAPI that any request starting with /images
# should be served from the 'data/images' directory on our computer.
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# --- API ENDPOINTS ---


@app.get("/")
def read_root():
    """
    A simple health check endpoint.
    """
    return {
        "message": "Welcome to the StyleSeeker API!",
        "image_directory_exists": IMAGE_DIR.exists(),
        "weaviate_connected": services.weaviate_client is not None,
        "model_loaded": services.model is not None,
    }


@app.post("/search/")
async def search_by_image(file: UploadFile = File(...)):
    """
    Accepts an image upload and returns a list of similar products.
    """
    if not services.model or not services.weaviate_client:
        raise HTTPException(status_code=503, detail="Service not available. Model or DB not loaded.")

    try:
        # 1. Read the uploaded image file into memory
        image_bytes = await file.read()
        query_image = Image.open(io.BytesIO(image_bytes))

        # 2. Find similar images using our service
        results = services.find_similar_images(query_image)

        # 3. Return the results
        return {"results": results}

    except Exception as e:
        # This will catch errors during image processing or searching
        print(f"An error occurred during search: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image and perform search.")
