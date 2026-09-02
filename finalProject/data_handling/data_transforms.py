from abc import ABC, abstractmethod
import xarray as xr

class Pipeline(object):
    def __init__(self, config:dict) -> None:
        pass

    def __call__(self, ds:xr.Dataset):
        pass

class DataTransform(ABC):
    @abstractmethod
    def forward(self, ds:xr.Dataset) -> xr.Dataset:
        raise NotImplementedError()

class TimeFilter(DataTransform):
    def __init__(self, config:dict):
        self.filter_months = None
        self.train_start = None
        self.test_end = None
        if('FILTER_MONTHS' in config.keys() and config['FILTER_MONTHS'] is not None):
            self.filter_months = config['FILTER_MONTHS']
        if('TRAIN_START' in config.keys() and config['TRAIN_START'] is not None):
            self.train_start = config['TRAIN_START']
        if('TEST_END' in config.keys() and config['TEST_END'] is not None):
            self.test_end = config['TEST_END']
    def forward(self, ds:xr.Dataset) -> xr.Dataset:
        if(self.filter_months is not None):
            ds = ds.where(ds['time.month'].isin(self.filter_months), drop=True)
        if(self.train_start is not None):
            ds = ds.where(ds['time'] >= self.train_start, drop=True)
        if(self.test_end is not None):
            ds = ds.where(ds['time'] < self.test_end, drop=True)
        return ds

class SpatialFilter(DataTransform):
    def __init__(self, config:dict):
        self.stride_x = None
        self.stride_y = None
        if('LAT_INT' in config.keys() and config['LAT_INT'] is not None):
            self.stride_x = config['LAT_INT']
        if('LON_INT' in config.keys() and config['LON_INT'] is not None):
            self.stride_y = config['LON_INT']
    def forward(self, array:np.array):
        assert len(array.shape) == 4 # time, lat, lon, var
        if(self.stride_x is not None):
            array = array[:, ::self.stride_x, :, :]
        if(self.stride_y is not None):
            array = array[:, :, ::self.stride_y, :]
        return array

class GenerateLandMask(DataTransform):
    def __init__(self, config:dict):
        self.gen_land_mask = False
        if('GENERATE_LAND_MASK' in config.keys() and config['GENERATE_LAND_MASK']):
            self.gen_land_mask = True
    def forward(self, array:np.array):
        assert len(array.shape) == 4 # time, lat, lon, var
        if(self.gen_land_mask):
            land_mask = np.where(np.isnan(sample), 0, 1).astype(np.int8)
            land_mask = np.expand_dims(land_mask, axis=-1)
            return array
        return array
        
