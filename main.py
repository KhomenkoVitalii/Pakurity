import logging
from src.modify_json import add_examples_to_parameters
from src.patch_script import patch_openapi_script

logging.basicConfig(level=logging.INFO)
is_patched_script_available = False


def initialize():
    global is_patched_script_available
    try:
        from src.modify_json_result import add_examples_to_parameters as add_examples_to_parameters_patched
        is_patched_script_available = True
    except ModuleNotFoundError:
        logging.info('There is no patched script available.')
        is_patched_script_available = False


def modify_json_script():
    logging.info("Starting 'modify json' script...")
    openapi_directory_path = 'src/json/'
    openapi_file_name = 'example.json'
    add_examples_to_parameters(openapi_directory_path, openapi_file_name)
    logging.info("Finished 'modify json' script.")


def patch_script():
    logging.info("Starting 'patch' script...")
    script_path = 'src/'
    script_name = 'modify_json.py'
    script_def_name = "get_fake_data"
    script_def_new_implementation = "return 'MADE BY KHOMENKO VITALII'"
    patch_openapi_script(script_path, script_name,
                         script_def_name, script_def_new_implementation)
    global is_patched_script_available
    is_patched_script_available = True
    logging.info("Finished 'patch' script.")


def run_patched_script():
    if not is_patched_script_available:
        logging.info("There is no patched script available.")
        return
    from src.modify_json_result import add_examples_to_parameters as add_examples_to_parameters_patched
    logging.info("Starting 'patched' script...")
    openapi_directory_path = 'src/json/'
    openapi_file_name = 'example.json'
    add_examples_to_parameters_patched(
        openapi_directory_path, openapi_file_name)
    logging.info("Finished 'patched' script.")


def start():
    initialize()
    while True:
        print("\n")
        print("Codes: {'1' = 'run modify json script', '2' = 'run patch script', '3' = 'run patched script to modify json', 'q' - exit }")
        code = input("Enter code: ")
        if code == 'q':
            print('Bye')
            break
        elif code == '1':
            modify_json_script()
        elif code == '2':
            patch_script()
        elif code == '3':
            run_patched_script()
        else:
            logging.info("Invalid code.")


if __name__ == "__main__":
    start()
