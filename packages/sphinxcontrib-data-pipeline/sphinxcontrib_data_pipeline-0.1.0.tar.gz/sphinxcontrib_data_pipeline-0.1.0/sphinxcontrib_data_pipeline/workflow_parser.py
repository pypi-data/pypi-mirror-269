import sphinx.application
import importlib

# TODO: add fall-back parsers


def get_driver_parser(app: sphinx.application.Sphinx):
    parser_str = app.config.driver_parser
    if parser_str is None:
        raise ValueError(
            "No driver parser specified (driver_parser variable in conf.py)"
        )
    module_name, fct_name = parser_str.rsplit(":", 1)
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(
            f"Could not find module {module_name} "
            "(specified as driver_parser in conf.py)"
        )
    return module.__dict__[fct_name]


def get_data_product_parser(app: sphinx.application.Sphinx):
    parser_str = app.config.data_product_parser
    if parser_str is None:
        raise ValueError(
            "No data product parser specified (data_product_parser variable in conf.py)"
        )
    module_name, fct_name = parser_str.rsplit(":", 1)
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(
            f"Could not find module {module_name} "
            "(specified as data_product_parser in conf.py)"
        )
    return module.__dict__[fct_name]
