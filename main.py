from bs4 import BeautifulSoup
import requests

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
                print(f'Company Name: {company_name}')
                print(f'Required Skills: {skills}')
                print(f'Link: {link}')
                print('')  # Add Empty Line
