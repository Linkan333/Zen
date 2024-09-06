import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

blue = "\033[36m"
reset = "\033[0m"

def userInterfaceStartup():
    print(blue +"░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░  ")
    time.sleep(1)
    print("       ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print("     ░▒▓██▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print("   ░▒▓██▓▒░  ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print(" ░▒▓██▓▒░    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print("░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print("░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ")
    time.sleep(1)
    print(reset + "")
    print("Use -help for more information about the tool")

def clean_url(url):
    parsed_url = urlparse(url)

    url_no_fragment = urlunparse(parsed_url._replace(fragment=''))

    if parsed_url.scheme == 'http':
        url_no_fragment = url_no_fragment.replace('http://', 'https://')
    
    return url_no_fragment


def inputs():
    print("[*] 1 - Crawl Website")
    print("[*] 2 - Find Subdomains")
    print("[*] 3 - WHOIS Lookup")
    print("[*] 4 - Content Discovery")
    print("[*] 99 - Exit")

    user_input = int(input("Select a number > "))


    if (user_input == "-help"):
        print_help()



    if (user_input == 1):
        website_url = input("Enter URL > ")
        time.sleep(2)
        file_input = input("File name to save to <FILENAME>.txt) > ")

        if not file_input.endswith(".txt"):
            file_input += ".txt"

        try:
            print("Validating connection to website " + website_url)
            r = requests.get(website_url, timeout=10)
            time.sleep(2)

            if r.status_code == 200:
                print("Crawling " + website_url )

                url_list = [clean_url(website_url)]
                crawled_urls = set()
                base_domain = urlparse(website_url).netloc

                while len(url_list) != 0:
                    current_url = url_list.pop()

                    if current_url not in crawled_urls:
                        try:
                            response = requests.get(current_url, timeout=10)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.text, 'html.parser')
                                link_elements = soup.find_all("a", href=True)

                                for link_element in link_elements:
                                    full_url = urljoin(current_url, link_element['href'])
                                    full_url = clean_url(full_url)

                                    link_domain = urlparse(full_url).netloc
                                    if base_domain in link_domain and full_url not in crawled_urls:
                                        url_list.append(full_url)
                                
                                crawled_urls.add(current_url)
                                with open(file_input, 'a') as file:
                                    file.write(f"URL: {current_url} Status code: {response.status_code} \n")

                        except requests.exceptions.RequestException as e:
                            print(f"Error crawling the {current_url} Error: {e}")
            else:
                print("Error response code: " + r.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Error checking the website {website_url}: error message: {e}")
    if (user_input == 2):
        print("Hello, you choosed Find subdomains")
        return inputs()
    if (user_input == 3):
        print("Hello, you choosed WHOIS Lookup")
        return inputs()
    if (user_input == 4):
        print("Hello, you choosed content Discovery")
        return inputs()
    if (user_input == 99):
        print("Exiting...")
        time.sleep(2)
        exit()

def print_help():
    print("Welcome to Zen")
    print("Zen is a tool designed for penetration testing and locating problems and misconfigurations within websites.\n")
    print("Usage: python3 zen.py")
    print("Options: Select a number 1-4 to test the web application with different techniques.\n")
    print("Examples")
    print("Enter URL > https://example.com/")
    
    
def startup():
    userInterfaceStartup()
    time.sleep(1)
    inputs()

startup()
