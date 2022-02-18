import requests
import sys, getopt

ENEA_SHORTAGE_LINK = "http://www.wylaczenia-eneaoperator.pl/page_print.php?rejon=17"

def get_outage_page():
    return requests.get(ENEA_SHORTAGE_LINK)


def find_outage_by_text(page, text):
    return text in page.text

def find_all(list_texts):
    page = get_outage_page()

    outages = {}
    for text in list_texts:
        outages[text] = find_outage_by_text(page, text)

    return outages


def main(argv):
    found = find_all(argv)
    print(found)

if __name__ =="__main__":
    main(sys.argv[1:])

