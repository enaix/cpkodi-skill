from mycroft.util.log import LOG
import requests
import json


def find_addon(kodi_path, query):
    api_path = kodi_path + "/jsonrpc"
    json_header = {'content-type': 'application/json'} 
    method = "Addons.GetAddons"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "1",
        "params": {}
    }
    try:
        kodi_response = requests.post(api_path, data=json.dumps(kodi_payload), headers=json_header)
        addons = json.loads(kodi_response.text)
        result = addons.get('addons')
    except Exception as e:
        LOG.info(e)
        return None
    if result:
        for addon in result:
            addonid = addon.get('addonid')
            if addonid and addonid.lower().find(query.lower()) != -1:
                return addonid
    return None
