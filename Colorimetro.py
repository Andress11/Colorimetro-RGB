from functions_gui import Functions
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sys
import os


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        f = Functions()

        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('1320x640+15+10')
        self.iconbitmap(self.resource_path('imgs/icono-.ico'))
        self.resizable(width=False, height=False)
        self.columnconfigure([1, 2, 3, 4, 5, 6], weight=1)
        self.rowconfigure([0,1], weight=1)

        self.Lab_var  = [tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()]
        self.Lab_str = ['L','a','b','C','H']

        self.v_normalizar = tk.IntVar()
        self.v_fondo = tk.IntVar()

        self.opciones_label = ttk.LabelFrame(self, text=' Opciones ')
        self.opciones_label.grid(row = 0, column = 0, sticky='ns', rowspan = 2, padx = 5, pady = 5)

        self.image_label = ttk.LabelFrame(self, text=' Imágenes ')
        self.image_label.grid(row=0, column=1, sticky='nsew', columnspan=6, rowspan=2, pady=5, padx=(0, 5))
        self.image_label.rowconfigure(0, weight=1)
        self.image_label.columnconfigure([0, 1], weight=1)

        self.sample = tk.Frame(self.image_label, bg='white')
        self.sample.grid(row=0, column=0, sticky='nsew', pady=5, padx=(5, 0))

        self.results = tk.Frame(self.image_label, bg='white')
        self.results.grid(row=0, column=1, sticky='nsew', pady=5, padx=(0, 5))

        self.Lectura = ttk.LabelFrame(self.opciones_label, text = ' Lectura de Imagenes ')
        self.Lectura.grid(row = 0, column = 0, sticky='ns', padx = 5, pady = 5)

        ttk.Button(self.Lectura, text = 'Abrir Imagen', width = 25, command = lambda: f.search_image(self.Lectura, self.sample)).grid( row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
        ttk.Button(self.Lectura, text = 'Tomar foto', width = 25, command = lambda: f.Open_Camera(self.Lectura,self.sample,self.selec_camera.get())).grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

        self.frame_camera = ttk.Frame(self.Lectura)
        self.frame_camera.grid( row = 2, column = 0, padx = 5, pady = 5, sticky = 'nsew')

        self.label_camera = ttk.Label(self.frame_camera, text = 'Selecione Cámara').grid(row = 0, column = 0, padx = 5, sticky = 'nsew')
        self.selec_camera = ttk.Combobox(self.frame_camera,state = 'readonly', values = [0,1,2], width = 3)
        self.selec_camera.grid(row = 0, column = 1, padx = (0,5))
        self.selec_camera.current(0)

        self.Color = ttk.LabelFrame(self.opciones_label, text = ' Analisis de Color ' )
        self.Color.grid(row = 1, column = 0, sticky = 'ns', padx = 5, pady = 5)

        self.boton_color = ttk.Button(self.Color, text = 'Realizar análisis', width = 25, command = lambda: f.color_analisis(self.results, with_reference = self.v_normalizar.get(),bg_remover = self.v_fondo.get()))
        self.boton_color.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)

        self.normalizar = ttk.Checkbutton(self.Color, text = 'Blanco\n  Ref', variable = self.v_normalizar, onvalue = True, offvalue = False)
        self.normalizar.grid(row = 1, column = 0, padx = (5, 0))

        self.Fondo = ttk.Checkbutton(self.Color, text = 'Eliminar\n Fondo', variable = self.v_fondo, onvalue = True, offvalue = False)
        self.Fondo.grid(row = 1, column = 1, padx = (0, 5))

        self.l_resultados = ttk.LabelFrame(self.opciones_label, text = 'Mapas de Color')
        self.l_resultados.grid(row = 2, column = 0, sticky = 'ns', padx = 5, pady = 5)

        self.map_opciones = tk.Menu()
        self.map_colores = tk.Menu()

        self.map_opciones.add_command(label = 'L', command = lambda: f.set_parametros(plot = 'L'))
        self.map_opciones.add_command(label = 'a', command = lambda: f.set_parametros(plot = 'a'))
        self.map_opciones.add_command(label = 'b', command = lambda: f.set_parametros(plot = 'b'))
        self.map_opciones.add_command(label = 'C', command = lambda: f.set_parametros(plot = 'C'))
        self.map_opciones.add_command(label = 'H', command = lambda: f.set_parametros(plot = 'H'))

        self.map_colores.add_command(label = 0, command = lambda: f.set_parametros(cmap_idx = 0))
        self.map_colores.add_command(label = 1, command = lambda: f.set_parametros(cmap_idx = 1))
        self.map_colores.add_command(label = 2, command = lambda: f.set_parametros(cmap_idx = 2))
        self.map_colores.add_command(label = 3, command = lambda: f.set_parametros(cmap_idx = 3))
        self.map_colores.add_command(label = 4, command = lambda: f.set_parametros(cmap_idx = 4))

        self.lab_seleccionador = ttk.Menubutton(self.l_resultados, text = 'Parámetros', width = 25, menu = self.map_opciones, direction = 'below')
        self.lab_seleccionador.grid(row = 0, column = 0, pady = 5)

        self.map_seleccionador = ttk.Menubutton(self.l_resultados, text = 'Mapa de Color', width = 25, menu = self.map_colores, direction = 'below')
        self.map_seleccionador.grid(row = 1, column = 0, pady = 5)

        self.actualizar =  ttk.Button(self.l_resultados, text = 'Actualizar', width = 25, command = lambda: f.update_plot(self.results))
        self.actualizar.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5)

        self.guardar = ttk.LabelFrame(self.opciones_label, text = ' Guardado de Imagenes ')
        self.guardar.grid(row = 3, column = 0, sticky = 'ns', padx = 5, pady = 5)

        self.save_img = ttk.Button(self.guardar, text = 'Guardar imagen png', width = 25, command = lambda: f.save_img_png())
        self.save_img.grid(row = 0, column = 0,columnspan = 5 ,padx = 10, pady = 5)

        self.save_img = ttk.Button(self.guardar, text = 'Guardar imagen hdr', width = 25, command = lambda: f.save_img([self.Lab_var[0].get(),self.Lab_var[1].get(),self.Lab_var[2].get(),self.Lab_var[3].get(),self.Lab_var[4].get()]))
        self.save_img.grid(row = 1, column = 0,columnspan = 5 ,padx = 10, pady = 5)

        for j,str_ in enumerate(self.Lab_str):
            ttk.Checkbutton(self.guardar, text = str_, variable = self.Lab_var[j], onvalue = True, offvalue = False).grid(row = 2, column = j, padx = (0, 0))

        self.logo = tk.PhotoImage(file = self.resource_path('imgs/logo.png'))
        self.l_logo = tk.Label(self.opciones_label,image = self.logo)
        self.l_logo.grid(row = 4, column = 0)

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path,relative_path)
    

