import argparse
from types import SimpleNamespace
from sys import exit
from datetime import datetime

from posters import post_fortune_cookie, post_menu
from parsers import get_menu_nepal
from json_files_handlers import get_glip_links, get_local_fortunecookies, get_urls
from correct_time_checker import check_if_menu_can_be_posted
from paths import GLIP_LINKS_PATH, LOCAL_FORTUNECOOKIES_PATH, URLS_PATH


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    if not check_if_menu_can_be_posted(datetime.today().weekday(), datetime.date(datetime.now())):
        exit('Not posting on non working day')

    glip_links = SimpleNamespace(**get_glip_links(GLIP_LINKS_PATH))
    local_fortunecookies = SimpleNamespace(**get_local_fortunecookies(LOCAL_FORTUNECOOKIES_PATH))
    urls = SimpleNamespace(**get_urls(URLS_PATH))

    if args["type"] == "test_conv":
        post_url = glip_links.test_conv
    elif args["type"] == "post_conv":
        post_url = glip_links.post_conv
    else:
        raise ValueError("wrong input argument")

    post_fortune_cookie(urls.fortune_cookie,
                        urls.fortune_cookie_icon,
                        post_url,
                        local_fortunecookies["local_fortune_cookies"])

    nepal = get_menu_nepal(urls)

    post_menu(post_url,
              urls.nepal_brno_icon,
              nepal["Name"],
              nepal["payload"])
