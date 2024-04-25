from loguru import logger
from jinja2 import Environment, BaseLoader, FileSystemLoader
import os


def envvar(variable_name):
    return os.environ.get(variable_name)


def get_jinja_environment(template_path=None):
    if template_path:
        templateLoader = FileSystemLoader(searchpath=template_path)
    else:
        templateLoader = BaseLoader()

    jinja_environment = Environment(loader=templateLoader)
    jinja_environment.globals.update(envvar=envvar)

    return jinja_environment


def compare_lists(list_a: list, list_b: list):
    """
    This function will take two lists and compare them retuning
    three lists for the list overlaps and the unique values in each list
    """

    in_a_and_b = sorted(list(set(list_a) & set(list_b)))
    in_a_not_b = sorted(list(set(list_a) ^ set(in_a_and_b)))
    in_b_not_a = sorted(list(set(list_b) ^ set(in_a_and_b)))

    return in_a_and_b, in_a_not_b, in_b_not_a


def get_item_from_list(item_name: str, item_list: list):
    """
    Filters a list of items based on the name of the item
    """
    try:
        item = list(filter(lambda x: item_name == x.name, item_list))[0]

    except Exception as exc:
        logger.info(f"Could not find group: {item_name} in the item list")
        logger.error(exc)

    return item


def get_filtered_item_list(
    item_list: list, attribute_list: list, filter_attribute: str
):
    """
    Filters a list of Items based on a specific list of values
    """

    filtered_list = list(
        filter(lambda x: getattr(x, filter_attribute) in attribute_list, item_list)
    )

    return filtered_list


def get_filtered_dict_list(dict_list: list, key_list: list, filter_key: str):
    """
    Filters a list of dictionaries based on a specific list of keys
    """
    filter_to = list()
    if not isinstance(key_list, list):
        filter_to.append(key_list)
    else:
        filter_to = key_list

    filtered_list = list(filter(lambda x: x.get(filter_key) in filter_to, dict_list))

    return filtered_list


def get_list_of_attr(source_list: list, target_attr: str):
    result_list = []
    for element in source_list:
        result_list.append(element.get(target_attr))
    return result_list
