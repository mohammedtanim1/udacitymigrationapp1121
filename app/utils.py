# utils.py
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from flask import current_app as app

servicebus_client = ServiceBusClient.from_connection_string(app.config.get('SERVICE_BUS_CONNECTION_STRING'))

def send_message_to_service_bus(message_content):
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))
        with sender:
            sender.send_messages([ServiceBusMessage(message_content)])
