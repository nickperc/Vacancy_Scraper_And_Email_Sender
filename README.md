# Vacancy Scraper and Email Sender

This project consists of two Python scripts:

1. A **Vacancy Scraper** that uses Selenium and BeautifulSoup to scrape job postings from a website, save them to a CSV file and a text file, and then transform the text file to a PDF.

2. An **Email Sender** that reads the previously created CSV file, and sends an email to the addresses found there with specific attachments.

## Dependencies

This project needs the following Python libraries:
- bs4 (BeautifulSoup)
- selenium
- csv
- pdfkit
- datetime
- smtplib
- email
- logging

You can install these with pip using the command:
```bash
pip install beautifulsoup4 selenium pdfkit
```
## Setting Up
### Environment Variables
Sensitive data like email credentials should be kept secure. We will use environment variables for that. 

Here is how you can set it up:
In your local development environment, create a new file named .env in your project root.
Put your sensitive data in this file with each variable on a new line like so:
```bash
EMAIL_USER="your_email@example.com"
EMAIL_PASSWORD="your_password"
```
In your .gitignore file, add .env to avoid pushing up sensitive data to GitHub.
In your Python script, you can access these variables with os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASSWORD').

Please, make sure to use your own email and password.
Running the Scripts
Both Python scripts can be executed with Python3:
```bash
python3 vacancy_Scraper.py
python3 email_Sender.py
```
Remember to run vacancy_Scraper.py before email_Sender.py as the second one depends on the CSV file generated by the first one.
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.