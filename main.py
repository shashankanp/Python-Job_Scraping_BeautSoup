from bs4 import BeautifulSoup
import requests
import time

print("Enter Unfamiliar Skills: ")
unfam_skills = list(map(str, input('>>').split()))
print(f'Filtering out {unfam_skills}')
print('\n'*2)


def find_jobs():
    html_texts = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_texts, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in jobs:
        published_date = job.find('span', class_='sim-posted').text.split()[1]
        if ((published_date.isnumeric() and int(published_date) < 3) or ('today' in published_date) or ('few' in published_date)):
            # Checks if date is < 3 days or if its contains the word 'few' or 'today'
            # print(published_date)
            company_name = job.find(
                'h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.replace(' ',
                                                                        '').replace(',', ', ').strip().title()
            link = job.h2.a["href"]

            if not any(skill in skills for skill in unfam_skills):
                # Only gives back results if the "unfamiliar skills" are Missing
                with open(f'Data/{company_name}.txt', 'w') as f:
                    f.write(f'Company Name: {company_name}\n')
                    f.write(f'Required Skills: {skills}\n')
                    f.write(f'Link: {link}\n')
                print(f'File Saved: {company_name}')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)  # Sets a timer of 10 minutes
