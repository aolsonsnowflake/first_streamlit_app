import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title("My Parents' New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🐿️🦯 Squirrel on a Stick')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# make function for getting fruityvice data
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("View Our Fruit List - Add Your Favorites!")
if streamlit.button('Get Fruit List', key = "sl_button_listfruit"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * from fruit_load_list")
  my_data_row = my_cur.fetchall()
  streamlit.text("The fruit load list contains:")
  streamlit.dataframe(my_data_row)
  my_cnx.close()

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', key = "sl_fruit_choice")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # display pandas dataframe
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()




# add fruit to fruit_load_list
add_to_fruit_load_list = streamlit.text_input('What fruit would you like add to the list?','Type fruit name here', key = "sl_add_to_fruit_load_list")

if streamlit.button('Add', key = "sl_button_addfruit"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur.execute("INSERT INTO FRUIT_LOAD_LIST (FRUIT_NAME) VALUES (%s)", add_to_fruit_load_list)
  streamlit.write("Added this fruit to list:", add_to_fruit_load_list)
  my_cnx.close()

  
