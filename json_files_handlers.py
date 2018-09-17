import json

from paths import GLIP_LINKS_PATH, LOCAL_FORTUNECOOKIES_PATH, URLS_PATH


def _get_data_from_json_file(path_to_json):
    with open(path_to_json) as file:
        data_from_json = json.load(file)
    
    return data_from_json


def load_data_from_json_files():
    with open(GLIP_LINKS_PATH) as file:
        glip_links = json.load(file)

    with open(LOCAL_FORTUNECOOKIES_PATH) as file:
        local_fortunecookies = json.load(file)

    with open(URLS_PATH) as file:
        urls = json.load(file)

    return {'glip_links': glip_links,
            'local_fortunecookies': local_fortunecookies,
            'urls': urls}
