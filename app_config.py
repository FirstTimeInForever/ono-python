import os


class AppConfig:
    post_time = int(os.environ["POST_TIME"])

    class GroupApi:
        application_id = os.environ["APPLICATION_ID"]
        access_token = os.environ["ACCESS_TOKEN"]
        session_secret_key = os.environ["SESSION_SECRET_KEY"]
        application_key = os.environ["APPLICATION_KEY"]
        group_id = os.environ["GROUP_ID"]
