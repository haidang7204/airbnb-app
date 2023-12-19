import streamlit as st
import pandas as pd
import folium
import numpy as np


np.random.seed(42)
boroughs = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
neighborhoods = {
    'Manhattan': ['Midtown', 'Harlem', 'Upper East Side', 'Upper West Side'],
    'Bronx': ['Riverdale', 'Fordham', 'Bronx Park'],
    'Brooklyn': ['Williamsburg', 'Park Slope', 'Brooklyn Heights'],
    'Queens': ['Astoria', 'Long Island City', 'Flushing'],
    'Staten Island': ['St. George', 'Tompkinsville', 'Stapleton']
}
prices = np.random.randint(50, 500, size=100) 
host_names = ['John', 'Tim', 'Sarah']  
room_types = ['Private room', 'Entire home/apt', 'Shared room']  


length = 100

data = pd.DataFrame({
    'house_name': np.random.choice(['Furnished room in Astoria apartment', 'Single room in Manhattan', 'Cozy apartment in Brooklyn', 'Spacious house in Queens', 'Charming loft in Staten Island'], size=length),  
    'listing_name': np.random.choice(host_names, size=length),
    'borough': np.random.choice(boroughs, size=length),
    'neighborhood': np.random.choice(np.concatenate([neighborhoods[borough] for borough in boroughs]), size=length),
    'room_type': np.random.choice(room_types, size=length),
    'price': prices,
    'latitude': np.random.uniform(40.5, 41, size=length),  
    'longitude': np.random.uniform(-74.3, -73.6, size=length)  
})

data.to_csv('airbnb_nyc_2019.csv', index=False)
data = pd.read_csv('airbnb_nyc_2019.csv')

import altair as alt
from PIL import Image
image = Image.open('houselogo.png')
st.image(image, use_column_width=False,width=200)


st.title('Airbnb NYC 2019 Housing Data')
st.write('Welcome to our website! Find your perfect place in NYC')


st.write('### Sample Data')
st.write(data.head())


st.write('### Instructions')
st.write('1. Use the dropdowns to select a borough and neighborhood.')
st.write('2. Set your desired price range.')
st.write('3. Explore available housing rentals in the selected area.')


boroughs = data['borough'].unique()
selected_borough = st.selectbox('Select a Borough', boroughs)

neighborhoods = data[data['borough'] == selected_borough]['neighborhood'].unique()
selected_neighborhoods = st.multiselect('Select Neighborhood(s)', neighborhoods)

price_range = st.slider('Price Range', min_value=0, max_value=1000, value=(100, 500))

filtered_data = data[
    (data['borough'] == selected_borough) &
    (data['neighborhood'].isin(selected_neighborhoods)) &
    (data['price'].between(price_range[0], price_range[1]))
]
st.write(f"Total {len(filtered_data)} housing rentals found.")

# Map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

for index, row in filtered_data.iterrows():
    tooltip = f"${row['price']}"
    
    
    house_name = row['house_name']

    details = f"""
    <strong>Name:</strong> {house_name}<br>
    <strong>Neighborhood:</strong> {row['neighborhood']}<br>
    <strong>Host name:</strong> {row['listing_name']}<br>
    <strong>Room type:</strong> {row['room_type']}<br>
    <strong>Price:</strong> ${row['price']}
    """

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        tooltip=tooltip,
        popup=folium.Popup(details, max_width=300, min_width=200)
    ).add_to(m)

st.write(m._repr_html_(), unsafe_allow_html=True)
