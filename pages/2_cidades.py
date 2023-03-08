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


#df_raw = pd.read_csv('zomato_1.csv', encoding='ISO-8859-1')

#from google.colab import drive

#drive.mount('/content/drive')

df_raw = pd.read_csv('zomato_1.csv', encoding="utf-8")

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
#Barra Lateral
#--------------------------
st.header( 'Informações de cidades' )
image_path = 'logo_zomato1.png'
image = Image.open('zomato_logo.jpg')
st.sidebar.image( image, width=120 )


st.sidebar.title( '' )
st.sidebar.markdown( '## Filtros ' )

st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Selecione países por exclusão')

country_options = st.sidebar.multiselect(
    'Quais países?',
    ['India','Australia','Brazil','Canada','Indonesia',"New Zeland","Philippines","Qatar","Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England","United States of America"],
    default= ['India','Australia','Brazil','Canada','Indonesia',"New Zeland","Philippines","Qatar","Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England","United States of America"] )

st.sidebar.markdown("""___""")

#Filtro de país
linhas_selecionadas = df['Country name'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

#---------------------------------------------------------------

col1, col2, col3, col4 = st.columns( 4 )
with col1:
   # st.subheader( 'Quantidade total de culinárias')

    df_aux1 = df.loc[:,'City'].nunique()
                                
    col1.metric('Cidades no total',df_aux1)

with col2:
    
    df_cn = (df.loc[:,['City','Aggregate rating']].groupby('City').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(4.00, 10.00)].count()
    
    
    col2.metric('Avaliações acima de 4.0',df_aux)
    
    
with col3:
    f_cn = (df.loc[:,['City','Aggregate rating']].groupby('City').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(3.00, 3.99)].count()
    
    
    col3.metric('Entre 3.0 e 4.0',df_aux)
    
with col4:
    
    f_cn = (df.loc[:,['City','Aggregate rating']].groupby('City').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(0.00, 2.99)].count()
    
    
    col4.metric('Abaixo de 3.0',df_aux)
    
#-----------------------------------------------------------------------------------

with st.container():
    st.markdown("""___""")
    st.title( 'Ranking de cidades' )

col1, col2 = st.columns( 2 )
with col1:
    st.subheader( 'Cidade com mais restaurantes cadastrados')
 
    mais_registro = (df.loc[:,['City','Restaurant ID',]].groupby('City').count().sort_values(['Restaurant ID'], ascending=False))
                               
    st.dataframe(mais_registro)

with col2:
    st.subheader( '20 Cidades com maior avaliação média')
 
    maior_avaliacao = round(df.loc[:,['City','Aggregate rating']].groupby('City').mean().sort_values(['Aggregate rating'], ascending=False),2).head(20)
    
    maior_avaliacao = maior_avaliacao.reset_index()
    
    fig = px.bar(maior_avaliacao, x= 'Aggregate rating', y= 'City', orientation='h')
                               
   
    st.plotly_chart( fig, use_container_width=True )
                                  
   
# --------------------------------------------------------------

with st.container():
        st.markdown("""___""")
        st.subheader( 'Média e desvio padrão de avaliação de cada cidade por país' )

#df_rating_4_mais = df[df['Aggregate rating'].between(4.0, 10.0)]

cols = ['Country name','City','Aggregate rating']
df_aux = df.loc[:, cols].groupby( ['Country name','City']).agg({'Aggregate rating':['mean','std']})

df_aux.columns = ['média','desviop']

df_aux.sort_values(['média'],ascending=True)

df_4 = round(df_aux.reset_index(),2)

st.dataframe(df_4)

#------------------------------------------


 #st.subheader( 'Cidade com mais restaurantes cadastrados')
 
#    mais_registro = (df.loc[:,['City','Restaurant #ID',]].groupby('City').count().sort_values(['Restaurant ID'], ascending=False))
                               
   
 #   st.dataframe(mais_registro)
    
with st.container():
   
    st.markdown('## Cidades que possuem os restaurantes que mais aceitam reserva')
   
    df_tbooking = df[df['Has Table booking'].isin([1])]
       
    reserva = df_tbooking.loc[:,['City','Has Table booking']].groupby('City').count().sort_values(['Has Table booking'], ascending=False).head(20)


    reserva = reserva.reset_index()

    fig = px.bar(reserva, x= 'City', y= 'Has Table booking')

    #fig.show()
   
    st.plotly_chart( fig, use_container_width=True )
    
#---------------------------------------------------------------------------------

with st.container():
   
    st.markdown('## Cidades que possuem os restaurantes que mais realizam pedidos de forma online e seus respectivos países')

    
    df_c = df[df['Has Online delivery'].isin([1])]


    df_aux2 = (df_c.loc[:,['City', 'Country name', 'Has Online delivery']]
          .groupby( ['Country name','City'])
          .agg({'Has Online delivery':['count']}))

    df_aux2.columns = ['count']

    df_aux2 = df_aux2.reset_index().sort_values(['count'], ascending=False)
    
    st.dataframe(df_aux2)

