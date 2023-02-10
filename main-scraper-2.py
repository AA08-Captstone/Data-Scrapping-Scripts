# Sourced from: https://www.scraperapi.com/blog/linkedin-scraper-python/
# Returns a .csv file with the job title, company, location, and link to apply

import csv
import requests
from bs4 import BeautifulSoup

file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Seniority', 'Employment Type', 'Apply'])

def linkedin_scraper(webpage, page_number):
  next_page = webpage + str(page_number)
  print(str(next_page))
  response = requests.get(str(next_page))
  soup = BeautifulSoup(response.content,'html.parser')

  jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
  for job in jobs:
    job_title = job.find('h3', class_='base-search-card__title').text.strip()
    job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
    job_location = job.find('span', class_='job-search-card__location').text.strip()
    job_link = job.find('a', class_='base-card__full-link')['href']

    writer.writerow([
    job_title.encode('utf-8'),
    job_company.encode('utf-8'),
    job_location.encode('utf-8'),
    job_link.encode('utf-8')
    ])

  # job_cards = soup.find_all('section',{"class" : "core-section-container my-3 description"})
  # for card in job_cards:
  #   job_seniority = card.find_all('span', class_="description__job-criteria-text description__job-criteria-text--criteria")
  #   job_employment_type = card.find_all('span', class_='description__job-criteria-text description__job-criteria-text--criteria').text.strip()

  #   writer.writerow([
  #   job_seniority.encode('utf-8'),
  #   job_employment_type.encode('utf-8'),
  #   ])
    
  print('Data updated')

  if page_number < 10:
    page_number = page_number + 1
    linkedin_scraper(webpage, page_number)
  else:
    file.close()
    print('File closed')

linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=data%20analyst&location=canada&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=software%20engineer&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Sales&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Graphic%20Designer&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Marketing%20Specialist&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Sales%20Management&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Sales%20Executive&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Software%20Development&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Structural%20Engineering&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Business%20Analysis&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Project%20Management&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Sales%20Engineer&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Database%20Administration&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)
# linkedin_scraper('https://www.linkedin.com/jobs/search?keywords=Data%20Specialist&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', 0)