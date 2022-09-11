import requests
import sys, getopt
from constants import ENEA_SHORTAGE_LINK
from bs4 import BeautifulSoup

def get_outage_page():
    return requests.get(ENEA_SHORTAGE_LINK)


def find_outage_by_text(page, text):
    return text in page.text

def find_all(list_texts):
    page = get_outage_page()

    outages = {}
    soup_page = BeautifulSoup(page.text, 'html.parser')
    for outage_div in soup_page.find_all("div",  class_="info"):
        for text in list_texts:
            if text in outage_div.text :
                date = outage_div.find("p", class_="subtext").text.strip()
                localisation = outage_div.find("p", class_="description").text.strip()
                try:
                    outages[text].append({"date": date, "localisation": localisation})
                except:
                    outages[text] = [{"date": date, "localisation": localisation}]

    return outages


def main(argv):
    found = find_all(argv)
    print(found)

if __name__ =="__main__":
    main(sys.argv[1:])

