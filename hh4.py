import requests
import statistics
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, EMAIL, PASSWORD):
    # Navigate to hh.ru
    driver.get('https://hh.ru')
    
    # Find and click the login button
    login_button = driver.find_element(By.XPATH, "//a[@data-qa='login']")
    login_button.click()
    
    # Expand button to enter the password
    expand_button = driver.find_element(By.XPATH, "//button[@data-qa='expand-login-by-password']")
    expand_button.click()

    # Wait for the email input field to be present and visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='login-input-password']"))
    )

    # Enter the email address and password
    email_input = driver.find_element(By.NAME, 'username')
    email_input.send_keys(EMAIL)
    email_input.send_keys(Keys.TAB)

    password_input = driver.find_element(By.XPATH, "//input[@data-qa='login-input-password']")
    password_input.send_keys(PASSWORD)
    password_input.submit()

    # Wait for the email input field to be present and visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='account-login-submit']"))
    )

# Search for jobs with the provided query and area_id
def search_jobs(query, area_id=1):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": query,
        "area": area_id,
        "only_with_salary": "true",
    }
    response = requests.get(url, params=params)
    return response.json()

# Extract salaries from the list of vacancies
def extract_salaries(vacancies):
    salaries = []
    for vacancy in vacancies:
        salary = vacancy["salary"]
        if salary is not None and salary["from"] is not None and salary["to"] is not None:
            salary_from = salary["from"]
            salary_to = salary["to"]
            if salary_from and salary_to:
                average_salary = (salary_from + salary_to) / 2
                salaries.append(average_salary)
    return salaries

# Calculate the median salary from a list of salaries
def median_salary(salaries):
    return statistics.median(salaries) if salaries else None

# Save salaries to a CSV file
def save_to_csv(salaries, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Salary'])
        for salary in salaries:
            csv_writer.writerow([salary])



# Define your email, password, search query, and CSV filename
EMAIL = 'your email'
PASSWORD = 'password'
SEARCH_QUERY = 'Atlassian Engineer'
CSV_FILE = 'salaries.csv'

# Initialize the WebDriver and login to hh.ru
driver = webdriver.Chrome()
login(driver, EMAIL, PASSWORD)

# Close the WebDriver
driver.quit()

# Search for jobs using the provided search query
search_results = search_jobs(SEARCH_QUERY)

# Extract salary data from the search results
salaries = extract_salaries(search_results["items"])

# Calculate the median salary
median = median_salary(salaries)

# Print the median salary or a message if no salary data is available
if median:
    print(f"The median salary is: {median}")
else:
    print("No salary data available")

# Save the salary data to a CSV file
save_to_csv(salaries, CSV_FILE)
