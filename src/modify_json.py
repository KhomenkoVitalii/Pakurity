import json
import logging
from faker import Faker
logging.basicConfig(level=logging.INFO)

faker = Faker()

DATA_TYPES = {'string', 'number', 'integer', 'boolean'}

def get_fake_data(type, string_options):
    match type:
        case 'string':
            if string_options == 'name':
                return faker.name()
            return faker.text()
        case 'number':
            return faker.random_number()
        case 'integer':
            return faker.random_int()
        case 'boolean':
            return faker.boolean()


def add_examples_to_parameters(openapi_directory_path, openapi_file_name):
    # Load OpenAPI specification from file
    with open(f"{openapi_directory_path}{openapi_file_name}", 'r') as file:
        openapi_spec = json.load(file)

    # Iterate through each path in the OpenAPI specification
    for path in openapi_spec['paths'].values():
        for method in path.values():
            # Add examples to parameters with basic datatypes
            if not 'parameters' in method:
                logging.warning('There are no parameters in method')
                return
            
            for param in method['parameters']:
                if not 'schema' in param:
                    logging.warning("There are no schema in params")
                    
                if 'type' in param['schema'] and param['schema']['type'] in DATA_TYPES:
                    param['example'] = get_fake_data(param['schema']['type'], param['name'])

    # Save modified OpenAPI specification to file
    with open(f"{openapi_directory_path}{openapi_file_name.split('.')[0]}_result.json", 'w') as file:
        json.dump(openapi_spec, file, indent=2)