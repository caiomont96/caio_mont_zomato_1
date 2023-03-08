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
#df_raw = pd.read_csv('dataset/zomato_1.csv', encoding="ISO-8859-1")
df_raw = pd.read_csv('dataset/zomato_1.csv', encoding='utf-8')


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
st.header( 'Informações sobre culinárias' )
image_path = 'logo_zomato1.png'
image = Image.open('zomato_logo.jpg')
st.sidebar.image( image, width=120 )


st.sidebar.title( '' )
st.sidebar.markdown( '## Filtro ' )

st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Seleção de países por exclusão')

country_options = st.sidebar.multiselect(
    'Quais países?',
    ['India','Australia','Brazil','Canada','Indonesia',"New Zeland","Philippines","Qatar","Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England","United States of America"],
    default= ['India','Australia','Brazil','Canada','Indonesia',"New Zeland","Philippines","Qatar","Singapure","South Africa","Sri Lanka","Turkey","United Arab Emirates","England","United States of America"] )

st.sidebar.markdown("""___""")

#Filtro de país
linhas_selecionadas = df['Country name'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

#-------------------------------------------------------------------

# contagem de quantas culinárias totais
# gráfico com cuinárias mais presentes

# ----------------------------------------------------------
# top italiano
# top árabe
# top japones

#--------------------------------------

# gráfico com culinárias que mais fazem entregas
#---------------------------------------------------------------
with st.container():
    st.markdown("""___""")
    st.subheader( 'Avaliações médias de culinárias' )

col1, col2, col3, col4 = st.columns( 4 )
with col1:
   # st.subheader( 'Quantidade total de culinárias')

    df_aux1 = df.loc[:,'Cuisines'].nunique()
                                
    col1.metric('Variedade de culinárias',df_aux1)

with col2:
    
    df_cn = (df.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(4.00, 10.00)].count()
    
    
    col2.metric('Avaliações acima de 4.0',df_aux)
    
    
with col3:
    df_cn = (df.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(3.00, 3.99)].count()
    
    
    col3.metric('Entre 3.0 e 4.0',df_aux)
    
with col4:
    
    df_cn = (df.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=False))
    
    df_aux = df_cn[df_cn['Aggregate rating'].between(0.00, 2.99)].count()
    
    
    col4.metric('Abaixo de 3.0',df_aux)

    


#------------------------------------------------------------------

with st.container():
   
    st.markdown('## 20 Culinárias mais comuns')
   


    df_aux = df.loc[:, ['Cuisines','Country name']].groupby('Cuisines').count().sort_values(['Country name'], ascending=False).head(20)

    df_aux = df_aux.reset_index()

    fig = px.bar(df_aux, x= 'Cuisines', y= 'Country name')

    #fig.show()

    st.plotly_chart( fig, use_container_width=True )



#------------------------------------------------------------------

with st.container():


    st.markdown("""___""")           

    st.subheader( 'Culinárias dos restaurantes que mais fazem entregas online')

    df_online1 = df[df['Has Online delivery'].isin([1])]

    df_online1_delivery1 = df_online1[df_online1['Is delivering now'].isin([1])]

    df_aux1 = (df_online1_delivery1.loc[: , ['Restaurant Name', 'Cuisines']].groupby('Cuisines').count().sort_values('Restaurant Name', ascending=False)).head(10)
    
    df_aux1 = df_aux1.reset_index()
    
    fig = px.bar(df_aux1, x= 'Cuisines' , y= 'Restaurant Name')
    
    st.plotly_chart( fig, use_container_width=True )

#-------------------------------------------------------------------

with st.container():


    st.markdown("""___""")           

    st.subheader( 'Culinárias dos restaurantes que mais fazem entregas online')

    df_online1 = df[df['Has Online delivery'].isin([1])]

    df_online1_delivery1 = df_online1[df_online1['Is delivering now'].isin([1])]

    df_aux1 = (df_online1_delivery1.loc[: , ['Restaurant Name', 'Cuisines']].groupby('Cuisines').count().sort_values('Restaurant Name', ascending=False)).head(10)
    
    df_aux1 = df_aux1.reset_index()
    
    fig = px.bar(df_aux1, x= 'Cuisines' , y= 'Restaurant Name')
    
    st.plotly_chart( fig, use_container_width=True )
    
#----------------------------------------------

    #--------------------------------------------------
    st.subheader( 'Fast Foods mais bem avaliados e seus respectivos países')

    
    df_c = df[df['Cuisines'] == ('Fast Food')]


    df_aux2 = (df_c.loc[:,['Restaurant Name', 'Country name', 'Aggregate rating']]
          .groupby( ['Country name','Restaurant Name'])
          .agg({'Aggregate rating':['mean']}))

    df_aux2.columns = ['mean']

    df_aux2 = df_aux2.reset_index().sort_values(['mean'], ascending=False)
    
    st.dataframe(df_aux2)
    
    
    #------------------------------
    
        
    st.subheader( 'Restaurantes de culinária brasileira mais bem avaliados e seus respectivos países')

    
    df_c = df[df['Cuisines'] == ('Brazilian')]


    df_aux2 = (df_c.loc[:,['Restaurant Name', 'Country name', 'Aggregate rating']]
          .groupby( ['Country name','Restaurant Name'])
          .agg({'Aggregate rating':['mean']}))

    df_aux2.columns = ['mean']

    df_aux2 = df_aux2.reset_index().sort_values(['mean'], ascending=False)
    
    st.dataframe(df_aux2)
    
    #-----------------------------------------------------------------
    
    

    # --------------------------------------------------
    
    st.subheader( 'Restaurantes de culinária italiana mais bem avaliados e seus respectivos países')

    
    df_c = df[df['Cuisines'] == ('Italian')]


    df_aux2 = (df_c.loc[:,['Restaurant Name', 'Country name', 'Aggregate rating']]
          .groupby( ['Country name','Restaurant Name'])
          .agg({'Aggregate rating':['mean']}))
    df_aux2.columns = ['mean']

    df_aux2 = df_aux2.reset_index().sort_values(['mean'], ascending=False)
    
    st.dataframe(df_aux2)
        
    #---------------------------------------------------------------
    
    st.subheader( 'Restaurantes de culinária japonesa mais bem avaliados e seus respectivos países')


    
    df_c = df[df['Cuisines'] == ('Japanese')]


    df_aux2 = (df_c.loc[:,['Restaurant Name', 'Country name', 'Aggregate rating']]
          .groupby( ['Country name','Restaurant Name'])
          .agg({'Aggregate rating':['mean']}))

    df_aux2.columns = ['mean']

    df_aux2 = df_aux2.reset_index().sort_values(['mean'], ascending=False)
    
    st.dataframe(df_aux2)
    
    #-----------------------------------------------------------------------
    

    
