import logging
import os
from io import StringIO
from os import listdir
from os.path import splitext
import pandas as pd

from ETL import constants
from ETL.integration.models import ConfigDatabase


class ParserCSV(object):
    """
    Parser CSV for process
    """
    def __init__(self):
        self.db = ConfigDatabase()
        self.cur = self.db.connect()
        self.io = StringIO()

    def read_files(self, file_path):

        files = [file for file in listdir(file_path)]
        for item in files:
            filename, extension = splitext(item)
            if extension == constants.CSV:
                file_name = open(file_path + item, "r")
                df = pd.read_csv(file_name)
                self.io.write(df.to_csv(index=None, header=None))
                self.io.seek(0)
                self.copy_csv(df)
            else:
                logging.info("File type not supported")
                return False

    def copy_csv(self, df):
        with self.cur as connection:
            connection.copy_from(self.io, constants.CODE_RAW, columns=df.columns, sep=',')
            self.db.session.commit()

