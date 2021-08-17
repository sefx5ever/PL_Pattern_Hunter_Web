from numpy.lib.shape_base import array_split
from tensorflow import keras
import numpy as np

class PatternHunterModel:
    def __init__(self):
        self.model = keras.models.load_model('./API/Channel_Doc/model.h5')

    def ts2gasf(self,ts, max_v, min_v):
        '''
        Args:
            ts (numpy): (N, )
            max_v (int): max value for normalization
            min_v (int): min value for normalization
        Returns:
            gaf_m (numpy): (N, N)
        '''
        # Normalization : 0 ~ 1
        if max_v == min_v:
            gaf_m = np.zeros((len(ts), len(ts)))
        else:
            ts_nor = np.array((ts-min_v) / (max_v-min_v))
            # Arccos
            ts_nor_arc = np.arccos(ts_nor)
            # GAF
            gaf_m = np.zeros((len(ts_nor), len(ts_nor)))
            for r in range(len(ts_nor)):
                for c in range(len(ts_nor)):
                    gaf_m[r, c] = np.cos(ts_nor_arc[r] + ts_nor_arc[c])
        return gaf_m

    def get_gasf(self,arr):
        '''Convert time-series to gasf    
        Args:
            arr (numpy): (N, ts_n, 4)
        Returns:
            gasf (numpy): (N, ts_n, ts_n, 4)
        Todos:
            add normalization together version
        '''
        arr = arr.copy()
        gasf = np.zeros((arr.shape[0], arr.shape[1], arr.shape[1], arr.shape[2]))
        for i in range(arr.shape[0]):
            for c in range(arr.shape[2]):
                each_channel = arr[i, :, c]
                c_max = np.amax(each_channel)
                c_min = np.amin(each_channel)
                each_gasf = self.ts2gasf(each_channel, max_v=c_max, min_v=c_min)
                gasf[i, :, :, c] = each_gasf
        return gasf

    def predict(self,gaf):
        gaf = np.expand_dims(gaf,axis=0)
        pred = np.argmax(self.model.predict(gaf),axis=1)
        return pred

    def reshape_to_gasf(self,arr):
        return self.get_gasf(np.array(arr).reshape(1,10,4))