class Login(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        hRoot = 300
        wRoot = 450
        hTotal  = self.winfo_screenheight()
        wTotal = self.winfo_screenwidth()
        wPosition = round(wTotal/2 - wRoot/2)
        hPosition = round(hTotal/2 - wRoot/2)

        self.loged = 0

        self.geometry(f'{wRoot}x{hRoot}+{wPosition}+{hPosition}')
        self.config(background = 'white')
        self.iconbitmap(self.resource_path('imgs/icono-.ico'))
        self.title('Color - Im')
        self.rowconfigure([0,1,2,3,4,5], weight=1)
        self.columnconfigure([0,1], weight=1)


        self.title_label = ttk.Label(self, text = 'Inicio de Sesión \n Color-Im', justify = 'center' ,font = ('TimesNewRoman', 20, 'bold'), background = 'white')
        self.title_label.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 5)

        self.usuario_label = ttk.Label(self, text = ' Usuario: ', justify = 'left', font = ('TimesNewRoman', 12), background = 'white')
        self.usuario_label.grid(row = 1, column = 1, sticky = 'nsew', padx = 10, pady = (20,5))

        self.usuario_get = ttk.Entry(self, font = ('TimesNewRoman', 10))
        self.usuario_get.grid(row = 2, column = 1,sticky = 'nsew' ,padx = 10, pady = 5)

        self.constraseña_label = ttk.Label(self, text = ' Contraseña: ', justify = 'left', font = ('TimesNewRoman', 12), background = 'white')
        self.constraseña_label.grid(row = 3, column = 1, sticky = 'nsew', padx = 10, pady = 5)

        self.constraseña_get = ttk.Entry(self, font = ('TimesNewRoman', 10), show = '*')
        self.constraseña_get.grid(row = 4, column = 1,sticky  = 'nsew' ,padx = 10, pady = 5)

        self.loggin_button = ttk.Button(self, text = 'Iniciar sesion', command = lambda: self.log(user = self.usuario_get.get(), password = self.constraseña_get.get()))
        self.loggin_button.grid(row = 5, column = 1, padx = 10, pady = (20,10), sticky = 'nsew')

        self.logo = tk.PhotoImage(file = self.resource_path('imgs/logo.png'))
        self.l_logo = tk.Label(self, text = 'ptm', image = self.logo, justify = 'center', anchor = 'center', background = 'white')
        self.l_logo.grid(row = 0, column = 0, sticky = 'nsew', rowspan = 6, pady = 5, padx = (5,0))


    def log(self, user, password):

        if user == 'user' and password == '1234':
            mb.showinfo("Login Successful",
                                       f'Bienvenido {user}')

            top.destroy()
            root = MainApp()
            root.title('Color- Im [RGB - CIE]      Developed by HSIA Laboratory V1.0')
            root.mainloop()
        else:
            mb.showerror('Error', 'CONTRASEÑA INCORRECTA')

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path,relative_path)

top = Login()
top.title('Color- Im [RGB - CIE]      Developed by HSIA Laboratory V1.0')
top.mainloop()