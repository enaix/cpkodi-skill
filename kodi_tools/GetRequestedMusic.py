from mycroft.util.log import LOG
import requests
import json


def get_requested_music(kodi_path, search_data):
    """
        returns a music list based on the search item string and the search type
        search_type =  album, artist, label
        may consider passing the music json data item as this will provide all the data required to filter
    """
    api_path = kodi_path + "/jsonrpc"
    json_header = {'content-type': 'application/json'}
    method = "AudioLibrary.GetSongs"
    search_filter = []
    # Check each music key
    # Todo: could iterate through the datatype for keys
    search_key = 'album'
    if search_data[search_key] != "None":
        key_words = ''.join((item for item in search_data[search_key] if not item.isdigit())).split()
        for each_word in key_words:  # Build a filter based on the words in the title
            search_key = {
                "field": search_key,
                "operator": "contains",
                "value": each_word.strip()
            }
            search_filter.append(search_key)
    search_key = 'title'
    if search_data[search_key] != "None":
        key_words = ''.join((item for item in search_data[search_key] if not item.isdigit())).split()
        for each_word in key_words:  # Build a filter based on the words in the title
            search_key = {
                "field": search_key,
                "operator": "contains",
                "value": each_word.strip()
            }
            search_filter.append(search_key)
    search_key = 'artist'
    if search_data[search_key] != "None":
        key_words = ''.join((item for item in search_data[search_key] if not item.isdigit())).split()
        for each_word in key_words:  # Build a filter based on the words in the title
            search_key = {
                "field": search_key,
                "operator": "contains",
                "value": each_word.strip()
            }
            search_filter.append(search_key)
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
                "artist",
                "duration",
                "album",
                "track"
            ],
            "filter": {
                "and": search_filter
            },
            "sort": {
                "order": "ascending",
                "method": "track",
                "ignorearticle": True
            }
        }
    }
    if True:
    #try:
        LOG.info("payload: " + str(kodi_payload))
        kodi_response = requests.post(api_path, data=json.dumps(kodi_payload), headers=json_header)
        LOG.info("Music json" + kodi_response.text)
        item_count = int(json.loads(kodi_response.text)['result']['limits']['total'])
        if item_count > 0:
            song_list = json.loads(kodi_response.text)['result']['songs']
            # remove duplicates
            clean_list = []  # this is a dict
            for each_song in song_list:
                song_title = str(each_song['label'])
                info = {
                    "label": each_song['label'],
                    "songid": each_song['songid'],
                    "artist": each_song['artist']
                }
                if song_title.lower() not in str(clean_list).lower():
                    clean_list.append(info)
                else:
                    if len(each_song['label']) == len(song_title):
                        LOG.info('Removing Duplicate Entries')
                    else:
                        clean_list.append(info)
            return clean_list  # returns a dictionary of matched movies
        else:
            LOG.info('No Songs Found! - ' + str(kodi_payload))
            return None
#    except Exception as e:
#        LOG.info(e)
#        return None
