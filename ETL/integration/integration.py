import logging
import os
from asyncio import sleep
from datetime import datetime

import requests

from ETL import constants
from ETL.integration.models import ConfigDatabase, FileUploader, PostCode, Code, PostCodeRAW
from ETL.integration.parser import ParserCSV


class IntegrationPostCode:
    """
    class for integration API
    """

    def __init__(self):

        self.db = ConfigDatabase()
        self.file_path = os.environ.get('FILES', None)
        self.parser = ParserCSV()
        self.url = os.environ.get('URL_POSTCODE')

    def execute(self, data_type):
        pending_files = self.db.session.query(FileUploader).filter(FileUploader.processed.is_(False)).all()
        if pending_files:
            self.extract_data()
        else:
            logging.info("No pending files to process")

    def extract_data(self):
        extract_data_csv = self.parser.read_files(self.file_path)
        if extract_data_csv:
            logging.info("Extract data succeeded")

    def get_postcode_api(self, data_type):
        data_api = self.db.session.query(PostCode).order_by(PostCode.id).limit(100000)
        for item in data_api:
            result = self.connect_postcode(item, data_type)
            self.transform_load_csv(result[0])

    def connect_postcode(self, item, data_type):
        url = self.url + '?lon={0}&lat={1}'.format(item.lon, item.lat)

        response = requests.get(url)
        if response.status_code == 200:
            r = response.json()
            result = r['result']
            self.load_data_raw(r, data_type, item.id)
            return result

    def transform_load_csv(self, data):
        try:
            data = Code(postcode=data['postcode'],
                        country=data['country'], latitude=data['latitude'], longitude=data['longitude'],
                        created_at=datetime.now())
            self.db.session.add(data)
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            raise

    def load_data_raw(self, data, data_type, _id):
        try:
            data = PostCodeRAW(postcode_id=_id, data_type=data_type, json_data=data, created_at=datetime.now())
            self.db.session.add(data)
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            raise

