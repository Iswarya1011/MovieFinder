import streamlit as st 
import pandas as pd
import plotly.express as px


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
  if search_submit:
    st.success("You searched for {}".format(search_term))


  

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
