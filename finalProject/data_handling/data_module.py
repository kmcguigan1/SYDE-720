import os
import xarray as xr

class DataModule(object):
    def __init__(self, config:dict) -> None:
        self.data_file = os.path.join(DATA_PATH, config['DATA_FILE'])
        self.batch_size = config['BATCH_SIZE']
        self.time_steps_in = config["TIME_STEPS_IN"]
        self.time_steps_out = config["TIME_STEPS_OUT"]
        self.time_int = config["TIME_INT"]
    
    def load_data(self):
        ds = xr.open_dataset(os.path.join('data', self.data_file))

def filter_months(ds:xr.Dataset, filter_months:list=None):
    if(filter_months is not None):
        ds = ds.where(ds['time.month'].isin(config['FILTER_MONTHS']), drop=True)
    return ds

def filter_spatially(ds:xr.Dataset, x_stride:int=None, y_stride:int=None):
    if(x_stride is not None):
        all_latitudes = ds['latitude'].values
        all_latitudes = all_latitudes[::x_stride]
        ds = ds.where(ds['latitude'].isin(all_latitudes), drop=True)
    if(y_stride is not None):
        all_longitudes = ds['longitude'].values
        all_longitudes = all_longitudes[::y_stride]
        ds = ds.where(ds['longitude'].isin(all_longitudes), drop=True)

def generate_land_mask(ds:xr.Dataset, )