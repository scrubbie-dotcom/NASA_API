from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import os  # Import os module
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI()

# CORS setup
origins = ["*"]  # Update with your allowed origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to your Remote MongoDB database
client = MongoClient(os.environ.get("MONGO_URI"))  # Use environment variable
db = client["space_pod_db"]  # Replace with your database name
collection = db["planets"]   # Replace with your collection name

# GridFS setup for handling large binary files (if needed)
fs = gridfs.GridFS(db)

@app.get('/planets')
def get_all_planets():
    """Retrieve details of all planets."""
    planets = []
    for planet in collection.find():
        planet["_id"] = str(planet["_id"])  # Convert MongoDB ObjectId to string
        planets.append(planet)
    return planets

@app.get('/planet/{planet_id}')
def get_planet_by_id(planet_id: str):
    """Retrieve a specific planet's details by its _id."""
    try:
        planet = collection.find_one({"_id": ObjectId(planet_id)})
        if planet:
            planet["_id"] = str(planet["_id"])  # Convert ObjectId to string
            return planet
        else:
            return {"error": "Planet not found"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/planet/name/{planet_name}')
def get_planet_by_name(planet_name: str):
    """Retrieve a specific planet's details by its name."""
    planet = collection.find_one({"Planet_Name": planet_name})
    if planet:
        planet["_id"] = str(planet["_id"])  # Convert ObjectId to string
        return planet
    else:
        return {"error": "Planet not found"}

# If needed for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
