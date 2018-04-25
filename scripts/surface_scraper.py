# A script for downloading ETD metadata from SURFACE as text files

import re
import requests
import logging
from bs4 import BeautifulSoup as bSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data(soup_obj, div_id='keywords'):
    """finds and returns the content of a div whose id is div_id. Used to extract keywords and abstracts."""
    div = soup_obj.find('div', {'id': div_id})
    content = ""
    if div:
        children = div.findChildren()
        for child in children:
            if child.name == 'p':
                content += child.text
    return content


def get_etd_uris(uri_in='https://surface.syr.edu/etd/', start_page=1, end_page=1):
    """
    A recursive function for collecting ETD URIs from SURFACE (http://surface.syr.edu/etd/).
    :param uri_in: the URI where the ETDs are located (page)
    :param start_page: the starting page from which we should start collecting ETD URIs
    :param end_page: The ending page of pages we wish to collect
    :return: a list of ETD URIs (as strings) from SURFACE
    """
    if start_page != 1 and "index" not in uri_in:
        uri_in = uri_in + 'index.{}.html'.format(str(start_page))
    base_uri = 'https://surface.syr.edu/etd/'
    resp = requests.get(uri_in)
    soup = bSoup(resp.content, 'html.parser')
    anchors = soup.find_all('a')
    etd_links = [a['href'] for a in anchors
                 if re.match('https://surface.syr.edu/' + '[A-z_]+/\d{1,4}/?$', a['href']) is not None]
    if start_page == end_page:
        return etd_links
    return etd_links + get_etd_uris(uri_in=base_uri + 'index.{}.html'.format(str(start_page + 1)),
                                    start_page=start_page + 1,
                                    end_page=end_page)


def main(num_pages=1):
    """get ETD keywords and abstracts from SURFACE, and save the content to a text file."""
    logging.info("collecting URIs...")
    uris = get_etd_uris(end_page=num_pages)
    for i, uri in enumerate(uris):
        this_etd = bSoup(requests.get(uri).content, 'html.parser')
        title = get_data(this_etd, div_id='title')
        department = get_data(this_etd, div_id='department')
        keywords = get_data(this_etd, div_id='keywords')
        abstract = re.sub(r'^(ABSTRACT|Abstract)', '', get_data(this_etd, div_id='abstract'))
        file_name = uri.split('/')[-2] + '_' + uri.split('/')[-1] + '.txt'
        logging.info("writing {}... ({} of {})".format(file_name, i+1, len(uris)))
        with open('../resources/ETD_metadata/' + file_name, 'w', encoding='utf-8') as text_file:
            text_file.write("$TITLE:\n" + title)
            text_file.write("\n\n$DEPARTMENT:\n" + department)
            text_file.write("\n\n$KEYWORDS:\n" + keywords)
            text_file.write('\n\n$ABSTRACT:\n' + abstract)
    logging.info("task complete.")


if __name__ == "__main__":
    main(41)  # total pages = 41 (as of 4/15/2018) (gets all)
