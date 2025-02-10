if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def generatetaxiurls(*args, **kwargs):
    colors = kwargs['taxis']
    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
    url_list = [[{color: f"{base_url}{color}/{color}_tripdata_2021-01.csv.gz"} for color in colors]]
    return url_list