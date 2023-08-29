from data import geWebsiteUrl, geWebsiteHeaders
import bs4
from bs4 import BeautifulSoup
import requests
from typing import List


def findItem(rowList: List[bs4.Tag], item: str):
    for row in rowList:
        name = str(row.find("span").getText())
        if str.lower(name) == str.lower(item):
            return row
    raise Exception(f"Found no items matching {item}")


def getItem(item: str):
    response = requests.request("POST", geWebsiteUrl, headers=geWebsiteHeaders, data=f"query={item.replace(' ', '+')}")
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the element on the RS GE
        classHolder = soup.find('table', {'class': 'results-table'}).find("tbody").find_all("tr")

        # If theres only one result, assume it's correct
        if len(list(classHolder)) == 1:
            if isinstance(classHolder[0], bs4.Tag):
                print(classHolder[0].find("a", {
                    "class": "table-item-link"
                })["href"])
        else:
            item = findItem(classHolder, item)
            if isinstance(item, bs4.Tag):
                return (item.find("a", {
                    "class": "table-item-link"
                })["href"])
    else:
        print("Failed to retrieve the webpage.")


def getPrice(itemUrl: str):
    response = requests.get(itemUrl, headers=geWebsiteHeaders)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing the price
        price_element = soup.find('div', class_='stats')
        price_element = price_element.find("span")

        # Extract the price text
        price_text = price_element.get_text(strip=True)

        print("Current price:", price_text)
    else:
        print("Failed to retrieve the webpage.")


if __name__ == "__main__":
   url = getItem("Vial")
   getPrice(url)
