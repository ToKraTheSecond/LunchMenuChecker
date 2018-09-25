import json


def _get_data_from_json_file(path_to_json):
    with open(path_to_json) as file:
        data_from_json = json.load(file)
    
    return data_from_json


def get_glip_links(GLIP_LINKS_PATH):
    glip_links = _get_data_from_json_file(GLIP_LINKS_PATH)

    return glip_links


def get_local_fortunecookies(LOCAL_FORTUNECOOKIES_PATH):
    local_fortunecookies = _get_data_from_json_file(LOCAL_FORTUNECOOKIES_PATH)

    return local_fortunecookies


def get_urls(URLS_PATH):
    urls = _get_data_from_json_file(URLS_PATH)

    return urls
