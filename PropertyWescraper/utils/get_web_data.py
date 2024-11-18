from fileinput import filename
from os.path import exists

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
from string import punctuation

from PropertyWescraper.utils.sql_helper import MysqlConnector
from config import WebData


def load_data_from_html(url_to_scrape):
    page = requests.get(url_to_scrape)
    return BeautifulSoup(page.content, "html.parser")

def download_image(response, filename_in):
    filename = filename_strip(filename_in)
    if not exists(f'./property_images/{filename}'):
        with open(f'./property_images/{filename}', 'wb') as out_file:
            for chunk in response.iter_content(1024):
                out_file.write(chunk)

    return filename

def filename_strip(filename: str):
    for char in punctuation:
        filename = filename.replace(char, ' ').replace(' ','')

    return f"{filename}.jpg"

def extract_job_details(job):
    title_div = job.find("div", class_="property-grid__item-title")

    image = job.find("div", class_="property-grid__item-image").find("img")["src"]
    image_filename = download_image(requests.get(image), title_div.find("a").text.strip())

    unique_id = title_div.find("a", class_="property--favourite")

    return {
        "unique_id1": unique_id['data-reapit-id'],
        "unique_id2": unique_id['data-property-id'],
        "title": title_div.find("a").text.strip(),
        "price": job.find("span", class_="property-grid__item-price").text.strip(),
        "parish": job.find("span", class_="property-grid__item-area").text.strip(),
        "bedrooms": job.find("span", class_="property-grid__item-bedrooms").text.strip(),
        "bathrooms": job.find("span", class_="property-grid__item-bathrooms").text.strip(),
        "dateAdded": datetime.now().strftime("%Y-%m-%d"),
        "imageName": image_filename
    }

def get_new_listings():

    soup = load_data_from_html(WebData.URL_new)
    results = soup.find(class_="property-grid__items")

    job_cards = results.find_all("div", class_="property-item")

    new_listings = [extract_job_details(job) for job in job_cards]

    # add_new_data_to_file(new_listings)
    add_new_data_to_sql(new_listings)

    return

def add_new_data_to_file (new_listings):
    with open(WebData.file_out, newline='\n', mode="a+") as file:
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

def add_new_data_to_sql(new_listings):
    #new_listings[0]["unique_id1"] = 12345
    sql_instance = MysqlConnector(table_name="new_properties")
    existing_data = sql_instance.select_data([row.get("unique_id1") for row in new_listings])

    how_many_added = 0
    for row in new_listings:
        unique_id = row.get("unique_id1")
        if unique_id not in existing_data:
            sql_instance.insert_data(row)
            how_many_added += 1
    print(how_many_added)


if __name__ == "__main__":

    get_new_listings()