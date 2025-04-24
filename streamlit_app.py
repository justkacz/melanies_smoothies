# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose your fruits you want in your custom Smoothie! 
  """
)

name_on_order = st.text_input("Name your smoothie.")
st.write(f"Name of your smoothie is: {name_on_order}")

session=get_active_session()
my_df = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
ingreditnts_list = st.multiselect('Choose up to 5 ingredients:', 
                                  my_df, 
                                  max_selections=5)

if ingreditnts_list:
    ingredients_string = ''

    for fruit_choosen in ingreditnts_list:
        ingredients_string += fruit_choosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")
