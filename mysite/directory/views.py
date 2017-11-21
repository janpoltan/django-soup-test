from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Professional, Contact

def index(request):
    return render(request, 'directory/index.html', {'total_profs': Professional.objects.count()})

def scrape(request):
    page = 1
    while (True):
        print("Scraping page %s" % page)
        url = "https://directory.easternuc.com/publicDirectory?page={0}".format(page)
        html = urlopen(url)
        html_text = html.read()
        soup = BeautifulSoup(html_text, 'html.parser') 
        directory_div = soup.find("div", class_="dirctory_design3")
        tag_i = directory_div.find('i')
        if tag_i is None:
            do_scrape(directory_div)
            page = page + 1
        else:
            break
    return render(request, 'directory/scrape.html', {'html': 'Done'})

def do_scrape(directory_div):
    row = directory_div.find_all('tr')
    for r in row:
        d = r.find_all('td')
        profile = d[0]
        phone_contacts = d[1]
        mobile_contacts = d[2]
        email_site = d[3]

        name = profile.h4.get_text()
        profile_more_info = profile.find_all('span')
        position = profile_more_info[0].get_text()
        company = profile_more_info[1].get_text()

        phone_numbers = []
        for c in phone_contacts.find_all('img'):
            phone_numbers.append(c.next_element.string)
        
        mobile_numbers = []
        for c in mobile_contacts.find_all('img'):
            mobile_numbers.append(c.next_element.string)
        
        email = ''
        site = ''

        flag = 0
        for i in email_site.find_all('img'):
            if flag == 0:
                email = i.next_element.string
                flag = flag + 1
            else:
                site = i.next_element.string

        info = {
            'name': name,
            'position': position,
            'company': company,
            'phone': phone_numbers,
            'mobile': mobile_numbers,
            'email': email,
            'site': site
        }

        save_info(info)
        
    #return render(request, 'directory/scrape.html', {'html': directory_div.get_text()})

def save_info(info):
    prof = save_profile(info['name'], info['position'], info['company'], info['email'], info['site'])
    if (len(info['phone']) > 0):
        save_contact(prof, info['phone'], 'Phone')
    if (len(info['mobile']) > 0):
        save_contact(prof, info['mobile'], 'Mobile')

def save_profile(name, position, company, email, site):
    return Professional.objects.create(name=name, position=position, company=company, email=email, website=site)

def save_contact(professional, numbers, contact_type):
    for n in numbers:
        Contact.objects.create(professional=professional, contact_number=n, contact_type=contact_type)
