from mycroft.util.log import LOG
import requests
import json


def search_addon(kodi_path, addon, query):
    api_path = kodi_path + "/jsonrpc"
    json_header = {'content-type': 'application/json'} 
    kodi_payload = {'jsonrpc': '2.0',
            'method': 'Files.GetDirectory',
            'params': {'properties': ['title', 'genre', 'year', 'rating', 'runtime', 'plot', 'file', 'art', 'sorttitle', 'originaltitle'],
                'directory': "plugin://" + addon + "/action=search&_query=keyword",
                # plugin://plugin.video.tvzavr.ru/action=search&_query=keyword
                'media': 'files'},
            'id': 1
            }
    try:
        kodi_response = requests.post(api_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response
        #queries = json.loads(kodi_response)
        #result = queries.get('result')
    except Exception as e:
        LOG.info(e)
        return None

    #if result:
        #return result.get('files', []) 

