# Importing Required Libraries
import os
from dotenv import load_dotenv
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')


class SendEmail:
    # Constructor
    def __init__(self, email_user, email_password):
        self.email_user = email_user
        self.email_password = email_password
        self.email_subject = input('Please enter the email subject: ')
        with open('body.txt', 'r', encoding='utf-8') as file:
            self.body = file.read()

    # Function to send email
    def _send_email(self, email_body, file_names, receiver_email):
        logging.info('Preparing email for: %s', receiver_email)
        msg = MIMEMultipart()
        msg['From'] = "FirstName LastName <{}>".format(self.email_user)
        msg['To'] = receiver_email
        msg['Subject'] = self.email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        # Attaching files
        for file in file_names:
            logging.info('Attaching file: %s', file)
            attachment = open(file, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + file)
            msg.attach(part)

        text = msg.as_string()

        # SMTP server setup and sending email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_user, self.email_password)

        logging.info('Sending email to: %s', receiver_email)
        server.sendmail(self.email_user, receiver_email, text)
        server.quit()
        logging.info('Email sent to: %s', receiver_email)

    # Function to read csv file and send emails
    def read_csv_file(self, file_name, ids):
        files_to_send = ["Cover_Letter.pdf", "CV.pdf"]
        with open(file_name, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Id'] in ids:
                    self._send_email(self.body, files_to_send, row['Email'])


# Main Function
def main():
    load_dotenv()
    email_sender = SendEmail(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
    user_ids = input('Please input the ids separated by comma: ')
    user_ids_list = user_ids.split(',')
    logging.info('Script started.')
    email_sender.read_csv_file('vacancies.csv', user_ids_list)
    logging.info('Script finished.')


if __name__ == '__main__':
    main()
