import numpy as np

from .utils import (
    unfolding,
    folding
)


class Image:

    def __init__(self, Image):
        global array_data
        array_data = Image.properties.array_data


    def _normalize(self, white_limit, with_reference, bg_remover):

        rows, columns, bands = array_data.shape
        data_array_2D = unfolding(array_data)


        if with_reference == 1:

            std_per_pixel = data_array_2D.std(axis = 1)
            
            mean_std_per_pixel = std_per_pixel.mean()
            std_std_per_pixel =  std_per_pixel.std()
            std_limit = mean_std_per_pixel + 3 * np.std( std_per_pixel <= 0.5*std_std_per_pixel)

            mask_bg = std_per_pixel <= std_limit
            bg = data_array_2D[mask_bg]
            bg_mean = bg.mean(axis = 1)

            mask_white = bg_mean >= white_limit
            white_mean = bg[mask_white].mean( axis = 0)
    
        else:
            white_mean = np.array([255,255,255], dtype = np.uint8)

        if bg_remover == 1:
            from rembg import remove
            bg_mask = np.clip(remove(array_data, post_process_mask = True, only_mask = True),0,1)
            normal_array_2D = np.zeros_like(data_array_2D)
            idx = bg_mask.reshape(-1) > 0
            normal_array_2D[idx] = data_array_2D[idx]
        
        else: 
            normal_array_2D = np.copy(array_data)
            bg_mask = None

        normal_array_2D = normal_array_2D/white_mean
        normal_array = np.clip(folding(normal_array_2D,rows,columns,bands),0,1)

        return normal_array, white_mean,bg_mask
