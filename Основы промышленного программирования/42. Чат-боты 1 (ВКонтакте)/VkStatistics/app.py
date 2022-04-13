import logging

import vk_api
from flask import Flask, render_template
from werkzeug.exceptions import Forbidden

from login_password import LOGIN, PASSWORD

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)


def get_vk_api():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        logger.error(error_msg)
        raise
    vk = vk_session.get_api()
    return vk


def get_ages(vk_stats):
    ages = {
        "12-18": 0,
        "18-21": 0,
        "21-24": 0,
        "24-27": 0,
        "27-30": 0,
        "30-35": 0,
        "35-45": 0,
        "45-100": 0,
    }
    for stat in vk_stats:
        stat = stat["reach"]  # конкретно подписчики
        for age in stat["age"]:
            ages[age["value"]] += age["count"]
    return ages


def get_activities(vk_stats):
    activities = {
        "likes": 0,
        "subscribed": 0,
        "unsubscribed": 0,
    }
    for stat in vk_stats:
        for activity_key, activity_value in stat["activity"].items():
            if activity_key in activities:
                activities[activity_key] += activity_value
    return activities


def get_cities(vk_stats):
    cities = set()
    for stat in vk_stats:
        stat = stat["reach"]  # конкретно подписчики
        for city in stat["cities"]:
            cities.add(city["name"])
    cities = sorted(cities)
    return cities


def get_club_statistics(club_id):
    vk = get_vk_api()
    stats = vk.stats.get(group_id=club_id, intervals_count=10, stats_groups="reach")
    ages = get_ages(stats)
    activities = get_activities(stats)
    cities = get_cities(stats)
    return activities, ages, cities


@app.route("/vk_stat/<int:club_id>")
def vk_stat(club_id):
    # club_id = 96015366
    # club_id = 144533659
    try:
        activities, ages, cities = get_club_statistics(club_id)
    except vk_api.ApiError:
        logger.error("no access for club")
        raise Forbidden("Нет доступа к сообществу")
    return render_template("statistics.html", activities=activities, ages=ages, cities=cities)


if __name__ == '__main__':
    app.run("", port=8080, debug=True)
