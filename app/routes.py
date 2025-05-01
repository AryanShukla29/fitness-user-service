import os
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

routes = Blueprint('routes', __name__)

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["fitness"]
user_collection = db["users"]

@routes.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    user_collection.insert_one(data)
    return jsonify({"message": "User created"}), 201

@routes.route("/users", methods=["GET"])
def get_users():
    users = list(user_collection.find({}, {"_id": 0}))  # hide _id field
    return jsonify(users), 200
