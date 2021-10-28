import os
import requests
from bs4 import BeautifulSoup
import json
# os.path.abspath(os.path.join(os.getcwd(), os.pardir))


def url_parse(url='http://quotes.toscrape.com/page/1/'):
    """
    Respond the list of parsed quotes from page
    @param url: The url to parse
    returns: A list of extracted quotes from page
    """

    response = requests.get(url)
    # scrapy_response = HtmlResponse(url, body=response.content)
    # print(scrapy_response)
    # assert Spider().parse(scrapy_response) == target
    return response_parsing(response.content)


def response_parsing(content):
    all_quotes = []
    data = BeautifulSoup(content, features="lxml")
    for each in data.find_all('span', attrs={'class': 'text'}):
        all_quotes.append(each.text)
    return all_quotes


def get_parsed_data():
    """
    returns: A list of parsed quotes from scrapy saved json
    """
    file_path = os.getcwd()
    # file_path = "/".join(os.getcwd().split("/")[:-1])
    file_path = os.path.join(file_path, "quotes.json")
    return json_parser(file_path)


def json_parser(file_path):
    all_quotes = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        for each in data:
            all_quotes.append(each['quote_text'])
    return all_quotes


def compare(file_quotes, response_quotes):
    """
    Comparing both scrapy saved data and url response data.
    All the quotes present in response should be in saved data.
    @param file_quotes: Scrapy spider saved data.
    @param response_quotes: URL response data.
    returns: String of "Matched" / "Not Matched"
    """
    status = True
    for quote in response_quotes:
        # if any quote not matched then scrapping failed
        if quote not in file_quotes:
            status = False
            print(quote)

    if status:
        return "Matched"
    else:
        return "Not Matched"


def testing():
    """
    Calling both parsing functions and printing the result
    :return:
    """
    print(compare(get_parsed_data(), url_parse()))



