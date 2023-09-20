import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from azure.servicebus import ServiceBusClient, ServiceBusMessage

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.secret_key = app.config.get('SECRET_KEY')

# Initialize ServiceBusClient
servicebus_client = ServiceBusClient.from_connection_string(app.config.get('SERVICE_BUS_CONNECTION_STRING'))

# Removed old QueueClient code as we are now using ServiceBusClient
#queue_client = QueueClient.from_connection_string(app.config.get('SERVICE_BUS_CONNECTION_STRING'),
#                                                 app.config.get('SERVICE_BUS_QUEUE_NAME'))

db = SQLAlchemy(app)

from . import routes  # assuming this import is supposed to be here; make sure this is what you intend

# Later in your code, when you're ready to send messages
# you'd use the following code snippet:

# with servicebus_client:
#    sender = servicebus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))
#    with sender:
#        sender.send_messages([ServiceBusMessage("Your Message Here")])
