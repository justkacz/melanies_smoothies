# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose your fruits you want in your custom Smoothie! 
  """
)

name_on_order = st.text_input("Name your smoothie.")
st.write(f"Name of your smoothie is: {name_on_order}")

cnx = st.connection("snowflake")
session = cnx.session()

my_df = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
pd_df=my_df.to_pandas()

ingreditnts_list = st.multiselect('Choose up to 5 ingredients:', 
                                  my_df, 
                                  max_selections=5)

if ingreditnts_list:
    ingredients_string = ''

    for fruit_choosen in ingreditnts_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")

