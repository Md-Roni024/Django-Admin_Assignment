from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import requests
from scrapy.exceptions import DropItem
import os
from urllib.parse import urlparse

Base = declarative_base()

class HotelDetails(Base):
    __tablename__ = 'hotels_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    rating = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    price = Column(Float)
    image_url = Column(String) 
    image_path = Column(String)


class HotelPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.database_url = settings.get('DATABASE_URL')
        print(f"Database URL: {self.database_url}")
        
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        self.test_connection() 

    def test_connection(self):
        try:
            with self.Session() as session:
                session.execute(text('SELECT 1'))
            print("Database successfuly connected.")
            print("Crawler is Running ....")
            print("Please wait ....")
        except Exception as e:
            print(f"Database connection test failed: {e}")

    def process_item(self, item, spider):
        session = self.Session()
        image_path = item.get('image_path')
        relative_image_path = self.get_relative_image_path(image_path)
        hotel = HotelDetails(
            title=item.get('title'),
            rating=self.parse_float(item.get('rating')),
            location=item.get('location'),
            latitude=self.parse_float(item.get('latitude')),
            longitude=self.parse_float(item.get('longitude')),
            room_type=item.get('room_type'),
            price=self.parse_float(item.get('price')),
            image_url=item.get('image_url'),
            image_path=relative_image_path
        )
        session.add(hotel)
        session.commit()
        session.close()
        return item

    def get_relative_image_path(self, full_path):
        return full_path

    def parse_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


class ImageDownloadPipeline:
    def process_item(self, item, spider):
        image_url = item.get('image_url')
        if not image_url:
            raise DropItem(f"Missing image URL in {item}")

        project_root = os.path.dirname(os.path.abspath(spider.settings.get('PROJECT_DIR')))
        images_dir = os.path.join(project_root, 'media', 'property_images')
        os.makedirs(images_dir, exist_ok=True)
        parsed_url = urlparse(image_url)
        image_name = os.path.basename(parsed_url.path)
        base, ext = os.path.splitext(image_name)
        counter = 1

        while os.path.exists(os.path.join(images_dir, image_name)):
            image_name = f"{base}_{counter}{ext}"
            counter += 1
        image_path = os.path.join(images_dir, image_name)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            item['image_path'] = "property_images/" + image_name
        else:
            raise DropItem(f"Failed to download image from {image_url}")
        return item
