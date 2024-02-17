import json
import logging
from faker import Faker

logging.basicConfig(level=logging.INFO)

faker = Faker()

DATA_TYPES = {'string', 'number', 'integer', 'boolean'}


def get_fake_data(data_type, name):
    """
    Generate fake data based on the given data type.

    Args:
        data_type (str): The data type.
        name (str): The name of the parameter.

    Returns:
        str or int or float or bool: The fake data.
    """
    if data_type == 'string':
        if name == 'name':
            return faker.name()
        return faker.text()
    elif data_type == 'number':
        return faker.random_number()
    elif data_type == 'integer':
        return faker.random_int()
    elif data_type == 'boolean':
        return faker.boolean()
    else:
        raise ValueError(f"Invalid data type: {data_type}")


def add_examples_to_parameters(openapi_directory_path, openapi_file_name):
    """
    Add example values to parameters in the OpenAPI specification.

    Args:
        openapi_directory_path (str): The directory path containing the OpenAPI specification file.
        openapi_file_name (str): The name of the OpenAPI specification file.
    """
    try:
        # Load OpenAPI specification from file
        with open(f"{openapi_directory_path}{openapi_file_name}", 'r') as file:
            openapi_spec = json.load(file)

        # Iterate through each path in the OpenAPI specification
        for path in openapi_spec.get('paths', {}).values():
            for method in path.values():
                parameters = method.get('parameters', [])
                if not parameters:
                    logging.warning("No parameters found in method.")
                    continue

                for param in parameters:
                    schema = param.get('schema', {})
                    param_type = schema.get('type')
                    if param_type in DATA_TYPES:
                        param['example'] = get_fake_data(
                            param_type, param.get('name'))

        # Save modified OpenAPI specification to file
        with open(f"{openapi_directory_path}{openapi_file_name.split('.')[0]}_result.json", 'w') as file:
            json.dump(openapi_spec, file, indent=2)
    except FileNotFoundError:
        logging.error(
            f"File not found: {openapi_directory_path}{openapi_file_name}")
    except json.JSONDecodeError:
        logging.error(
            f"Error decoding JSON file: {openapi_directory_path}{openapi_file_name}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


# Example usage:
if __name__ == "__main__":
    openapi_directory_path = 'src/json/'
    openapi_file_name = 'example.json'
    add_examples_to_parameters(openapi_directory_path, openapi_file_name)
