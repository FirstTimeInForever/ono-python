import pause
from datetime import datetime as dt
import datetime
from group_api import GroupApi
import ono_api
import math
from app_config import AppConfig


group_api = GroupApi(AppConfig.GroupApi)


def build_media_query(text_content):
    query = {
        "media": [{
            "type": "text",
            "text": text_content
        }],
        "publishAt": datetime.now().isoformat(),
        "onBehalfOfGroup": False,
        "disableComments": True
    }
    return query


def probe_source_type(source):
    if source.lower() == "independent":
        return "Независимые"
    return "Официальные"


def post_current_news():
    data = ono_api.get_articles_with_raiting()
    media = []
    first_one = True
    assert "articles" in data
    for articles in data["articles"]:
        source_type = probe_source_type(articles[0]["source_type"])
        header_text = f"{source_type} источники:"
        if not first_one:
            header_text = "\n" + header_text
        media.append({
            "type": "text",
            "text": header_text
        })
        for index, article in enumerate(articles):
            media.append({
                "type": "text",
                "text": f"{index}. {article['title']}"
            })
            media.append({
                "type": "text",
                "text": article["link"]
            })
        first_one = False
    group_api.make_post({
        "media": media
    })


def calc_seconds_after_midnight():
    now = dt.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    return now, seconds


def calc_next_post_time(interval_time):
    assert interval_time < 24 * 60
    now, current_seconds = calc_seconds_after_midnight()
    # print(f"Current date: {now}")
    minutes = math.floor(current_seconds / 60)
    next_minutes = math.floor(minutes / interval_time + 1) * interval_time
    # print(minutes)
    # print(next_minutes)
    minutes_diff = next_minutes - minutes
    # print(minutes_diff)
    next_date = now + datetime.timedelta(minutes=minutes_diff)
    # print(f"Next date: {next_date}")
    return next_date


def wait_until_next_post_time():
    assert AppConfig.post_time < 24 * 60
    # interval in minutes
    interval_time = AppConfig.post_time
    post_date = calc_next_post_time(interval_time)
    pause.until(post_date)


def run_post_loop():
    while True:
        print("Waiting for post time")
        print(dt.now(), flush=True)
        wait_until_next_post_time()
        post_current_news()
        break


if __name__ == "__main__":
    run_post_loop()
