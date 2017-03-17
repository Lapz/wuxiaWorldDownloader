#!/usr/local/bin/python3

"""
Downloads all chapters from a story on wuxia-world and saves them as in a folder called local host

Examples:
    import wuxia_scrape
        wuxia_scrape.run()
            This will grab all the links from a given index page and save them in a folder called wuxia_world
Methods:
    check_for_dir:
        Checks if a directory exsist, if not creates the directory
    get_chap_links:
        Gets all the chap links found on a webpage
    get_book_name:
        Takes a url and and gets the book name from it
    changes_href_to_rel:
        Takes a href poiniting to a exteranl link and changes it to point to a local link
    download_chapter_links:
        Downloads all the chapters passed in to a local folder
    run:
        Runs the whole program
TODO:
    Change how the get_book_name function works and remove list splicing part
    Add better error handling
    Enable the script to work with differnet sites


"""

from bs4 import BeautifulSoup
import requests
import sys
import os
import glob


def check_for_dir(dirName):
    """
    Checks if a directory exists and if not then creates the directory

    Arguments:

        - A dircetory fileName

    """
    if not os.path.exists(dirName):
        os.makedirs(dirName)


def get_chap_links(url):
    """
    Takes a webpage and returns all links found on the page

    Arguments:
        - url A valid url

    Returns:
        - An array contain links

     """
    index_page = requests.get(url)

    try:
        index_page.raise_for_status()

    except Exception as exc:
        print("Their was an error {0}".format(exc))

    index_page_soup = BeautifulSoup(index_page.text, "html.parser")

    chapter_links = list(index_page_soup.select('p > a, div > a'))

    return chapter_links

    # print(chapter_links.getText())


def get_book_name(url):
    """
    Gets the formated book name from the url
    E.g. http://www.wuxiaworld.com/desolate-era-index/de-book-24-chapter-29/
        will return 'de-book-24'

    Arguments:
        A  valid url

    Returns:
        A string
    """
    book_list = str(url).split("/")

    for index, part in enumerate(book_list):
        if "book" in part:
            book_name = ''.join(book_list[index:]).split("-")

            for index, word in enumerate(book_name):
                if "chapter" in word:
                    book = '-'.join(book_name[:index])
                    return book

        elif "chapter" in part:
            chap_name = book_list[index:]
            book_name = ''.join(chap_name)
            return book_name

    # book_name = '-'.join(book_list)

    # return book_name


def changes_href_to_rel(url):
    """ Opens the file and changes the href to point to a local file not the web """
    split_url = url.split("/")

    for section in split_url:
        if "book" in section:

            chap_name = section.split("-")

            for index, word in enumerate(chap_name):

                if "chapter" in word:
                    rel_url = "./" + \
                        " ".join(chap_name[index:]).title() + ".html"
                    return rel_url


def download_chapters(links):
    """ Downloads the chapters and saves them in markdown format"""

    if(links == 0):
        print("Invalid index page")

    else:

        for link in links:
            chapter_url = str(link.get('href'))
            chapter_book = get_book_name(link.get('href'))
            # Gets the url splits it takes the part that has the book splits
            # that and joins it together for a valid pathname

            chapter_file_name = str(link.getText()).split(" ")[0:2]

            chapter_file_name = ' '.join(chapter_file_name)
            chapter_file_name += ".html"

            chapter_title = str(link.getText())

            try:
                print('Downloading {0}  from {1} \n '.format(
                    chapter_title, chapter_book))

                res = requests.get(chapter_url)

                res.raise_for_status()

                soup = BeautifulSoup(res.text, "html.parser")

                for a in soup.findAll('a'):
                    a['href'] = changes_href_to_rel(a['href'])

                chapter_contents = soup.find(
                    "div", itemprop="articleBody").prettify("utf-8")

                check_for_dir("./wuxia_world/{0}".format(chapter_book))

                chapter_file = open(os.path.join(
                    "./wuxia_world/{0}".format(chapter_book), os.path.basename(chapter_file_name)), 'wb')

                chapter_file.write(chapter_contents)

                chapter_file.flush()

                chapter_file.close()

            except Exception as exc:
                continue

        print("Finished downloading {0} chapters".format(len(links)))

        # Skip this link


def run(index_link):
    """ Operates the whole program and allows it to be run from the command line """
    check_for_dir("./wuxia_world")
    links = get_chap_links(index_link)
    download_chapters(links)


if __name__ == "__main__":
    run(sys.argv[1])
