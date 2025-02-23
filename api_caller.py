import requests
import json

class APICaller:
    def __init__(self, url, output_file, logger):
        self.url = url
        self.output_file = output_file
        self.logger = logger

    def fetch_and_store_api_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            with open(self.output_file, 'w') as file:
                json.dump(data, file, indent=4)

            self.logger.info(f"Data successfully fetched from {self.url} and stored in {self.output_file}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    api_url = "https://api3.rsna.org/radelement/v1/sets"
    output_json_file = "api_data.json"
    api_caller = APICaller(api_url, output_json_file, logger)
    api_caller.fetch_and_store_api_data()
