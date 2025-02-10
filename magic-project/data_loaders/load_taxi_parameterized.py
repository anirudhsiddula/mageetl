import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(data, *args, **kwargs):
    
    taxi_dtypes = {
        'VendorID': 'Int64',
        'store_and_fwd_flag': 'str',
        'RatecodeID': 'Int64',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'ehail_fee': 'float64',
        'improvement_surcharge': 'float64',
        'total_amount': 'float64',
        'payment_type': 'float64',
        'trip_type': 'float64',
        'congestion_surcharge': 'float64'
    }

    parse_dates_green_taxi = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    parse_dates_yellow_taxi = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    color = next(iter(data))

    taxi_date_columns = parse_dates_green_taxi if color == 'green' else parse_dates_yellow_taxi

    df = pd.read_csv(next(iter(data.values())), sep = ',', compression = 'gzip', \
                        dtype = taxi_dtypes, \
                        parse_dates = taxi_date_columns)
    
    # df = df.rename(columns={'tpep_pickup_datetime': 'lpep_pickup_datetime', 'tpep_dropoff_datetime': 'lpep_dropoff_datetime'}) if color == 'yellow' else df
    
    return [df, color]
