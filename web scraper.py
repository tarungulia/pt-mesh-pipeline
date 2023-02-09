"""
# requirements.txt
beautifulsoup4==4.11.2
matplotlib==3.3.3
requests==2.25.0
"""
# main.py
import logging
import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt

def get_tender_data():
    r = requests.get('https://etenders.gov.in/eprocure/app')
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('tr', class_='list_header')
    content = s.find_all('td')
    header = [header.text.strip() for header in content]

    s = soup.find('div', id='vmarquee')
    content1 = s.find_all('td')

    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(0, len(content1), 4):
            row = [content1[i].text.strip(), content1[i+1].text.strip(), content1[i+2].text.strip(), content1[i+3].text.strip()]
            writer.writerow(row)

def plot_tender_frequency():
    tender_count = {}
    with open('output.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row[0] for row in reader]
        for tender in data:
            if tender in tender_count:
                tender_count[tender] += 1
            else:
                tender_count[tender] = 1

    plt.bar(tender_count.keys(), tender_count.values(), color='blue')
    plt.xlabel('Tenders')
    plt.ylabel('Frequency')
    plt.title('Tender frequency')
    plt.show()

def main():
    logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    try:
        get_tender_data()
        plot_tender_frequency()
        logging.info('Scraping and plotting successful')
    except Exception as e:
        logging.error(f'Error occured while scraping and plotting: {e}')

if __name__ == '__main__':
    main()
