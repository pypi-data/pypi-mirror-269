import os
"""
MarcusLion Global variable
"""
__env__ = os.getenv('MARCUSLION_ENV', "uat")
__api_key__ = os.getenv('MARCUSLION_API_KEY', "b7f88c9c-94ba-11ee-b9d1-0242ac120002")
__base_url__ = os.getenv('MARCUSLION_API_HOST', "https://uat.marcuslion.com")
__api_version__ = "core/api/v2"  # no starting slash
project_id = os.getenv('MARCUSLION_API_PROJECT_ID', "7ea7393b-017d-3ba9-a363-5b7a1043e0fes")


def set_config(env):
    global __base_url__
    global __env__
    if env == "qa":
        __base_url__ = "https://qa1.marcuslion.com"
        __env__ = env
    elif env == "uat":
        __base_url__ = "https://uat.marcuslion.com"
        __env__ = env
    else:
        raise RuntimeError("Invalid environment")

    pass


def get_config():
    return {
        "env": __env__,
        "api_key": __api_key__,
        "base_url": __base_url__,
        "project_id": project_id,
        "api_version": __api_version__
    }