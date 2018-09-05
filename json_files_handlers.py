import json


def _get_data_from_json_file(path_to_json):
    with open(path_to_json) as file:
        data_from_json = json.load(file)
    
    return data_from_json


def load_data_from_json_files(paths):
    with open(paths['glip_links_path']) as file:
        glip_links = json.load(file)

    with open(paths['local_fortunecookies_path']) as file:
        local_fortunecookies = json.load(file)

    with open(paths['urls_path']) as file:
        urls = json.load(file)

    return {'glip_links': glip_links,
            'local_fortunecookies': local_fortunecookies,
            'urls': urls}
