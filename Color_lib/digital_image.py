import cv2 as cv
import os


class Digital_Image:

    def __init__(self,path = None, array = None):
        
        if array is None and path is not None:
            self.properties = self._read_properties(path = path)

        if path is None and array is not None:
            self.properties = self._read_properties(array = array)

        else:
            print('ERROR')

    def _read_properties(self,path = None, array = None):
        
        if path is not None and array is None:
            image_data_rgb = cv.imread(path)
            name = os.path.basename(path)[:-4]
        if path is None and array is not None:
            image_data_rgb = array
            name = 'Foto tomada'    

        try:
            rows, columns, bands = image_data_rgb.shape
        except ValueError:
            print('Ruta no valida')
        class P:
            pass

        properties = P()

        properties.array_data = image_data_rgb[...,::-1]
        properties.name = name
        properties.n_rows = rows
        properties.n_columns = columns
        properties.n_bands = bands 
        properties.shape = (rows,columns)

        return properties