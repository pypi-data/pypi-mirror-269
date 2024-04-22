import os

"""
MarcusLion Global variable
"""
__env__ = os.getenv('MARCUSLION_ENV', "uat")
api_key = os.getenv('MARCUSLION_API_KEY', "b7f88c9c-94ba-11ee-b9d1-0242ac120002")
base_url = os.getenv('MARCUSLION_API_HOST', "https://uat.marcuslion.com")
project_id = os.getenv('MARCUSLION_API_PROJECT_ID', "7ea7393b-017d-3ba9-a363-5b7a1043e0fes")
api_version = "core/api/v2"  # no starting slash


def set_config(env):
    global base_url
    global __env__
    if env == "qa":
        base_url = "https://qa1.marcuslion.com"
        __env__ = env
    elif env == "uat":
        base_url = "https://uat.marcuslion.com"
        __env__ = env
    else:
        raise RuntimeError("Invalid environment")

    pass


def get_config():
    return {
        "env": __env__,
        "api_key": api_key,
        "base_url": base_url,
        "project_id": project_id,
        "api_version": api_version
    }