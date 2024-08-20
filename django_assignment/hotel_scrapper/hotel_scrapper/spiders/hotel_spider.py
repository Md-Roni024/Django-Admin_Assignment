import re
import json
import scrapy
import random
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import sys

class TripSpider(scrapy.Spider):
    name = 'hotel_spider'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def parse(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1).strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    
                    Translate = hotel_data_dict['translate']
                    polular_hotel_country = Translate['key.hotel.homepage.hotelrecommendation.hotdomestichotels'].split('%')[0]
                    polular_hotel_worldwide = Translate['key.hotel.homepage.hotelrecommendation.hotoverseashotels']
                    polular_hotel_citiesIn = Translate['key.hotel.homepage.hotelrecommendation.hotdomesticcities'].split('%')[0]
                    polular_hotel_cities_worldwide = Translate['key.hotel.homepage.hotelrecommendation.hotoverseascities']
                    polular_hotel_hot5starhotels = Translate['key.hotel.homepage.hotelrecommendation.hot5starhotels']
                    polular_hotel_hotcheaphotels = Translate['key.hotel.homepage.hotelrecommendation.hotcheaphotels']

                    combined_list = [
                        polular_hotel_country,
                        polular_hotel_worldwide,
                        polular_hotel_citiesIn,
                        polular_hotel_cities_worldwide,
                        polular_hotel_hot5starhotels,
                        polular_hotel_hotcheaphotels
                    ]
                    
                    random_items = random.sample(combined_list, 3)    
                    for item in random_items:
                        yield from self.hotelDetails(item)

                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {e}")

    def hotelDetails(self, random_items):
        if random_items in ["Top Luxury 5-star Hotels", "Budget-friendly Hotels Worldwide"]:
            if random_items == "Top Luxury 5-star Hotels":
                yield scrapy.Request(
                    url='https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
                    callback=self.parse_hotel_details,
                    meta={'flag': "Top Luxury 5-star Hotels"}
                )
            else:
                yield scrapy.Request(
                    url='https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
                    callback=self.parse_hotel_details,
                    meta={'flag': "Budget-friendly Hotels Worldwide"}
                )
        else:
            cities = {
                "Popular Hotels in ": [338, 722, 318],
                "Popular Hotels Worldwide": [315, 359, 2],
                "Popular Cities in ": [338, 722, 318, 1270, 3194, 706, 1733, 780, 1289]
            }.get(random_items, [359, 2, 315, 58, 1, 73, 220, 532, 192, 32])
            
            for city_id in cities:
                url = f"https://uk.trip.com/hotels/list?city={city_id}&checkin=2024/8/19&checkout=2024/08/25"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details_With_cities
                )

    def parse_hotel_details(self, response):
        flag = response.meta.get('flag') 
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1).strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    initData = hotel_data_dict['initData']
                    htlsData = initData['htlsData']
                    if flag == "Top Luxury 5-star Hotels":
                        fiveStarHotels = htlsData['fiveStarHotels']
                        for hotel in fiveStarHotels:
                            hotel_name = hotel.get('hotelName')
                            hotelAddress = hotel.get('address')
                            image_url = "https://ak-d.tripcdn.com/images" + hotel.get('imgUrl')
                            rating = hotel.get('rating')
                            price_info = hotel.get("displayPrice", {})
                            price = price_info['price']
                            rooms = [picture for picture in hotel["pictureList"] if picture["pictureTypeName"] == "Rooms"]
                            room_type = random.choice(rooms)["pictureTypeName"]
                            longitude = hotel.get('lon')
                            latitude = hotel.get('lat')
                            yield {
                                'title': hotel_name,
                                'rating': rating,
                                'location': hotelAddress,
                                'latitude': latitude,
                                'longitude': longitude,
                                'room_type': room_type,
                                'price': price,
                                'image_url': image_url,
                            }
                    else:
                        cheapHotels = htlsData['cheapHotels']
                        for hotel in cheapHotels:
                            hotel_name = hotel.get('hotelName')
                            hotelAddress = hotel.get('address')
                            image_url = "https://ak-d.tripcdn.com/images" + hotel.get('imgUrl')
                            rating = hotel.get('rating')
                            price_info = hotel.get("displayPrice", {})
                            price = price_info['price']
                            rooms = [picture for picture in hotel["pictureList"] if picture["pictureTypeName"] == "Rooms"]
                            room_type = random.choice(rooms)["pictureTypeName"]
                            longitude = hotel.get('lon')
                            latitude = hotel.get('lat')

                            yield {
                                'title': hotel_name,
                                'rating': rating,
                                'location': hotelAddress,
                                'latitude': latitude,
                                'longitude': longitude,
                                'room_type': room_type,
                                'price': price,
                                'image_url': image_url,
                            }

                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {e}")

    def parse_hotel_details_With_cities(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1).strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    Translate = hotel_data_dict['initData']
                    firstPageList = Translate['firstPageList']
                    hotelList = firstPageList['hotelList']

                    for hotel in hotelList:
                        hotel_info = hotel.get('hotelBasicInfo')
                        hotel_name = hotel_info.get('hotelName')
                        hotelAddress = hotel_info.get('hotelAddress')
                        price = hotel_info.get('price')
                        image_url = hotel_info.get('hotelImg')

                        comment_info = hotel.get('commentInfo', {})
                        rating = comment_info.get('commentScore')

                        roomInfo = hotel.get('roomInfo', {})
                        roomType = roomInfo.get('physicalRoomName')

                        positionInfo = hotel.get('positionInfo', {})
                        coordinate = positionInfo.get('coordinate', {})
                        longitude = coordinate.get('lng')
                        latitude = coordinate.get('lat')
                        yield {
                            'title': hotel_name,
                            'rating': rating,
                            'location': hotelAddress,
                            'latitude': latitude,
                            'longitude': longitude,
                            'room_type': roomType,
                            'price': price,
                            'image_url': image_url,
                        }

                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {e}")

def spider_opened(spider):
    print("Scrapy is running...")

def spider_closed(spider):
    print("Scrapy successfully completed.")

if __name__ == "__main__":
   # Configure logging to suppress unnecessary output
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        level=logging.WARNING,  # Suppress info-level logs
        format='%(levelname)s: %(message)s',
        stream=sys.stdout
    )
    
    process = CrawlerProcess({
        'LOG_LEVEL': 'WARNING',  # Adjust log level if needed
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    })
    process.crawl(TripSpider)
    process.start(stop_after_crawl=True)
    
    spider_opened(None)
    spider_closed(None)



