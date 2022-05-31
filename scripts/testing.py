"""
based on docs from https://developers.home-assistant.io/docs/api/rest/

"""
from requests import get, post

from config.secrets import token, HA_url
from config.entities import lights, plugs

headers = {
    "Authorization": f"Bearer {token}",
    "content-type": "application/json",
}

def example_get_request():
    url = f"{HA_url}/api/services"
    response = get(url, headers=headers)
    print(response.text)

def example_post_request_lights():
    url = f"{HA_url}/api/services/light/turn_on"  # Something like http://localhost:8123/api
    ent_id = lights['bigLight']
    data = {"entity_id":ent_id,
            "brightness_pct": 0}
    response = post(url, json=data, headers=headers)
    print(response.text)


def example_post_request_plugs():
    url = f"{HA_url}/api/services/switch/toggle"  # Something like http://localhost:8123/api
    ent_id = plugs['fairyLights']
    data = {"entity_id":ent_id}
    response = post(url, json=data, headers=headers)
    print(response.text)

example_post_request_plugs()
