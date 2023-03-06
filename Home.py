!pip install streamlit --upgrade
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.header( 'Informações Básicas' )
#image_path = \Users\User\zomato_1\zomato_logo.jpg'
image = Image.open('zomato_logo.jpg')
st.sidebar.image( image, width=120 )


#df_raw = pd.read_csv('zomato_1.csv', encoding='ISO-8859-1')

#from google.colab import drive

#drive.mount('/content/drive')



df_raw = pd.read_csv('dataset/zomato_1.csv', encoding="ISO-8859-1")

df = df_raw.copy()

# ===================================================================

#Separando os tipos de culinária em restaurantes que possuem mais de uma:


df['Cuisines'] = df.loc[:, 'Cuisines'].apply(lambda x: str(x).split(",")[0])

# Criando uma coluna com o nome dos países baseado em código.

df['Country name'] = df['Country Code'].replace({
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
})

# Criando uma coluna Categorizando Comidas com base em seus price range


df['Price Type'] = df['Price range'].replace({
    1: "cheap",
    2: "normal",
    3: "expensive",
    4: "gourmet",
})

# Criando uma coluna com o nome das cores baseado em código de cor.


df['Colors'] = df['Rating color'].replace({
    '3F7E00': "darkgreen",
    '5BA829':"green",
    '9ACD32': "lightgreen",
    'CDD614': "orange",
    'FFBA00': "red",
    'CBCBC8': "darkred",
    'FF7800': "darkred",

})

def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize (x)
  snakecase = lambda x: inflection.underscore (x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_old = list(map(snakecase, cols_old))
  df.columns = cols_new

  return df

# Barra Lateral

#----------------------


#-------------------------------------------------------------------------------------


st.markdown('A Zomato é um serviço de busca de restaurantes para quem quer sair para jantar, buscar comida ou pedir em casa na Índia, Brasil, Portugal, Turquia, Indonésia, Nova Zelândia, Itália, Filipinas, África do Sul, Sri Lanka, Catar, Emirados Árabes Unidos, Reino Unido, Estados Unidos, Austrália e Canadá.')
st.markdown('___________________________________________________________________')          
st.markdown('Essa Dashboard tem o intuito de fazer análises sob o ponto de vista de países, cidades e tipos de culinárias.')
st.markdown('Essas análises podem ser acessadas no menu do canto superior esquerdo junto de um filtro de países feito para fins comparativos.')
st.markdown('___________________________________________________________________')           
st.markdown('Essas informações foram disponibilizadas pelo site kaggle.com')
st.markdown('___________________________________________________________________')           
st.markdown('Caso queira visualizar na versão de tela escura, basta alterar no canto superior direito:')
st.markdown('Settings ➡️ Theme ➡️ Dark.')
