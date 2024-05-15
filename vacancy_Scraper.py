from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import csv
import pdfkit


def get_soup(driver):
    """Extract the HTML with BeautifulSoup"""
    return BeautifulSoup(driver.page_source, 'html.parser')


def find_vacancies(driver, wait):
    """Find all vacancies on the page and click on the next button"""
    vacancies = []
    while True:
        sleep(1)
        soup = get_soup(driver)
        vacancies.extend(soup.find_all('div', class_='preview'))
        try:
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Дальше")]')))
            next_button.click()
        except:
            break
    return vacancies


def export_vacancies(vacancies, driver):
    """Parse and export the vacancies to a csv and txt file"""
    with open('vacancies.csv', 'w', newline='', encoding='utf-8') as csvfile, \
            open('vacancies.txt', 'w', encoding='utf-8') as txtfile:
        writer = csv.writer(csvfile)
        # Write the header of csv file
        writer.writerow(["Id", "Timestamp", "Title", "Company", "Salary", "Vacancy Description", "Link", "Email"])

        for id_num, vacancy in enumerate(vacancies, start=1):
            # Parsing vacancy details
            title, company, salary, link, description, email = parse_vacancy_details(vacancy, driver)

            # Write the row in csv file
            writer.writerow(
                [id_num, datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), title, company, salary, description, link,
                 email])

            # Write the information in text file
            write_txt_file(txtfile, id_num, title, company, salary, link, email, description)


def parse_vacancy_details(vacancy, driver):
    """Parse the details of a single vacancy"""
    rabota_md_url = 'https://www.rabota.md'
    title = vacancy.find('a', class_='vacancy-title').text.strip()
    href = vacancy.find('a', class_='vacancy-title')['href']
    link = rabota_md_url + href if 'https' not in href else href.replace(rabota_md_url, '')
    company = get_text(vacancy.find('a', class_='font-semibold'), 'Not Provided')
    salary = get_text(vacancy.find('span', class_='salary-negotiable'), 'Not Provided')

    # Open the vacancy link and get the description and emails
    driver.get(link)
    soup_link = get_soup(driver)
    description = get_text(soup_link.find('div', class_='preview'), 'Not Provided')
    email = get_emails(soup_link)
    return title, company, salary, link, description, email


def get_text(element, default_text='Not Provided'):
    """Get text from an element if it's not None else return a default text"""
    return element.text.strip() if element is not None else default_text


def get_emails(soup):
    """Extract email addresses from the vacancy page"""
    mailto_links = soup.find_all('a', href=True)
    emails = []
    for email_link in mailto_links:
        if email_link['href'].startswith('mailto:'):
            emails.append(email_link.text.strip())
    emails = [email for email in emails if 'rabota@rabota.md' not in email]
    return 'Not Provided' if len(emails) == 0 else emails[0]


def write_txt_file(txtfile, id_num, title, company, salary, link, email, description):
    """Write the details of a vacancy to a txt file"""
    txtfile.write(
        f'Id: {id_num}\nTimestamp: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n'
        f'Title: {title}\nCompany: {company}\nSalary: {salary}\n'
        f'Vacancy Description:\n{description}\nLink: {link}\nEmail: {email}\n' + '-' * 100 + '\n')
    print(
        f'Id: {id_num}\nTimestamp: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n'
        f'Title: {title}\nCompany: {company}\nSalary: {salary}\n'
        # f'Vacancy Description:\n{description}\n'
        f'Link: {link}\nEmail: {email}\n' + '-' * 100)


def get_vacancies(keyword):
    """Main function to scrape vacancies for a keyword and export details"""
    rabota_md_url = 'https://www.rabota.md'
    keyword_path_format = '/ru/jobs-moldova-{}'
    url = rabota_md_url + keyword_path_format.format(keyword)

    options = Options()
    options.add_argument("--headless")  # Running in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 1)
    vacancies = find_vacancies(driver, wait)
    print(f"Total count of vacancies: {len(vacancies)}")

    # Parse and export vacancies
    export_vacancies(vacancies, driver)
    driver.quit()

    # Convert TXT file to PDF
    pdfkit.from_file('vacancies.txt', 'vacancies.pdf',
                     configuration=pdfkit.configuration(
                         wkhtmltopdf=r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'),
                     options={'encoding': 'UTF-8'})


if __name__ == '__main__':
    get_vacancies('Your vacancy')