import calendar
from collections import Counter
import json
import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from wordcloud import WordCloud

# Configuraciones de la pagina
st.set_page_config(
page_title="Análisis de datos",
page_icon=":bar_chart:",
layout="centered",
initial_sidebar_state="expanded"
)

ruta_archivo_logs = os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","logs.csv")
# Carga el archivo en un DataFrame de Pandas
datos_logs = pd.read_csv(ruta_archivo_logs)

ruta_archivo_img = os.path.join(os.path.dirname(os.path.dirname(__file__)),"datos_app","img_data.csv")
# Carga el archivo en un DataFrame de Pandas
datos_img = pd.read_csv(ruta_archivo_img)


def grafico_pastel_img(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de torta"):
        st.write("El gráfico de torta muestra la distribución de los tipos de imágenes presentes en los datos proporcionados.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Se utiliza el método value_counts() para contar la frecuencia de cada tipo de imagen.")
        st.write("Luego se obtienen los porcentajes.")
        st.write("Una vez calculados los porcentajes, se genera el gráfico de torta utilizando la función pie() de ***Matplotlib***.")
        st.write("Finalmente, se agrega una etiqueta al costado del gráfico que muestra los tipos de imagen junto con su porcentaje correspondiente.")
        
    #Copia del dataframe
    datosCopia = datos.copy()
    # Calcular los porcentajes según el tipo de imagen
    imagen_tipos = datosCopia['tipo'].value_counts()
    total_img = imagen_tipos.sum()
    porcentajes = (imagen_tipos / total_img) * 100

    # Generar el gráfico de torta
    fig, ax = plt.subplots()
    pie = ax.pie(porcentajes, autopct='%1.1f%%', startangle=90)
    ax.set_title('Tipos de imágenes')
    
    # Agregar una etiqueta con cada color al costado del gráfico
    ax.legend(pie[0], porcentajes.index, title='Tipo de imagen', loc='center left', bbox_to_anchor=(1, 0.5))

    st.pyplot(fig) 
      
def grafico_dispersion(datos):
    
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de dispersión"):
        st.write("El gráfico de dispersión muestra la relación entre el ancho y el alto de las imágenes.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("A continuación, se extrae el ancho y el alto de la resolución de cada imagen.")
        st.write("Esto se logra dividiendo la cadena de resolución utilizando split() y convirtiendo los valores a enteros.")
        st.write("Se calculan los valores máximos de ancho y alto para determinar el rango del gráfico.")
        st.write("Finalmente, se genera el gráfico de dispersión utilizando la función scatter() de ***Matplotlib***.")
    
    #Copia del dataframe
    datosCopia = datos.copy()
    # Extraer el ancho y el alto de la resolución
    datosCopia[['ancho', 'alto']] = datosCopia['resolucion'].str.split('x', expand=True).astype(int)

    # Calcular los valores máximos de ancho y alto
    max_width = datosCopia['ancho'].max()
    max_height = datosCopia['alto'].max()

    # Generar un gráfico de dispersión, fig representa la figura y ax los ejes.
    fig, ax = plt.subplots()
    ax.scatter(datosCopia['ancho'], datosCopia['alto'])
    ax.set_xlabel('Ancho')
    ax.set_ylabel('Alto')
    ax.set_title('Relación entre ancho y alto de las imágenes')

    st.pyplot(fig)

def grafico_barras(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de barras"):
        st.write("El gráfico de barras muestra la cantidad de cambios realizados por día de la semana.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego, se calcula el día de la semana para cada fecha de actualización.")
        st.write("Se cuentan la cantidad de cambios realizados para cada día de la semana utilizando value_counts().")
        st.write("Para asegurar que el gráfico incluya todos los días de la semana, se reindexa el resultado utilizando reindex().")
        st.write("Se define una paleta de colores personalizada para las barras del gráfico.")
        st.write("Finalmente, se genera el gráfico de barras utilizando la función bar() de ***Matplotlib***.")
        
    #Copia del dataframe
    datosCopia = datos.copy()
    try:
        datosCopia['fecha actualizacion'] = pd.to_datetime(datosCopia['fecha actualizacion'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    except ValueError:
    # Si hay un error al convertir, asignar un valor predeterminado
        datosCopia['fecha actualizacion'] = None
    # Filtrar los registros que tienen valores no válidos en la columna de fecha_actualizacion
    datosCopia = datosCopia.dropna(subset=['fecha actualizacion'])
    
    # Obtener el día de la semana para cada fecha de actualización
    datosCopia['dia_semana'] = datosCopia['fecha actualizacion'].dt.day_name()
    
    # Contar la cantidad de cambios realizados para cada día de la semana
    cambios_por_dia = datosCopia['dia_semana'].value_counts().sort_index()
    
    # Reindexar para incluir todos los días de la semana
    dias = list(calendar.day_name)  # Lista de los siete días de la semana
    cambios_por_dia = cambios_por_dia.reindex(dias, fill_value=0)
    
    # Definir una paleta de colores personalizada
    paleta_colores = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845', '#07167E', '#00A6ED']
    
    # Generar gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(range(len(cambios_por_dia)), cambios_por_dia.values, color=paleta_colores)
    ax.set_xlabel('Días de la semana')
    ax.set_ylabel('Cantidad de cambios')
    ax.set_title('Cambios')
    # Cambiar los valores en el nombre de los días de la semana
    nombres_dias = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    ax.set_xticklabels(nombres_dias, rotation=0)
    st.pyplot(fig)
     
def grafico_lineas(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de líneas"):
        st.write("El gráfico de líneas muestra la cantidad de actualizaciones por día.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se obtiene el componente del día de la fecha de actualización. Esto se logra utilizando split() y tomando unicamente la parte correspondiente al día.")
        st.write("Se cuenta la cantidad de actualizaciones para cada día y se ordenan los resultados por fecha.")
        st.write("Finalmente, se genera el gráfico de líneas utilizando la función plot() de ***Matplotlib***.")
        
    # Copia del dataframe
    datosCopia = datos.copy()
    
    # Obtener el componente del día de la fecha
    datosCopia['fecha actualizacion'] = datosCopia['fecha actualizacion'].str.split(' ').str[0]
    
    # Contar la cantidad de actualizaciones por día
    contador = datosCopia['fecha actualizacion'].value_counts().sort_index()

    # Crear el gráfico de líneas
    fig, ax = plt.subplots()
    ax.plot(contador.index, contador.values)
    ax.set_ylabel('Cantidad de actualizaciones')
    ax.set_title('Actualizaciones')
    ax.set_xticks([])
   
    st.pyplot(fig)
        
def nube_tags(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Nube de tags"):
        st.write("En esta sección, se genera una nube de palabras a partir de los tags presentes en los datos.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se transforma los tags de la columna del archivo en una lista y se concatenan los tags en un mismo string.")
        st.write("Por ultimo se crea la nube de tags utilizando la biblioteca ***WordCloud***.")

    #Copia del dataframe
    datosCopia = datos.copy()
    # Obtener una lista de todos los tags
    tags = datosCopia['tags'].tolist()
    # Unir los tags en un solo string
    tags_text = ' '.join(tags)
    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tags_text)

    # Mostrar la nube de palabras
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()

    st.pyplot(fig)
    
    # Obtener los 3 tags más utilizados. Counter devuelve una lista de tuplas con el tag y n° apariciones
    top_tags = Counter(tags).most_common(3)

    # Crear una lista de los tags y sus frecuencias
    tag_data = [(tag, count) for tag, count in top_tags]

    # Mostrar los tags más utilizados en formato de tabla
    st.markdown("### Tags más utilizados:")
    st.table(pd.DataFrame(tag_data, columns=["Tags", "Usos"]))

def tabla_tamaño_promedio(datos):
    #Copia del dataframe
    datosCopia = datos.copy()
    # Transformar la columna tamanio a integer dado que tiene el patron xMB deonde x es un real
    datosCopia['tamanio'] = datosCopia['tamanio'].str.replace('MB', '').astype(float)

    #Obtener el tamaño promedio de cada perfil y transformarlo a patron xMB donde x es un real
    perfil_sizes = datosCopia.groupby('ultimo perfil')['tamanio'].mean().apply(lambda x: f'{x:.2f}MB').reset_index()

    # Mostrar los perfiles y sus tamaños promedio en formato de tabla
    st.markdown("### Perfiles con mayor tamaño promedio:")
    st.table(perfil_sizes)

def grafico_pastel_genero(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de torta"):
        st.write("El gráfico de torta muestra los porcentajes de uso de la aplicación por género.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Se utiliza el método value_counts() para contar la cantidad de cada género.")
        st.write("Luego se obtienen los porcentajes.")
        st.write("Una vez calculados los porcentajes, se genera el gráfico de torta utilizando la función pie() de ***Matplotlib***.")
        st.write("Finalmente, se agrega una etiqueta al costado del gráfico que muestra el uso de la aplicación por género junto con su porcentaje correspondiente.")
        
    # Cargar los datos del perfil desde el archivo json
    with open("../datos_app/perfiles.json", 'r') as file:
        datos_genero = json.load(file)
           
    #Copia del dataframe
    datosCopia = datos.copy()
    # Crear una nueva columna 'genero' en el dataframe datosCopia
    generos = []
    #Itero sobre la columna perfil
    for perfil in datosCopia['perfil']:
        #Itero sobre los elementos de la lista
        for i in datos_genero['datos']:
            if perfil == i['Nick']:
                genero = i['Genero']
                generos.append(genero)

    datosCopia['genero'] = generos
    
    # Calcular los porcentajes según el tipo de genero
    genero_tipos = datosCopia['genero'].value_counts()
    total_gen = genero_tipos.sum()
    porcentajes = (genero_tipos / total_gen) * 100

    # Generar el gráfico de torta
    fig, ax = plt.subplots()
    pie = ax.pie(porcentajes, autopct='%1.1f%%', startangle=90)
    ax.set_title('Uso por género')
    
    # Agregar una etiqueta con cada color al costado del gráfico
    ax.legend(pie[0], porcentajes.index, title='Generos', loc='center left', bbox_to_anchor=(1, 0.5))

    st.pyplot(fig)

def grafico_barras_op(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de barras"):
        st.write("Este gráfico de barras refleja las cantidades de cada operación realizada.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se cuentan la cantidad de operaciones realizados para de cada tipo utilizando value_counts().")
        st.write("Se define una paleta de colores personalizada para las barras del gráfico.")
        st.write("Finalmente, se genera el gráfico de barras utilizando la función bar() de ***Matplotlib***.")
        
    #Copia del dataframe
    datosCopia = datos.copy()
    
    # Contar la cantidad de operaciones realizadas para cada tipo.
    cantidad_por_op = datosCopia['operacion'].value_counts().sort_index()
    
    # Definir una paleta de colores personalizada
    paleta_colores = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845', '#07167E', '#00A6ED']
    
    # Generar gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(range(len(cantidad_por_op)), cantidad_por_op.values, color=paleta_colores)
    ax.set_title('Operaciones realizadas')
    # Establecer etiquetas de tipo de operación en el eje x
    ax.set_xticks(range(len(cantidad_por_op)))
    ax.set_xticklabels(cantidad_por_op.index, rotation=45, ha='right')
    st.pyplot(fig)

def grafico_barras_apiladas_nick(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de barras apiladas"):
        st.write("Este gráfico de barras apiladas muestra las cantidades de operaciones de cada tipo por nick.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego, se agrupa el dataframe por nick y tipo de operación, y se cuenta la cantidad de operaciones para cada combinación.")
        st.write("A continuación, se genera el gráfico de barras apiladas utilizando la función barh() de ***Matplotlib***.")

    # Copia del dataframe
    datosCopia = datos.copy()

    # Agrupar el dataframe por nick y tipo de operación, y contar la cantidad de operaciones para cada combinación
    cantidad_por_nick_operacion = datosCopia.groupby(['perfil', 'operacion']).size().unstack()

    # Obtener los nicks y los tipos de operación como listas separadas
    nicks = cantidad_por_nick_operacion.index.tolist()
    tipos_operacion = cantidad_por_nick_operacion.columns.tolist()

    # Generar gráfico de barras apiladas horizontal
    fig, ax = plt.subplots()
    bottom = None
    for tipo_operacion in tipos_operacion:
        valores = cantidad_por_nick_operacion[tipo_operacion].tolist()
        ax.barh(nicks, valores, height=0.6, left=bottom, label=tipo_operacion)
        if bottom is None:
            bottom = valores
        else:
            bottom = [b + v for b, v in zip(bottom, valores)]
    
    ax.set_title('Operaciones')
    ax.invert_yaxis()

    st.pyplot(fig)

def ranking_img(datos):
    #1.
    
    # Copia del dataframe
    datosCopia = datos.copy()

    # Filtrar las operaciones de tipo 'nuevo_meme'
    datos_meme = datosCopia[datosCopia['operacion'] == 'nuevo_meme']

    # Dividir los valores por punto y coma y expandir en nuevas filas
    # Esto crea múltiples filas con el mismo nick y diferentes valores en la columna 'valores'.
    datos_meme = datos_meme.assign(valores=datos_meme['valores'].str.split(';')).explode('valores')
    
    # Obtener la frecuencia de cada imagen
    frecuencia_img = datos_meme['valores'].value_counts()

    # Seleccionar las 5 imágenes con mayor frecuencia
    top_img = frecuencia_img.head(5)

    # Crear una lista de los nombres de las imágenes y sus frecuencias
    img_data = [(imagen, frecuencia) for imagen, frecuencia in top_img.items()]

    # Mostrar el ranking de imágenes más utilizadas en formato de tabla
    st.markdown("### Ranking de imágenes más utilizadas para memes:")
    st.table(pd.DataFrame(img_data, columns=["Imagen", "Usos"]))
    
    #2.
    
    # Filtrar las operaciones de tipo 'nuevo_collage'
    datos_collage = datosCopia[datosCopia['operacion'] == 'nuevo_collage']

    # Dividir los valores por punto y coma y expandir en nuevas filas
    # Esto crea múltiples filas con el mismo nick y diferentes valores en la columna 'valores'.
    datos_collage = datos_collage.assign(valores=datos_collage['valores'].str.split(';')).explode('valores')
    
    # Obtener la frecuencia de cada imagen
    frecuencia_img = datos_collage['valores'].value_counts()

    # Seleccionar las 5 imágenes con mayor frecuencia
    top_img = frecuencia_img.head(5)

    # Crear una lista de los nombres de las imágenes y sus frecuencias
    img_data = [(imagen, frecuencia) for imagen, frecuencia in top_img.items()]

    # Mostrar el ranking de imágenes más utilizadas en formato de tabla
    st.markdown("### Ranking de imágenes más utilizadas para collages:")
    st.table(pd.DataFrame(img_data, columns=["Imagen", "Usos"]))

def nube_tags_collage(datos):
# Crear el contenedor expandible en Streamlit
    with st.expander("Nube de tags"):
        st.write("En esta sección, se genera una nube de palabras a partir de los textos agregados en collages.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se transforma los textos agregados de la columna concatenando los tags en un mismo string.")
        st.write("Por ultimo se crea la nube de tags utilizando la biblioteca ***WordCloud***.")

    #Copia del dataframe
    datosCopia = datos.copy()
    # Filtrar las operaciones de tipo 'nuevo_collage'
    datos_collage = datosCopia[datosCopia['operacion'] == 'nuevo_collage']
    # Dividir los valores por punto y coma y expandir en nuevas filas
    # Esto crea múltiples filas con el mismo nick y diferentes valores en la columna 'valores'.
    datos_collage = datos_collage.assign(textos=datos_collage['textos'].str.split(';')).explode('textos')
    
   # Convertir los textos a cadenas de texto antes de unirlos
    textos = [str(texto) for texto in datosCopia['textos'].tolist()]

    # Unir los tags en un solo string
    str_text = ' '.join(textos)
    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(str_text)

    # Mostrar la nube de palabras
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()

    st.pyplot(fig)

def nube_tags_meme(datos):
# Crear el contenedor expandible en Streamlit
    with st.expander("Nube de tags"):
        st.write("En esta sección, se genera una nube de palabras a partir de los textos agregados en memes.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se transforma los textos agregados de la columna concatenando los tags en un mismo string.")
        st.write("Por ultimo se crea la nube de tags utilizando la biblioteca ***WordCloud***.")

    #Copia del dataframe
    datosCopia = datos.copy()
    # Filtrar las operaciones de tipo 'nuevo_meme'
    datos_meme = datosCopia[datosCopia['operacion'] == 'nuevo_meme']
    # Dividir los valores por punto y coma y expandir en nuevas filas
    # Esto crea múltiples filas con el mismo nick y diferentes valores en la columna 'valores'.
    datos_meme = datos_meme.assign(textos=datos_meme['textos'].str.split(';')).explode('textos')
    
   # Convertir los textos a cadenas de texto antes de unirlos
    textos = [str(texto) for texto in datosCopia['textos'].tolist()]

    # Unir los tags en un solo string
    str_text = ' '.join(textos)
    # Crear la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(str_text)

    # Mostrar la nube de palabras
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()

    st.pyplot(fig)                   

def grafico_pastel_genero_op(datos):
    # Crear el contenedor expandible en Streamlit
    with st.expander("Gráfico de torta"):
        st.write("El gráfico de torta muestra los porcentajes según género de las personas que realizaron las operaciones 'Nueva imagen clasificada' y 'Modificación de imagen previamente clasificada'.")
        st.write("Primero, se realiza una copia del dataframe original para preservar los datos originales.")
        st.write("Luego se carga el archivo de perfiles para obtener los géneros de las personas.")
        st.write("A continuación, se filtran las operaciones de interés y se obtienen los porcentajes por género.")
        st.write("Finalmente, se genera el gráfico de torta utilizando la función pie() de Matplotlib.")

    # Copia del dataframe
    datosCopia = datos.copy()

    # Cargar los datos del perfil desde el archivo json
    with open("../datos_app/perfiles.json", 'r') as file:
        datos_genero = json.load(file)

    # Filtrar las operaciones de interés
    operaciones_interes = ['Nueva imagen clasificada', 'Modificación de imagen previamente clasificada']
    datos_interes = datosCopia[datosCopia['operacion'].isin(operaciones_interes)]

    # Obtener los géneros de las personas que realizaron las operaciones
    generos = []
    for perfil in datos_interes['perfil']:
        for i in datos_genero['datos']:
            if perfil == i['Nick']:
                genero = i['Genero']
                generos.append(genero)

    # Calcular los porcentajes por género
    genero_tipos = pd.Series(generos).value_counts()
    total_gen = genero_tipos.sum()
    porcentajes = (genero_tipos / total_gen) * 100

    # Generar el gráfico de torta
    fig, ax = plt.subplots()
    pie = ax.pie(porcentajes, autopct='%1.1f%%', startangle=90)
    ax.set_title('Operaciones por género')

    # Agregar una etiqueta con cada color al costado del gráfico
    ax.legend(pie[0], porcentajes.index, title='Género', loc='center left', bbox_to_anchor=(1, 0.5))

    st.pyplot(fig)
    
st.header("Analisis de datos - Archivo imágenes clasificadas.")
grafico_pastel_img(datos_img)
grafico_dispersion(datos_img)
grafico_barras(datos_img)    
grafico_lineas(datos_img)
nube_tags(datos_img)
tabla_tamaño_promedio(datos_img)
st.header("Analisis de datos - Archivo log del sistema.")
grafico_barras(datos_logs)
grafico_pastel_genero(datos_logs)
grafico_barras_op(datos_logs)
grafico_barras_apiladas_nick(datos_logs)
ranking_img(datos_logs)
nube_tags_collage(datos_logs)
nube_tags_meme(datos_logs)
grafico_pastel_genero_op(datos_logs)