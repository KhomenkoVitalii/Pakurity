from src.modify_json import add_examples_to_parameters
import logging
logging.basicConfig(level=logging.INFO)

if "__main__" == __name__:
    logging.info("Start...")
    openapi_directory_path = 'src/json/'
    openapi_file_name = 'example.json'
    add_examples_to_parameters(openapi_directory_path, openapi_file_name)
    logging.info("Finished")
