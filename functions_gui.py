from Color_lib.digital_image import Digital_Image
from Color_lib.color_preprocess import Image
from Color_lib.color_transformation import Color_transformation

import numpy as np
import tkinter as tk
import spectral.io.envi as envi
from tkinter import filedialog

import matplotlib.pyplot as plt
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
            print('SELECIONE UNA IMAGEN')
            return
        else: 
            img = Digital_Image(path_image)
            img_properties = img.properties
            properties = [img_properties.name, img_properties.shape, img_properties.n_rows*img_properties.n_columns]
            self.LabelGen_Properties(master_properties,properties)
            self.plot(master_plot, img_properties.array_data, title = properties[0], colorbar = False)
            self.img = img


    def clean_frame(self, frame, step):
    
        for widget in frame.winfo_children()[step:]:
            widget.destroy()


    def LabelGen_Properties(self, master, properties):

        self.clean_frame(master, step = 1)
        Frames = ['Nombre', 'Dimensión']

        for i, frame in enumerate(Frames):
            text = f'{frame}:  {properties[i]}'
            Label =  tk.Label(master, text = text, width = 20, justify = 'left').grid( row = i+1, column = 0, padx = (0,5), pady = 5)

    def set_parametros(self,plot = None,cmap_idx = None):

        
        cmaps = ['viridis', 'gray', 'hsv', 'gist_rainbow', 'nipy_spectral']


        if plot is None:
            self.plot_parametros['cmap'] = cmaps[cmap_idx]

        if cmap_idx is None:
            self.plot_parametros['plot'] = plot

    def plot(self, master, img_, title: str, colorbar = False,cmap = 'viridis'):
            
            self.clean_frame(master,step = 0)
            fig = Figure(figsize = (7,6),dpi = 78)
            
            ax =  fig.add_subplot(111)
            im = ax.imshow(img_)
            ax.set_title(title)
            ax.axis('off')
            if colorbar is True:
                im = ax.imshow(img_,cmap=cmap)
                fig.colorbar(im,ax=ax)

            canvas = FigureCanvasTkAgg(fig, master = master) 
            canvas.draw()
            tk_widget = canvas.get_tk_widget()
            tk_widget.pack(side = 'left', fill = 'y', expand = False)

    def color_analisis(self, frame_image, with_reference: bool, bg_remover: bool):

        if self.img is None:
            print('PRIMERO SELECIONE UNA IMAGEN')
        else:
            title = f'Mapa de Color: {self.plot_parametros['plot']}'
            img_normal, white_mean,bg_mask = Image(self.img)._normalize(white_limit = 200, with_reference = with_reference, bg_remover = bg_remover)
            color = Color_transformation(img_normal).color
            self.plot(frame_image,color[self.plot_parametros['plot']], title, colorbar = True, cmap = self.plot_parametros['cmap'])  
            self.color = color    

    def update_plot(self,frame_image):

        if self.color is None:
            print('DEBE REALIZAR ANALISIS PRIMERO')
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
            print('NO HAY INFORMACIÓN PARA GUARDAR')
            # DISEÑAR PESTAÑA DESPLEGABLE
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
            print('NO HAY DATOS PARA GUARDAR')
            return
            
        save_path = filedialog.asksaveasfilename()
        if len(save_path) == 0:
            return
        else:
            fig = Figure(figsize = (12,8),dpi = 90)
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
            #plt.savefig(save_path)
