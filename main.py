import argparse
from types import SimpleNamespace
from sys import exit

from posters import post_fortune_cookie, post_menu
from parsers import get_menu_nepal
from json_files_handlers import load_data_from_json_files
from correct_time_checker import check_if_menu_can_be_posted


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    if not check_if_menu_can_be_posted():
        exit('Not posting on non working day')

    data_from_json_files = load_data_from_json_files()
    data_from_json_files = SimpleNamespace(**data_from_json_files)

    glip_links = data_from_json_files.glip_links
    local_fortunecookies = data_from_json_files.local_fortunecookies
    urls = data_from_json_files.urls
    urls = SimpleNamespace(**urls)

    post_url = glip_links[args["type"]]

    post_fortune_cookie(urls.fortune_cookie,
                        urls.fortune_cookie_icon,
                        post_url,
                        local_fortunecookies["local_fortune_cookies"])

    nepal = get_menu_nepal(urls)

    post_menu(post_url,
              urls.nepal_brno_icon,
              nepal["Name"],
              nepal["payload"])
