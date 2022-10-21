"""
Script that can grab a company's glassdoor review pages with high accuracy.
it can determine when a link is not entirely accurate and can add a flag so
we can go back and check.
input files:
    .csv containing all company names
    "secret.json" containing glassdoor login information:
        {
            "username": "USERNAME",
            "password": "PASSWORD"
        }
Outputs a .csv with headers:
    "Company Name", "Link", "Flag"
To run the file:
    python3 glassdoor_link_scrapper.py --file <path_to_csv> --secret_file <path_to_secret.json>
"""


import csv
import json
import time

import click
from selenium import webdriver as wd
from selenium.webdriver.common.by import By


@click.command()
@click.option(
    "--file",
    prompt="Path to file",
    help="Path to file",
)
@click.command()
@click.option(
    "--secret_file",
    prompt="Path to secret.json file",
    help="Path to secret.json file",
)
def get_browser():

    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1200")
    browser = wd.Chrome("/usr/local/bin/chromedriver", options=chrome_options)
    return browser


def sign_in(browser, username, password):
    url = "https://www.glassdoor.ca/index.htm"
    browser.get(url)
    print("At Homepage")
    signin_field = browser.find_element(
        By.XPATH,
        ".//button[@type='button'][@class='d-none d-lg-block p-0 LockedHomeHeaderStyles__signInButton']",
    )
    browser.execute_script("arguments[0].click();", signin_field)
    time.sleep(2)
    email_field = browser.find_element(By.NAME, "username")

    password_field = browser.find_element(By.NAME, "password")
    submit_btn = browser.find_element(By.NAME, "submit")

    email_field.send_keys(username)

    password_field.send_keys(password)
    time.sleep(1)
    print("Signing in now")
    submit_btn.click()

    time.sleep(3)


def go_to_companies_page(browser):
    url = "https://www.glassdoor.ca/member/home/companies.htm"
    browser.get(url)
    print("At Companies homepage now")


def get_link(company_name, browser):
    search_field = browser.find_element(By.XPATH, '//*[@id="sc.keyword"]')
    search_btn = browser.find_element(By.XPATH, '//*[@id="scBar"]/div/button')
    search_field.clear()
    search_field.send_keys(company_name)
    time.sleep(3)
    search_btn.click()
    time.sleep(3)
    print("Searching Company: " + str(company_name))
    check = " No"
    try:
        if "Reviews" in browser.current_url:
            print("More than 1 result for company: " + str(company_name))
            print("Finding first result...")
            company_cell = browser.find_element(
                By.XPATH, '//*[@id="MainCol"]/div/div[1]/div/div[1]/div/div[2]/h2/a'
            )
            company_path = company_cell.get_attribute("href")
            browser.get(company_path)
            check = " Yes"
            time.sleep(3)

        if "Overview" in browser.current_url:
            print("At Homepage for: " + str(company_name))
            print("Navigating to reviews...")
            reviews_cell = browser.find_element(By.XPATH, '//a[@data-label="Reviews"]')
            reviews_path = reviews_cell.get_attribute("href")
            browser.get(reviews_path)
            print("Done" + str(company_name))
            return browser.current_url, check
    except Exception:
        print("Company not found : " + str(company_name))
        print("Adding flag...")
        check = " Yes"
        return "Not Found", check

    print("No Results for" + str(company_name))
    print("Adding flag...")
    check = " Yes"
    return "Not Found", check


def main(file, secret_file):

    browser = get_browser()

    with open(file) as f:
        reader = csv.reader(f)
        data = list(reader)

    with open(secret_file) as f:
        d = json.loads(f.read())
        username = d["username"]
        password = d["password"]

    sign_in(browser, username, password)

    go_to_companies_page(browser)

    ls = []

    for company in data:

        link, flag = get_link(company)
        row = [company, link, flag]
        ls.append(row)

    header = ["Company Name", "Link", "Flag"]

    with open("output.csv", "w") as f:
        write = csv.writer(f)
        write.writerow(header)
        write.writerows(ls)


if __name__ == "__main__":
    main()