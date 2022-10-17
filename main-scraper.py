import time
from pandas import pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(r'C:\Users\popco\Downloads\Setups\chromedriver.exe')
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)
driver.get('https://www.linkedin.com')
time.sleep(2)

#locate and accept cookies
driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div/section/div/div[2]/button[2]").click()

# Reading txt file where we have our user credentials
with open('user_credentials.txt', 'r',encoding="utf-8") as file:
  user_credentials = file.readlines()
  user_credentials = [line.rstrip() for line in user_credentials]
  user_name = user_credentials[0] # First line
  password = user_credentials[1] # Second line
  driver.find_element(By.XPATH, '//[@id="username"]').send_keys(user_name)
  driver.find_element(By.XPATH, '//[@id="password"]').send_keys(password)
  time.sleep(1)

#Login button
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Access to the Jobs button and click it
driver.find_element(By.XPATH, '‘//*[@id=”ember19"]’').click()
time.sleep(3)

#Find search results via link
driver.get("https://www.linkedin.com/search/results/all/?keywords=data%20analyst&origin=GLOBAL_SEARCH_HEADER&sid=l4!")
time.sleep(1)

#Find job blocks via the left sidebar job list
jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search-results__list')
jobs_list = driver.find_element(By.CSS_SELECTOR, '.jobs-search-results__list-item')

#Loop through the job list
for job in jobs_list:
    all_links = job.find_element(By.TAG_NAME, 'a')
    for a in all_links:
      if str(a.get_attribute('href')).startsWith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links:
        links.append(a.get_attribute('href'))
      else:
        pass

# scroll down for each job element
driver.execute_script("arguments[0].scrollIntoView();", job)

# go to the next page
driver.find_element(By.XPATH, "//button[@aria-label=’Page {enter_page_number_here}’]").click()
time.sleep(3)

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []

i = 0
j = 1
# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(2)

        # Click the 'See More' button
        driver.find_element(By.CLASS_NAME, 'artdeco-card__actions').click()
        time.sleep(2)
    except:
        pass

# Scrape detailed information within the job offer
contents = driver.find_element(By.CLASS_NAME, 'p5')
for content in contents:
  try:
    job_titles.append(content.find_element(By.TAG_NAME, 'h1').text)
    company_names.append(content.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text)
    company_locations.append(content.find_element(By.CLASS_NAME, 'jobs-unified-top-card__bullet').text)
    work_methods.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__workplace-type").text)
    post_dates.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__posted-date").text)
    work_times.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-insight").text)
    print(f'Scraping the Job Offer {j} DONE.')
    j += 1

  except:
    pass
  time.sleep(2)

# Scrape detailed information within the job description
job_description = driver.find_element(By.CLASS_NAME, 'jobs-description__content')
for description in job_description:
  job_text = description.find_element(By.CLASS_NAME, 'jobs-box__html-content').text
  job_desc.append(job_text)
  print(f'Scraping the Job Description {j} DONE.')
  time.sleep(2)

#Create the dataframe
df = pd.DataFrame(list(zip(job_titles, company_names, company_locations, work_methods, post_dates, work_times)),
columns = ['Job Title', 'Company Name', 'Company Location', 'Work Method', 'Post Date', 'Work Time'])

#Store data into .csv file
df.to_csv('job_offers.csv', index=False)

#Output job descriptions to .txt file
with open('job_descriptions.txt', 'w', encoding="utf-8") as f:
  for line in job_desc:
    f.write(line)
    f.write('\n')