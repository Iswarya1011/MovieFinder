import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

def closeFilms(film_name, df, r=0.5, cols=range(10)):

    dataf = df.copy()
    
    i = dataf.loc[dataf['name'] == film_name]

    
    dataf["dist"] = 0
    for c in cols:
        dataf["tempDist"] = dataf[c].apply(lambda x : (x-i[c])**2)
        dataf["dist"] += dataf["tempDist"]

    dataf["dist"] = dataf["dist"].apply(lambda x : np.sqrt(x))
    
    dataf.drop(columns=["tempDist"], inplace=True)
    
    dataf = dataf[dataf["dist"]<r]
    dataf = dataf.sortvalues("dist")

    return dataf


st.title('This is my first app!')
st.write('This is a table')

df = pd.read_csv("all_films.csv",sep=";")

genres = []
for i in range(df.shape[0]):
    sti = df['genre'].loc[i]
    sti = sti.replace(" ", "")
    sti = sti.replace('[',"")
    sti = sti.replace(']',"")
    sti = sti.replace("'", "")
    sti = sti.split(",")
    genres.append(sti)

s = set()
for i in range(len(genres)):
    for j in range(len(genres[i])):
        s.add(genres[i][j])
s = list(s)


with st.sidebar:
  st.header("Search your Films !")
  st.multiselect('Genres', s)

  with st.form(key = 'searchform'):
    nav1,nav2 = st.columns([2,1])

    with nav1:
        search_term = st.text_input('Film Name')
    with nav2:
        st.text("")
        st.text("")
        search_submit = st.form_submit_button()
  

st.write(df)

data = pd.read_csv('df_famd.csv', sep =';')
st.write(data)

st.write('FAMD')

fig = px.scatter_3d(data, x='4', y='1', z='2', color='3')

fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="LightSteelBlue"
    )

st.plotly_chart(fig)

if search_submit:
    st.success("You searched for {}".format(search_term))
    df_result = df.loc[df['name'].str.contains(search_term, case=False)]
    st.write(df_result)
