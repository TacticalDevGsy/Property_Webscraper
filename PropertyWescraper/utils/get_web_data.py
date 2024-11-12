from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import config

page = requests.get(config.URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="property-grid__items")

job_cards = results.find_all("div", class_="property-item")

def extract_job_details(job):
    title_div = job.find("div", class_="property-grid__item-title")
    unique_id = title_div.find("a", class_="property--favourite")

    return {
        "unique_id1": unique_id['data-reapit-id'],
        "unique_id2": unique_id['data-property-id'],
        "title": title_div.find("a").text.strip(),
        "price": job.find("span", class_="property-grid__item-price").text.strip(),
        "parish": job.find("span", class_="property-grid__item-area").text.strip(),
        "bedrooms": job.find("span", class_="property-grid__item-bedrooms").text.strip(),
        "bathrooms": job.find("span", class_="property-grid__item-bathrooms").text.strip(),
        "date_added": datetime.now().strftime("%d-%m-%Y"),
    }

new_listings = [
    extract_job_details(job)
    for job in job_cards
]

with open(config.file_out, newline='\n', mode="a+") as file:
    headers = [head for head in new_listings[0].keys()]
    writer = csv.DictWriter(file, fieldnames=headers)
    how_many_added = 0

    for row in new_listings:
        unique_id = row.get("unique_id1")
        file.seek(0)
        lines = file.read()
        if unique_id not in lines:
            writer.writerow(row)
            how_many_added += 1

    print(how_many_added)

