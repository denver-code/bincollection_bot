from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrapeResult:
    '''class to hold the individual values of each bin and its details'''
    bin_type: str
    bin_colour: str
    collection_days: list[str]
    datetime_parser: str = "%A %d %b %Y"
    datetime_format = "%Y-%m-%d"

    def parse_collection_days(self) -> list[str]:
        '''takes raw collection days and parses into flutter friendly format'''
        return [datetime.strptime(collection_day, self.datetime_parser)
                .strftime(self.datetime_format)
                for collection_day in self.collection_days]


def expand_for_json(results: list[ScrapeResult]) -> list[dict]:
    '''takes existing results and expands based on collection_days'''
    expanded_results = [{
        'bin_type': result.bin_type,
        'bin_colour': result.bin_colour,
        'collection_day': collection_day
    } for result in results
        for collection_day in result.parse_collection_days()
    ]
    return expanded_results


class Scraper:
    BASE_URL: str = "https://www.adur-worthing.gov.uk"
    def scrape(
            self,
            url: str =
            "/bin-day/?brlu-selected-address=200004014421"
    ) -> list[ScrapeResult]:
        """scrapes the table data from the council website"""
        r = requests.get(self.BASE_URL + url)
        if r.status_code != 200:
            return False
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find_all('table')[0]

        # loop through table rows and generate data
        rows = table.find_all('tr')
        results = [parse_row(row) for row in rows[1:-1]]
        return results
    

    def scrape_calendar_link(
            self,
            url: str = "/bin-day/?brlu-selected-address=200004014421"
    ):
        r = requests.get(self.BASE_URL + url)
        if r.status_code != 200:
            return False
        soup = BeautifulSoup(r.text, "lxml")
        a = soup.find_all("a", {"class": "file-pdf"})[0]
        
        return a["href"]


def parse_row(row: Tag) -> ScrapeResult:
    """parses a row from the table
    to retrieve the bin collection information"""
    bin_type = row.find_all('th')[0].text
    eles = row.find_all('td')
    bin_colour = eles[0].text.strip()
    collection_days = [
        str(ele) for ele in eles[1].contents if not isinstance(ele, Tag)
    ]
    return ScrapeResult(bin_type, bin_colour, collection_days)
