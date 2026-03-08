from langchain_community.document_loaders.csv_loader import CSVLoader
from Multiagent.exception.exception import MultiagentException
import sys
import os
from Multiagent.logging.logger import logger

FILE_PATH = "file/test1.csv"


def document_loader():
    try:

        if not os.path.exists(FILE_PATH):
            logger.info("File not found")
            return

        loader = CSVLoader(file_path=FILE_PATH)

        data = loader.load()

        logger.info("File successfully loaded")

        return data

    except Exception as e:
        logger.error("Error while loading document")
        raise MultiagentException(e, sys)


document_loader()