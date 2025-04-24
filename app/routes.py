from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import pika
import json
import os

routes = Blueprint('routes', __name__)

# MongoDB Connection
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["fitness"]
user_collection = db["users"]

# Routes

@routes.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user_id = user_collection.insert_one(data).inserted_id

    # Send message to RabbitMQ
    message = {
        "event": "user_created",
        "user": data
    }

    try:
        rabbitmq_uri = os.environ.get("RABBITMQ_URI", "amqp://guest:guest@rabbitmq:5672/")
        params = pika.URLParameters(rabbitmq_uri)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue="user_created")
        channel.basic_publish(
            exchange='',
            routing_key='user_created',
            body=json.dumps(message)
        )
        connection.close()
    except Exception as e:
        print("Error publishing message to RabbitMQ:", e)

    return jsonify({"message": "User created", "user_id": str(user_id)}), 201


@routes.route("/users", methods=["GET"])
def get_users():
    users = list(user_collection.find({}, {"_id": 0}))
    return jsonify(users), 200
