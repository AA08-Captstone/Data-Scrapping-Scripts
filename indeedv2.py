"""
python3 indeedv2.py --job_titles /Users/danielkhan/CODE/CAPSTONE/input/titles.csv --lim 10
"""


import os
import csv
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import click
import time
import pandas as pd

def get_browser():
    chrome_options = wd.ChromeOptions()
    #chrome_options.add_argument("log-level=3")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1200")
    browser = wd.Chrome("/usr/local/bin/chromedriver", options=chrome_options)
    return browser

def search_job_title(browser, title, location):
    url = "https://ca.indeed.com/"
    browser.get(url)
    print(f"At Homepage of {url}")
    print(f"Searching for '{title}' jobs")
    search_field = browser.find_element(
        By.XPATH,
        '//*[@id="text-input-what"]',
    )
    search_field.send_keys(title)
    browser.find_element(By.XPATH,'//*[@id="text-input-where"]').send_keys([Keys.BACKSPACE] * 1000)
    location_field = browser.find_element(By.XPATH,'//*[@id="text-input-where"]')
    location_field.send_keys(location)
    time.sleep(2)
    
    search_button = browser.find_element(By.XPATH, '//*[@id="jobsearch"]/button')
    browser.execute_script("arguments[0].click();", search_button)
    return browser.current_url

def check_popup(browser):
    try:
        popup = browser.find_element(By.XPATH,'//*[@id="mosaic-modal-mosaic-provider-desktopserp-jobalert-popup"]/div/div/div[1]')
        Xbutton = browser.find_element(By.XPATH,'//*[@id="mosaic-modal-mosaic-provider-desktopserp-jobalert-popup"]/div/div/div[1]/div/button').click()
        print("Found Popup, closing it now")
        time.sleep(2)
    except Exception:
        print("No Popup")
        

@click.command()
@click.option("--job_titles",prompt="Path to file",help="Path to file")
#@click.option("--lim",prompt="Number of Postings",help="Number of Postings",type=click.INT)
def main(job_titles):#,lim):
    browser = get_browser()

    raw_data = pd.DataFrame(columns = ['title', 'comapny', 'location','desc','link'])
    job_titles_data = pd.read_csv(job_titles)

    """
    with open(job_titles) as f:
        reader = csv.reader(f)
        job_titles_data = list(reader)
    """
    for title in job_titles_data:
        url=search_job_title(browser,title,"Canada")
        i=1
        while True:
            try:
                card = browser.find_element(By.XPATH,f'//*[@id="mosaic-provider-jobcards"]/ul/li[{i}]')
                card.click()
                time.sleep(2)
                check_popup(browser)
                # get job title
                try:
                    job_title = browser.find_element(By.XPATH,'//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/h2').text
                    print("found title")
                except Exception:
                    print("No title found")
                    job_title = "No Title"
                # get job location
                try:
                    job_location = card.find_element(By.CLASS_NAME,'companyLocation').text
                    print("found location")
                except Exception:
                    print("No location found")
                    job_location = "No Location"
                # get company
                try:
                    job_company = card.find_element(By.CLASS_NAME,'companyName').text
                    print("found company name")
                except Exception:
                    print("No company name found")
                    job_company = "No Company Name"
                # get job desc
                try:
                    job_desc = browser.find_element(By.XPATH,'//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]').text
                    print("found desc")
                except Exception:
                    print("No Description found")  
                    job_desc = "No Description"              
                # get job date?   
                raw_data = raw_data.append({'title' : job_title, 'company' : job_company, 'location' : job_location, 'desc': job_desc ,'link': browser.current_url }, 
                ignore_index = True)
                i+=1
                print(f"Scrapping card {i}")
            except Exception:
                print("No more Jobs?")
                break
        print(f"Collected {i} jobs, moving on")
        time.sleep(3)
    print("Done Collect, saving now ")
    raw_data.to_excel("../output/output.xlsx")

    """
    with open('../output/links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for link in raw_data:
            writer.writerow([link])
    """


if __name__ == "__main__":
    main()