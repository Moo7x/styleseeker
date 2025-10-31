# backend/app/services.py

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import weaviate
from .core.config import IMAGE_DIR  # Import our settings

# --- 1. GLOBAL VARIABLES & MODEL LOADING ---

# We load the model and other heavy objects only once when the application starts.
# This is much more efficient than loading them for every API request.
try:
    print("Loading CLIP model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name).to(device)
    processor = CLIPProcessor.from_pretrained(model_name)
    print("CLIP model loaded successfully.")
except Exception as e:
    print(f"Error loading CLIP model: {e}")
    model = None
    processor = None

# Weaviate client setup
try:
    print("Connecting to Weaviate...")
    weaviate_client = weaviate.connect_to_local()
    collection_name = "StyleSeekerImage"
    style_seeker_collection = weaviate_client.collections.get(collection_name)
    print("Connected to Weaviate successfully.")
except Exception as e:
    print(f"Error connecting to Weaviate: {e}")
    weaviate_client = None
    style_seeker_collection = None


# --- 2. THE EMBEDDING FUNCTION ---


def get_image_embedding(image: Image.Image) -> list[float]:
    """
    Takes a PIL Image, processes it, and returns its vector embedding.
    Note: The input is now a PIL Image object, not a file path.
    """
    if not model or not processor:
        raise RuntimeError("Model is not loaded.")

    image = image.convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        embedding = model.get_image_features(**inputs)

    embedding /= embedding.norm(dim=-1, keepdim=True)
    return embedding.cpu().numpy().tolist()[0]


# --- 3. THE SEARCH FUNCTION ---


def find_similar_images(image: Image.Image, top_k: int = 5) -> list[dict]:
    """
    Finds similar images in the Weaviate database.
    """
    if not style_seeker_collection:
        raise RuntimeError("Weaviate collection is not available.")

    # 1. Get the embedding for the query image
    query_vector = get_image_embedding(image)

    # 2. Perform the search
    response = style_seeker_collection.query.near_vector(near_vector=query_vector, limit=top_k)

    # 3. Format and return the results
    results = []
    for item in response.objects:
        # We construct a full UcaRL or path to the image for the frontend
        # For now, we'll just return the image ID (filename)
        image_id = item.properties["image_path"].split("/")[-1]
        results.append({"id": image_id, "product_name": item.properties["product_name"]})

    return results


# --- 4. CLEANUP FUNCTION ---
# This is good practice to include in case we need to close connections.
def close_connections():
    if weaviate_client:
        weaviate_client.close()
        print("Weaviate connection closed.")
