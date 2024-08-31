import numpy as np
from .constans import *

from .utils import (
    unfolding,
    folding
)

class Color_transformation:

    def __init__(self,image):
        rows, columns, bands = image.shape
        self.properties = {'rows': rows,
                           'columns': columns,
                           'bands': bands,
                           'shape': (rows,columns,bands)}
        _Lab = self._RGB2Lab(image, fold = True)
        _Lch = self._Lab2Lch(_Lab,fold = True)
    
        self.color = {'L': _Lab[:,:,0],
                      'a': _Lab[:,:,1],
                      'b': _Lab[:,:,2],
                      'C': _Lch[:,:,1],
                      'H': _Lch[:,:,2],}


    def _companding_sRGB(self,rgb_values: np.ndarray):
        
        idx = rgb_values <= 0.04045

        rgb_values[idx] =  rgb_values[idx]/(12.92)
        rgb_values[~idx] = ((rgb_values[~idx]+0.055)/1.055)**2.4

        return rgb_values

    def _RGB2Lab(self,array_3D_RGB: np.ndarray, fold = False):

        array_2D_RGB = unfolding(array_3D_RGB)
        array_2D_RGB = self._companding_sRGB(array_2D_RGB)

        xyz_linear = np.dot(array_2D_RGB, RGB_LAB_MATRIX_D65.T)
        xyz_normalized = xyz_linear / XYZ_D65_STANDAR_ILUMINATION
        linear_condition = xyz_normalized > EPSILON
        xyz_final = np.where(linear_condition, xyz_normalized ** (1 / 3), (xyz_normalized * 903.3 + 16) / 116)

        L = 116 * xyz_final[:, 1] - 16
        L = np.clip(L, 0, 100)
        a = 500 * (xyz_final[:, 0] - xyz_final[:, 1])
        b = 200 * (xyz_final[:, 1] - xyz_final[:, 2])

        Lab = np.column_stack((L, a, b))
        if fold is True:
            Lab = folding(Lab,self.properties['rows'],self.properties['columns'],self.properties['bands'])

        return Lab
    
    def _Lab2Lch(self, img_Lab: np.ndarray,fold = False):

        Lab = unfolding(img_Lab)

        L, a, b = Lab[:, 0], Lab[:, 1], Lab[:, 2]
        
        c = np.sqrt(a**2 + b**2)
        h = np.arctan2(b, a) * (180 / np.pi)
        h[h < 0] += 360

        Lch = np.column_stack((L, c, h))
        if fold is True:
            Lch = folding(Lch,self.properties['rows'],self.properties['columns'],self.properties['bands'])
       
        return Lch