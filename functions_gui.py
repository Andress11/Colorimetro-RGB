from Color_lib.digital_image import Digital_Image
from Color_lib.color_preprocess import Image
from Color_lib.color_transformation import Color_transformation

import numpy as np
import cv2 as cv
import tkinter as tk
import spectral.io.envi as envi
from tkinter import filedialog
from tkinter import messagebox as mb

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Functions:

    def __init__(self):
        self.img = None
        self.color = None

        self.plot_parametros = {'plot': 'L',
                                'cmap': 'viridis'}

    def search_image(self,master_properties, master_plot):

        path_image = tk.filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if len(path_image) == 0:
            mb.showerror('Error', 'ERROR EN LA SELECCION DE UNA IMAGEN')
            return
        else: 
            img = Digital_Image(path = path_image)
            img_properties = img.properties
            properties = [img_properties.name, img.properties.shape]
            self.LabelGen_Properties(master_properties,properties[1])
            self.plot(master_plot, img_properties.array_data, title = properties[0], colorbar = False)
            self.img = img

    def clean_frame(self, frame, step):
    
        for widget in frame.winfo_children()[step:]:
            widget.destroy()

    def LabelGen_Properties(self, master, propertie):

        self.clean_frame(master, step = 2)
        

        text = f'Tamaño:  {propertie}'
        tk.Label(master, text = text, width = 20, justify = 'left').grid( row = 2, column = 0, padx = (0,5), pady = 5)

    def set_parametros(self,plot = None,cmap_idx = None):
        
        cmaps = ['viridis', 'gray', 'hsv', 'gist_rainbow', 'nipy_spectral']

        if plot is None:
            self.plot_parametros['cmap'] = cmaps[cmap_idx]

        if cmap_idx is None:
            self.plot_parametros['plot'] = plot

    def plot(self, master, img_, title: str, colorbar = False,cmap = 'viridis'):
            
            self.clean_frame(master,step = 0)
            if colorbar is True:
                fig = Figure(figsize = (8,7),dpi = 78)
                ax =  fig.add_subplot(111)
                im = ax.imshow(img_,cmap=cmap)
                fig.colorbar(im,ax=ax)
            else:
                fig = Figure(figsize = (7,6),dpi = 78)
                ax =  fig.add_subplot(111)
                im = ax.imshow(img_)
            ax.set_title(title)
            ax.axis('off')
            
            canvas = FigureCanvasTkAgg(fig, master = master) 
            canvas.draw()
            tk_widget = canvas.get_tk_widget()
            tk_widget.pack(side = 'left', fill = 'y', expand = False)

    def color_analisis(self, frame_image, with_reference: bool, bg_remover: bool):

        if self.img is None:
            mb.showerror('Error', 'SELECIONE UNA IMAGEN')
        else:
            title = f'Mapa de Color: {self.plot_parametros['plot']}'
            img_normal, white_mean,bg_mask = Image(self.img)._normalize(white_limit = 200, with_reference = with_reference, bg_remover = bg_remover)
            color = Color_transformation(img_normal).color
            self.plot(frame_image,color[self.plot_parametros['plot']], title, colorbar = True, cmap = self.plot_parametros['cmap'])  
            self.color = color    

    def update_plot(self,frame_image):

        if self.color is None:
            mb.showerror('Error', 'DEBE REALIZAR ANALISIS PRIMERO')
            return 
        else:
            title = f'Mapa de Color: {self.plot_parametros['plot']}'
            parametro_color = self.plot_parametros['plot']
            cmap = self.plot_parametros['cmap']
            self.plot(frame_image, self.color[parametro_color], title, colorbar = True, cmap = cmap)

    def save_img(self,save_parameters: list):

        write_data = [[],[],[]]
        bands_names = ['L', 'a', 'b','C','H']
        descriptions = ['Brillo', 'A','B','Croma', 'Tono']

        if self.color is None or save_parameters == [0,0,0,0,0]:
            mb.showerror('Error', 'NO HAY INFORMACION PARA GUARDAR')
        else:
            data = self.color
            save_path = filedialog.asksaveasfilename()
            if len(save_path) == 0:
                return
            else:
                for i in range(len(save_parameters)):
                    
                    write_data[0].append(data[bands_names[i]]) if save_parameters[i] == 1 else None
                    write_data[1].append(bands_names[i]) if save_parameters[i] == 1 else None
                    write_data[2].append(descriptions[i]) if save_parameters[i] == 1 else None

                write_data_ = np.stack(write_data[0],axis= 2)
                
                hdr_metadata = {
                    'lines': write_data_.shape[1],
                    'samples': write_data_.shape[2],
                    'bands': write_data_.shape[0],
                    'data type': str(write_data_.dtype),
                    'interleave': 'bsq',
                    'byte order': 0,
                    'band names': write_data[1],
                    'descriptions': write_data[2],
                    'data ignore value': -999.0
                    }
                hdr_path_out = save_path + ".hdr"
                envi.save_image(hdr_path_out, write_data_, metadata=hdr_metadata,ext = '.raw')

    def save_img_png(self):

        bands_names = ['L', 'a', 'b','C','H']
        color = self.color
        if color is None:
            mb.showerror('Error', 'NO HAY INFORMACION PARA GUARDAR')
            return
            
        save_path = filedialog.asksaveasfilename()
        if len(save_path) == 0:
            return
        else:
            fig = Figure(figsize = (12,8),dpi = 300)
            ax =  fig.add_subplot(2,3,1)
            ax.set_title('Imagen')
            ax.imshow(self.img.properties.array_data)
            ax.axis('off')

            for i,parametro in enumerate(bands_names):
                ax =  fig.add_subplot(2,3,i+2)
                ax.set_title(f'Parametro {parametro}')
                im = ax.imshow(color[parametro], cmap = self.plot_parametros['cmap'])
                fig.colorbar(im, ax = ax)
                ax.axis('off')

            fig.savefig(save_path)
    
    def Open_Camera(self,master_properties ,master_plot,cap_select):
    
        cap = cv.VideoCapture(int(cap_select))
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1024)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)

        while True:

            ret, frame = cap.read()
            frame = cv.flip(frame,1)

            frame_show = cv.resize(frame, (640,480))
            cv.imshow('c para capturar - q para salir', frame_show)

            if cv.waitKey(1) == 99:
                self.img = Digital_Image(array = frame)
                break

            if cv.waitKey(1) == 113:
                break
  
        cap.release()
        cv.destroyAllWindows()

        if self.img is not None:
            img_properties = self.img.properties
            properties = [img_properties.name, img_properties.shape]
            self.LabelGen_Properties(master_properties,properties[1])
            self.plot(master_plot, img_properties.array_data, title = properties[0], colorbar = False)

        else:
            mb.showerror('Error', 'IMAGEN NO CAPTURADA')