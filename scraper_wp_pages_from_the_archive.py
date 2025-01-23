import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import *
import logging

logging.getLogger("requests").setLevel(logging.CRITICAL)

failure = Fore.LIGHTRED_EX
information = Fore.LIGHTYELLOW_EX
success = Fore.LIGHTGREEN_EX

url = "https://endwalker.com/archive.html"  # found this webpage on Reddit for 500 Reddit posts that the user likes

try:
    print(information, f"Trying to open {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        print(success, f"{url} opened successfully!")
    else:
        print(failure, f"Failed to open {url} with status code: {response.status_code}")
except Exception as e:
    print(failure, f"An error occurred while fetching the page: {e}")

soup = BeautifulSoup(response.text, "html.parser")

try:
    last_modified = soup.select_one(
        "body > main > div:nth-of-type(1) > div > p:nth-of-type(4)"
    ).text
    print(information, last_modified)
except Exception as e:
    print(failure, f"Failed to find last modified date: {e}")

try:
    links = soup.find_all("a", class_="text-black")
    external_links = [link.get("href") for link in links if link.get("href")]
    print(
        information,
        f"Fetching all external links from the webpage... {success} found {len(external_links)} external links!",
    )

    with open("extracted_text.txt", "a", encoding="utf-8") as file:

        for index, link in enumerate(external_links, start=1):
            print(information, f"Visiting link {index}/{len(external_links)}: {link}")
            try:
                linked_page = requests.get(link)
                if linked_page.status_code == 200:
                    linked_soup = BeautifulSoup(linked_page.text, "html.parser")
                    paragraphs = linked_soup.find_all("p")
                    page_text = "\n".join(
                        [p.text for p in paragraphs if p.text.strip()]
                    )
                    file.write(page_text + "\n\n")
                    print(success, f"Extracted text from {link} successfully!")
                else:
                    print(
                        failure,
                        f"Failed to retrieve page {link} with status code: {linked_page.status_code}",
                    )
            except Exception as e:
                print(failure, f"Failed to extract text from {link}: {e}")

            # sleep(2) # Sleep between requests to avoid being rate-limited
except Exception as e:
    print(failure, f"An error had occurred: {e}")
