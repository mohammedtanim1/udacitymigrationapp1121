import logging
import json
import azure.functions as func
import psycopg2
import os
from datetime import datetime
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):
    notified_counter = 0
    notification_id = None

    try:
        msg_body = msg.get_body().decode('utf-8')
        logging.info("Message: %s", msg)
        cleaned_msg_body = msg_body.replace("Notification#", "")
        notification_id = int(cleaned_msg_body)
    except ValueError:
        print("The message body cannot be converted to an integer.")
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    try:
        # Get connection to database
        conn = psycopg2.connect(host="azurepostgressql1121.postgres.database.azure.com", 
                                dbname="techconfdb",
                                user="azurepostgres@azurepostgressql1121", 
                                password="Tanim1990")
        cursor = conn.cursor()

        # Get notification message and subject from database using the notification_id
        cursor.execute("SELECT subject, message FROM notification WHERE id=%s", (notification_id,))
        subject, message = cursor.fetchone()

        # Get attendees email and name
        cursor.execute("SELECT email FROM attendee")
        attendees = cursor.fetchall()

        # Loop through each attendee and send an email with a personalized subject
        for email in attendees:
            
            # Increment the notified counter
            notified_counter += 1

            # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
            update_status = f'Notified {str(notified_counter)} Attendees'
            cursor.execute(
                "UPDATE notification SET status=%s, completed_date=%s WHERE id=%s", 
                (update_status, datetime.utcnow(), notification_id)
            )
            
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn:
            cursor.close()
            conn.close()
