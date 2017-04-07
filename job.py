import requests
from bs4 import BeautifulSoup
import codecs
import re
URL = 'https://www.indeed.com/jobs?q=software+engineer&l=Chicago%2C+IL&jt=internship'


class Details(object):
    def __init__(self,name,company,link,review,description):
        self.name = name
        self.company = company
        self.link = link
        self.review = review
        self.description = description

    def tostring(self):
        return str(self.review) + "reviews " + self.name+" " + self.company


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    job_list_soup = soup.find('td', attrs={'id': 'resultsCol'})
    job_name_list = []
    job_link_list = []
    company_name_list = []
    reviews_count_list = []
    job_description_list = []
    count= 0
    for job_li in job_list_soup.find_all('div', class_=re.compile('(.*)row(.+)result')):
        count += 1
        job_name_shell = job_li.find('a', attrs={'data-tn-element': 'jobTitle'})
        job_name = job_name_shell['title']
        job_link = URL + job_name_shell['href']
        name_tmp = job_li.find('span', attrs={'class': 'company'})
        company_name = ''
        for string in name_tmp.stripped_strings:
            company_name += string
        reviews_count = job_li.find('span', attrs={'class': 'slNoUnderline'})
        if reviews_count is None:
            reviews_count = 0
        else:
            reviews_count = int(re.sub('[^0-9,]',"",reviews_count.string).replace(',', ''))
        description = job_li.find('span', attrs={'class': 'summary'})
        job_description = ''
        for string in description.stripped_strings:
            job_description += string
        job_name_list.append(job_name)
        job_link_list.append(job_link)
        company_name_list.append(company_name)
        reviews_count_list.append(reviews_count)
        job_description_list.append(job_description)
    print('contains '+str(count)+' records in this page')
    url_list = soup.find('div', attrs={'class': 'pagination'}).find_all('span', attrs={'class': 'np'})
    for url in url_list:
        if url.string == 'Next »':
            return job_name_list, company_name_list, job_link_list, reviews_count_list, job_description_list, 'https://www.indeed.com' + url.parent.parent['href']
    return job_name_list, company_name_list, job_link_list, reviews_count_list, job_description_list, None


def main():
    url = URL
    job_list = []
    company_list = []
    link_list = []
    review_list = []
    des_list = []

    while url:
        job, company, link, review, description, url = parse_html(download_page(url))
        job_list += job
        company_list += company
        link_list += link
        review_list += review
        des_list += description
    container = set()
    result = []
    for index,x in enumerate(job_list):
        if x in container:
            pass
        else:
            result.append(Details(job_list[index],company_list[index],link_list[index],review_list[index],des_list[index]))
            container.add(x)

    result.sort(key=lambda y: y.review,reverse=True)
    for x in result:
        print(result.tostring())
    #with codecs.open('intern_jobs_indeed.Chicago', 'wb', encoding='utf-8') as fp:
    #    for x in result:
    #        fp.writelines("%s \n" % x.tostring())
    print('finished!')


if __name__ == '__main__':
    main()