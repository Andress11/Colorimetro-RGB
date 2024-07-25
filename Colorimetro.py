from functions_gui import Functions

import tkinter as tk
from tkinter import ttk

f = Functions()

root = tk.Tk()
root.geometry('1320x640+15+10')
root.title('Colorimetro RGB - CIE           Developed by HSIA Laboratory V1.0')
root.resizable(width=False, height=False)
root.columnconfigure([1, 2, 3, 4, 5, 6], weight=1)
root.rowconfigure([0,1], weight=1)

Lab_var  = [tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()]
Lab_str = ['L','a','b','C','H']


v_normalizar = tk.IntVar()
v_fondo = tk.IntVar()

style = ttk.Style(root)

opciones_label = ttk.LabelFrame(root, text=' Opciones ')
opciones_label.grid(row = 0, column = 0, sticky='ns', rowspan = 2, padx = 5, pady = 5)

image_label = ttk.LabelFrame(root, text=' Imágenes ')
image_label.grid(row=0, column=1, sticky='nsew', columnspan=6, rowspan=2, pady=5, padx=(0, 5))
image_label.rowconfigure(0, weight=1)
image_label.columnconfigure([0, 1], weight=1)

sample = tk.Frame(image_label, bg='white')
sample.grid(row=0, column=0, sticky='nsew', pady=5, padx=(5, 0))

results = tk.Frame(image_label, bg='white')
results.grid(row=0, column=1, sticky='nsew', pady=5, padx=(0, 5))

Lectura = ttk.LabelFrame(opciones_label, text = ' Lectura de Imagenes ')
Lectura.grid(row = 0, column = 0, sticky='ns', padx = 5, pady = 5)

ttk.Button(Lectura, text = 'Abrir Imagen', width = 25, command = lambda: f.search_image(Lectura, sample)).grid( row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
for i in range(1,3):
    label = ttk.Label(Lectura, text = ' ', width = 20).grid( row = i, column = 0, padx = 5, pady = 5)

Color = ttk.LabelFrame(opciones_label, text = ' Analisis de Color ' )
Color.grid(row = 1, column = 0, sticky = 'ns', padx = 5, pady = 5)

boton_color = ttk.Button(Color, text = 'Realizar análisis', width = 25, command = lambda: f.color_analisis(results, with_reference = v_normalizar.get(),bg_remover = v_fondo.get()))
boton_color.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)

normalizar = ttk.Checkbutton(Color, text = 'Blanco\n  Ref', variable = v_normalizar, onvalue = True, offvalue = False)
normalizar.grid(row = 1, column = 0, padx = (5, 0))

Fondo = ttk.Checkbutton(Color, text = 'Eliminar\n Fondo', variable = v_fondo, onvalue = True, offvalue = False)
Fondo.grid(row = 1, column = 1, padx = (0, 5))

l_resultados = ttk.LabelFrame(opciones_label, text = 'Mapas de Color')
l_resultados.grid(row = 2, column = 0, sticky = 'ns', padx = 5, pady = 5)

map_opciones = tk.Menu()
map_colores = tk.Menu()

map_opciones.add_command(label = 'L', command = lambda: f.set_parametros(plot = 'L'))
map_opciones.add_command(label = 'a', command = lambda: f.set_parametros(plot = 'a'))
map_opciones.add_command(label = 'b', command = lambda: f.set_parametros(plot = 'b'))
map_opciones.add_command(label = 'C', command = lambda: f.set_parametros(plot = 'C'))
map_opciones.add_command(label = 'H', command = lambda: f.set_parametros(plot = 'H'))

map_colores.add_command(label = 0, command = lambda: f.set_parametros(cmap_idx = 0))
map_colores.add_command(label = 1, command = lambda: f.set_parametros(cmap_idx = 1))
map_colores.add_command(label = 2, command = lambda: f.set_parametros(cmap_idx = 2))
map_colores.add_command(label = 3, command = lambda: f.set_parametros(cmap_idx = 3))
map_colores.add_command(label = 4, command = lambda: f.set_parametros(cmap_idx = 4))



lab_seleccionador = ttk.Menubutton(l_resultados, text = 'Parámetros', width = 25, menu = map_opciones, direction = 'below')
lab_seleccionador.grid(row = 0, column = 0, pady = 5)

map_seleccionador = ttk.Menubutton(l_resultados, text = 'Mapa de Color', width = 25, menu = map_colores, direction = 'below')
map_seleccionador.grid(row = 1, column = 0, pady = 5)

actualizar =  ttk.Button(l_resultados, text = 'Actualizar', width = 25, command = lambda: f.update_plot(results))
actualizar.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5)



guardar = ttk.LabelFrame(opciones_label, text = ' Guardado de Imagenes ')
guardar.grid(row = 3, column = 0, sticky = 'ns', padx = 5, pady = 5)


save_img = ttk.Button(guardar, text = 'Guardar imagen png', width = 25, command = lambda: f.save_img_png())
save_img.grid(row = 0, column = 0,columnspan = 5 ,padx = 10, pady = 5)

save_img = ttk.Button(guardar, text = 'Guardar imagen hdr', width = 25, command = lambda: f.save_img([Lab_var[0].get(),Lab_var[1].get(),Lab_var[2].get(),Lab_var[3].get(),Lab_var[4].get()]))
save_img.grid(row = 1, column = 0,columnspan = 5 ,padx = 10, pady = 5)



for j,str_ in enumerate(Lab_str):
    ttk.Checkbutton(guardar, text = str_, variable = Lab_var[j], onvalue = True, offvalue = False).grid(row = 2, column = j, padx = (0, 0))

logo = tk.PhotoImage(file = 'Color_lib/logo.png')
l_logo = tk.Label(opciones_label,image = logo)
l_logo.grid(row = 4, column = 0)



root.mainloop()