import requests
import sys, getopt

ENEA_SHORTAGE_LINK = "http://www.wylaczenia-eneaoperator.pl/page_print.php?rejon=17"
def find_outage_by_text(text):
    res = requests.get(ENEA_SHORTAGE_LINK)
    return text in res.text

def main(argv):
    text_search = argv[0]
    found = find_outage_by_text(text_search)
    print(found)

if __name__ =="__main__":
    main(sys.argv[1:])

