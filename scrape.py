import httpx
import csv
import time
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict

@dataclass
class Property:
    title:str
    price:str 
    location:str
    bedrooms:str 
    bathrooms:str
    size_msq:str

class Scrape_Property:
    def __init__(self) -> None:
        self.fieldnames = [
            "title", "price","location", "bathrooms", "bedrooms", "size_msq"
        ]

    def get_html(self, page):
        url = f"https://www.property24.co.ke/property-to-rent?Page={page}"
        response = httpx.get(url, timeout=30)
        return HTMLParser(response.text)

    def parse_property(self, html):
        property = html.css("div.p24_regularTile")

        results = []
        for item in property:
            # Query all necessary elements
            title_elem = item.css_first("span.p24_propertyTitle")
            price_elem = item.css_first("span.p24_price")
            location_elem = item.css_first("span.p24_address")
            bathrooms_elem = item.css_first("span.p24_featureDetails[title='Bathrooms']")
            bedrooms_elem = item.css_first("span.p24_featureDetails[title='Bedrooms']")
            size_msq_elem = item.css_first("span.p24_size")

            #Extract text if the element exists, otherwise assign None
            title = title_elem.text().strip() if title_elem else None
            price = price_elem.text().strip() if price_elem else None
            location = location_elem.text().strip() if location_elem else None
            bathrooms = bathrooms_elem.text().strip() if bathrooms_elem else None
            bedrooms = bedrooms_elem.text().strip() if bedrooms_elem else None
            size_msq = size_msq_elem.text().strip() if size_msq_elem else None

            rental = Property(
                title=title, 
                price=price, 
                location=location, 
                bathrooms=bathrooms, 
                bedrooms=bedrooms,
                size_msq=size_msq
            )
            results.append(asdict(rental))
        return results

    def to_csv(self, res):
        with open("tmp/hosuing_data.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerows(res)

    def main(self):
        for x in range(1, 11544):
            html = self.get_html(x)
            print(f"Successfully scraped page {x}")
            res = self.parse_property(html)
            self.to_csv(res)
            #time.sleep(300)

if __name__=='__main__':
    scraper = Scrape_Property()
    scraper.main()