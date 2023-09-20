import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    try:
        # Get connection to database
        conn = psycopg2.connect(host="azurepostgressql1121.postgres.database.azure.com", 
                                dbname="techconfdb"
                                user="azurepostgres@azurepostgressql1121", 
                                password="Tanim1990")
        cursor = conn.cursor()

        # Get notification message and subject from database using the notification_id
        cursor.execute("SELECT subject, message FROM notifications WHERE id=%s", (notification_id,))
        subject, message = cursor.fetchone()

        # Get attendees email and name
        cursor.execute("SELECT email, first_name FROM attendees")
        attendees = cursor.fetchall()

        # Initialize SendGrid API client
        #sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

        # Loop through each attendee and send an email with a personalized subject
        for email, first_name in attendees:
            personalized_subject = subject.replace("{first_name}", first_name)
            mail = Mail(
                from_email=os.getenv("SENDER_EMAIL"),
                to_emails=email,
                subject=personalized_subject,
                html_content=message
            )
            ##sendgrid_client.send(mail)

        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute(
            "UPDATE notifications SET status=%s, completed_date=%s, attendees_notified=%s WHERE id=%s", 
            ('Completed', datetime.utcnow(), len(attendees), notification_id)
        )
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn:
            cursor.close()
            conn.close()
