import requests
import statistics
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HeadHunter:
    def __init__(self, email, password, query):
        self.email = email
        self.password = password
        self.query = query

    def login(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://hh.ru/')

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@data-qa='expand-login-by-password']")))

        expand_button = self.driver.find_element(By.XPATH, ("//button[@data-qa='expand-login-by-password']"))
        expand_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))

        email_input = self.driver.find_element(By.XPATH, ("//input[@name='username']"))
        email_input.send_keys(self.email)

        password_input = self.driver.find_element(By.XPATH, ("//input[@type='password']"))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

    def search_jobs(self, area_id=1):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": self.query,
            "area": area_id,
            "only_with_salary": "true",
        }
        response = requests.get(url, params=params)
        return response.json()

    def extract_salaries(self, vacancies):
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

    def median_salary(self, salaries):
        return statistics.median(salaries) if salaries else None

    def save_to_csv(self, salaries, filename):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Salary'])
            for salary in salaries:
                csv_writer.writerow([salary])

    def run(self, csv_file):
        self.login()
        search_results = self.search_jobs()
        salaries = self.extract_salaries(search_results["items"])
        median = self.median_salary(salaries)

        if median:
            print(f"The median salary is: {median}")
        else:
            print("No salary data available")

        self.save_to_csv(salaries, csv_file)
        self.driver.quit()


if __name__ == "__main__":
    hh = HeadHunter("youremail@mickeymouse.com", "yourpassword", "Java Developer")
    hh.run("salaries.csv")
