import os
import boto3
from utils import *
from flask import Flask, request

app = Flask(__name__)

DEVICE_TABLE = os.environ['USERS_TABLE']
client = boto3.client('dynamodb')


@app.route("/api/health", methods=["GET"])
def check_health():
    return buildResponse(200)
    

@app.route("/api/devices/<string:device_id>")
def get_device(device_id):
    try:
        response = client.get_item(
            TableName=DEVICE_TABLE,
            Key={
                'id': { 'S': device_id }
                }
                )
        if "Item" in response:
            return buildResponse(200, response["Item"])
        else:
            return buildResponse(404, {"Message": "HTTP 404 Not Found"})
    except:
        return buildResponse(500, {"Message": "HTTP 500 Internal Server Error"})


@app.route("/api/devices", methods=["POST"])
def create_user():
    try:
        id = request.json.get('id')
        name = request.json.get('name')
        serial = request.json.get('serial')
        note = request.json.get('note')
        deviceModel = request.json.get('deviceModel')
        if not id or not name or not serial or not note or not deviceModel:
            return buildResponse(404, {"Message": "HTTP 400 Bad Request, missing field"})
        client.put_item(
            TableName=DEVICE_TABLE,
            Item={
                'id': {'S': id },
                'name': {'S': name },
                'note': {'S': note},
                'serial':{'S', serial},
                'deviceModel': {'S', deviceModel}
            }
            )
        return buildResponse(201, {"Message": "HTTP 201 Created"})
    except:
        return buildResponse(500, {"Message": "HTTP 500 Internal Server Error"})