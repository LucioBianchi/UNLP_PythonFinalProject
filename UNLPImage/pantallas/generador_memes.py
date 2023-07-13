import PySimpleGUI as sg
from pantallas import constantes as const, seleccionador_memes
from . funciones_comunes import boton_volver, actualizar_logs
import os
import json
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap


def actualizar_botones(template,window):
    """
    Hace visible los botones
    """
    for i in range(len(template["text_boxes"])):
        window[f"-TEXTO {i + 1}-"].update(visible=True)
        window[f"-INPUT {i + 1}-"].update(visible=True)


def actualizar_texto(window,template,ruta,values):
    """
    Actualiza el texto en el meme
    """
    img = Image.open(ruta)
    draw = ImageDraw.Draw(img)
    index = 1
    for box in template["text_boxes"]:
        x1 = box["top_left_x"]
        y1 = box["top_left_y"]
        x2 = box["bottom_right_x"]
        y2 = box["bottom_right_y"]
        text_content = window[f"-INPUT {index}-"].get()
        width_text = 15
        lines = textwrap.wrap(text_content,width= width_text)
        text_color = (0, 0, 0)
        text = """"""
        #Creo el texto final entre comillas triples agregando un salto de linea
        for line in lines:
            text += f"""{line}\n"""
        #Le saco el ultimo \n
        text = text[:-1]
        w, h = draw.multiline_textsize(text)
        font_filename = f"{values['-LISTA TEMPLATE-']}.ttf"
        font_size = 13
        font = ImageFont.truetype(font_filename,font_size)
        while(y2 - y1 < h):
            font_size -= 1
            width_text += 3
            lines = textwrap.wrap(text_content,width= width_text)
            text = """"""
            #Creo el texto final entre comillas triples agregando un salto de linea
            for line in lines:
                text += f"""{line}\n"""
            #Le saco el ultimo \n
            text = text[:-1]
            font = ImageFont.truetype(font_filename,font_size)
            w,h= draw.multiline_textsize(text, font=font)
        x = (x2 - x1 - w)/2 + x1
        y = (y2 - y1 - h)/2 + y1
        draw.multiline_text((x,y), text, fill=text_color,font= font)
        index += 1 
    img.thumbnail((280,280))
    image_tk = ImageTk.PhotoImage(img)
    window["-IMAGE-"].update(data=image_tk)
    return img


def actualizar_imagen(element,ruta):
    '''
    Actualiza la imagen.
    '''
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","templates_meme",ruta)
    image = Image.open(ruta)
    image.thumbnail((280,280))
    image_tk = ImageTk.PhotoImage(image)
    element.update(data=image_tk)

def count_files_with_base_name(folder_path, base_name):
    """
    Devuelve la cantidad de archivos con el nombre base pasado como parametro"
    """
    file_names = os.listdir(folder_path)
    count = sum(1 for file_name in file_names if file_name.startswith(base_name))
    return count

def increment_file_name(file_path, value_to_add):
    """
    Devuelve el nombre que se le pone al meme a guardar, aumentanto en uno segun la cantidad que se le pasa como parametro"
    """
    base_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(base_name)
    print(base_name)
    new_base_name = base_name + str(value_to_add + 1)
    new_file_path = os.path.join(os.path.dirname(file_path), new_base_name + extension)
    print(new_file_path)
    return new_file_path

def guardar_imagen(image,dir_memes,template):
    """
    Guarda la imagen
    """
    path = os.path.join(dir_memes, template['image'])
    x = count_files_with_base_name(dir_memes,os.path.splitext(template['image'])[0])
    path = increment_file_name(path, x)
    image.save(path)
    return os.path.basename(path)

def generar_texto_valores(template,values):
    """
    Genera un unico texto con los input de texto
    """
    aux_text = ""
    for i in range(len(template["text_boxes"])):
        aux_text += values[f"-INPUT {i+1}-"] + ";"
    return aux_text[:-1]

def crear_ventana(usuario,template,dir_memes):
    '''
    Crea y muestra la ventana de generador de memes
    '''
    col1 = [
        [sg.Text("Seleccionar fuente")],
        [sg.Combo(["arial","calibri","couri","segoesc","times","comic","consola"],size=(15, 5),default_value="arial",key=("-LISTA TEMPLATE-"),enable_events=True,)],
        [sg.Text("Texto1", visible=False, key="-TEXTO 1-")],
        [sg.Input(visible=False, key="-INPUT 1-")],
        [sg.Text("Texto2", visible=False, key="-TEXTO 2-")],
        [sg.Input(visible=False, key="-INPUT 2-")],
        [sg.Text("Texto3", visible=False, key="-TEXTO 3-")],
        [sg.Input(visible=False, key="-INPUT 3-")],
        [sg.Text("Texto4", visible=False, key="-TEXTO 4-")],
        [sg.Input(visible=False, key="-INPUT 4-")],
        
    ]
    
    col2 = [
        [sg.Image(key="-IMAGE-")]
    ]

    layout = [
                
                [sg.Push(), sg.Button("Volver", key="-VOLVER-", border_width=0)],
                [sg.Column(col1, expand_y=True,expand_x=True,size=(250,200)),
                 sg.Column(col2)],
                [sg.Button("Agregar",key="-AGREGAR-",button_color="#65b2db",pad=(10,(10,20))),sg.Push(),sg.Button("Generar", key="-GENERAR-", button_color="#65b2db",pad=(10,(10,20)))],    
            ]

    window = sg.Window("Generador memes", layout,finalize=True,size=const.TAM_VENTANAS)
    boton_volver(window)
    actualizar_botones(template,window)
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","templates_meme",template["image"])
    actualizar_imagen(window["-IMAGE-"],ruta)
    list_txt = []
    while True:
        
        event, values = window.read()

        if event == "-VOLVER-":
            window.close()
            seleccionador_memes.crear_ventana(usuario,dir_memes)

        if event == "-AGREGAR-":
           img_original = actualizar_texto(window,template,ruta,values)

        if event == "-GENERAR-":
            img_nombre = guardar_imagen(img_original,dir_memes,template)
            list_txt = generar_texto_valores(template,values)
            actualizar_logs("nuevo_meme",usuario,img_nombre,list_txt)

        if event == sg.WIN_CLOSED:
            break
    window.close()