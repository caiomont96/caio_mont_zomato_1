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

#st.write(df.style.format({"Predictions": "{:.2f}"}))


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
st.header( 'Informações de países' )
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

#-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------
#Qual o país que mais aceita reserva?

#with st.container():
    
  #  st.markdown('Países que mais aceitam reserva')
       
  #  df_tbooking = df[df['Has Table booking'].isin([1])]

   # reserva = df_tbooking.loc[:,['Country name','Has Table booking']].groupby('Country name').count().sort_values(['Has Table booking'], ascending=False)
    


 #   reserva = reserva.reset_index()
    
 #   reserva.head()
    
    #st.plotly_chart( fig, use_container_width=True )
    
    #-------------------------------------------------------------------

        #------------------------------------------------------------------
    

# ------------------------------------------------------------------------

with st.container():
       
    col1, col2, col3, col4 = st.columns(4)
    with col1:      
        rstrts = df.loc[:, 'Restaurant ID'].nunique()
        col1.metric('Restaurantes', rstrts)
           
    with col2:
        paises_registrados = df.loc[:,	'Country Code'].nunique()
        col2.metric('Países', paises_registrados)
           
    with col3:
        cidade = df.loc[:,	'City'].nunique()
        col3.metric('Cidades', cidade)

    with col4:
        total_avaliacoes = df['Votes'].sum()
        col4.metric('Total Avaliações', total_avaliacoes) 

# Mapa!
    
with st.container():
    
        st.markdown("""___""")
        st.subheader('Localização geográfica dos restaurantes')
        st.markdown('*zoom in/out com scroll do mouse')
        df_ll = df.loc[:,['Restaurant ID','Latitude','Longitude']]

        df_ll = df_ll.rename(columns={"Restaurant ID":"ID",'Latitude':'Y','Longitude':'X'})

        df_ll.columns = df_ll.columns.str.strip()

        #df_ll.head()
        
        subset_of_df_ll = df_ll.sample(n=500)
        
        
        some_map2 = folium.Map(location= [subset_of_df_ll['Y'].mean(),
                                subset_of_df_ll['X'].mean()],
                                zoom_start=10)
        
        mc= MarkerCluster()
        
        for row in subset_of_df_ll.itertuples():

            mc.add_child(folium.Marker(location=[row.Y,row.X], popup=row.ID))
            
        some_map2.add_child(mc)
        
        folium_static(some_map2, width=700, height=500)
      

# Países com mais restaurantes cadastrados

with st.container():
    st.markdown("""___""")

col1, col2 = st.columns( 2 )
with col1:
    st.subheader( 'Mais avaliados')
 
    mais_avaliacao = (df.loc[:,['Country name','Votes']].groupby('Country name').sum().sort_values(['Votes'], ascending=False))
                                
   
    st.dataframe(mais_avaliacao)
   
with col2:
    st.subheader( 'Com maior avaliação média')
    
    #st.dataframe(df.style.format(subset=['Aggregate rating'], formatter='{:.2f}'))

 
    maior_avaliacao = round(df.loc[:,['Country name','Aggregate rating']].groupby('Country name').mean().sort_values(['Aggregate rating'], ascending=False),2)
                                
   
    st.dataframe(maior_avaliacao)


with st.container():
    st.markdown("""___""")
    st.title( 'Características' )

with st.container():
    
    st.markdown('## Países com mais restaurantes cadastrados')
    


    df_aux = df.loc[:, ['City','Country name']].groupby('Country name').count().sort_values(['City'], ascending=False)

    df_aux = df_aux.reset_index()

    fig = px.bar(df_aux, x= 'Country name', y= 'City')

    #fig.show()

    st.plotly_chart( fig, use_container_width=True )


#------------------------------------------------------------------------------
#Qual o país que possui na média a maior nota média registrada?

with st.container():
    
    st.markdown('## Países com restaurantes que mais aceitam reserva')
    
    df_tbooking = df[df['Has Table booking'].isin([1])]
       
    reserva = df_tbooking.loc[:,['Country name','Has Table booking']].groupby('Country name').count().sort_values(['Has Table booking'], ascending=False)


    reserva = reserva.reset_index()

    fig = px.bar(reserva, x= 'Country name', y= 'Has Table booking')

    #fig.show()
    
    st.plotly_chart( fig, use_container_width=True )

    #----------------------------------
    
   # st.subheader( 'Países que mais aceitam reserva' )
  #  df_tbooking = df[df['Has Table booking'].isin([1])]

  #  reserva = df_tbooking.loc[:,['Country name','Has Table booking']].groupby('Country name').count().sort_values(['Has Table booking'], ascending=False)
  
  #  st.dataframe(reserva)
