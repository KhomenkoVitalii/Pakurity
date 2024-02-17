import ast
import logging

logging.basicConfig(level=logging.INFO)


def patch_def(tree, def_name, def_new_implementation):
    """
    Patch the function definition with a new implementation.

    Args:
        tree (ast.AST): The abstract syntax tree of the script.
        def_name (str): The name of the function to patch.
        def_new_implementation (str): The new implementation for the function.

    Returns:
        str: The patched script.
    """
    if not def_name or not def_new_implementation:
        raise ValueError(
            "Please provide the function name and new implementation.")

    is_def_found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == def_name:
            logging.info(f"Found function '{def_name}'.")
            node.body = ast.parse(def_new_implementation).body
            is_def_found = True

    if not is_def_found:
        logging.warning(f"Function '{def_name}' not found in the script.")

    return ast.unparse(tree)


def patch_openapi_script(script_path, script_name, script_def_name, script_def_new_implementation):
    """
    Patch the specified script with a new implementation for a function.

    Args:
        script_path (str): The path to the script.
        script_name (str): The name of the script file.
        script_def_name (str): The name of the function to patch.
        script_def_new_implementation (str): The new implementation for the function.
    """
    script_file_path = f"{script_path}{script_name}"
    result_file_path = f"{script_path}{script_name.split('.')[0]}_result.py"

    with open(script_file_path, 'r') as file:
        script_content = file.read()

    tree = ast.parse(script_content)

    patched_script = patch_def(
        tree, script_def_name, script_def_new_implementation)

    with open(result_file_path, 'w') as file:
        file.write(patched_script)

    logging.info(f"Patched script saved as '{result_file_path}'.")
