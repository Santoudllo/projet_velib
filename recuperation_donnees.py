import requests
import pandas as pd
from time import gmtime, strftime
def getData():
    #https://data.opendatasoft.com/explore/dataset/velib-disponibilite-en-temps-reel%40parisdata/api/
    nbrows = 1500
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel%40parisdata&rows=" + str(nbrows) + "&facet=overflowactivation&facet=creditcard&facet=kioskstate&facet=station_state"
    print(url)
    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    return resp.json()
    data = getData()