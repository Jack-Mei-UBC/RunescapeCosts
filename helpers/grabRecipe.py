import requests
import bs4
from data import rsWikiUrlPart0, rsWikiUrlPart1, rsWikiUrl
from bs4 import BeautifulSoup


def findMaterialStart(tr: bs4.Tag):
    for child in tr.children:
        if isinstance(child, bs4.Tag):
            if list(child.children)[0] is not None:
                if list(child.children)[0].getText() == "Material":
                    return child.nextSibling
    return None


def findMaterialEnd(child: bs4.Tag):
    if list(child.children)[0] is not None:
        if list(child.children)[0].getText() == "Total cost":
            return True
    return False


def findMaterialName(url: str = "https://runescape.wiki/w/Multiply_I"):
    response = requests.get(url)


def searchAssumeCorrect(name: str):
    return searchWiki(name)[-1][0]


def searchWiki(name: str):
    response = requests.request("GET", rsWikiUrlPart0 + name + rsWikiUrlPart1)
    return response.json()


def getMaterial(url: str = "https://runescape.wiki/w/Multiply_I"):
    response = requests.get(url)
    output = []
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the element containing the price information
        classHolder = soup.find('div', {'class': 'recipe-table'})
        tableBody = classHolder.find("tbody")
        ingredient = findMaterialStart(tableBody)
        while not findMaterialEnd(ingredient):
            if isinstance(ingredient, bs4.Tag):
                if list(ingredient.children)[1] is not None:
                    # print(list(ingredient.children)[1].getText)
                    output += [rsWikiUrl + list(ingredient.children)[1].contents[0]["href"]]
            ingredient = ingredient.nextSibling
        return output
    else:
        raise Exception("Failed to get materials")


if __name__ == "__main__":
    print(getMaterial(searchAssumeCorrect("Powerful necroplasm")))
