import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd


comment = st.text_area("กรุณาใส่ความคิดเห็นของคุณ:", "")

# List of categories (24 categories for 6x4 table)
categories = ['PM2.5', 'การเดินทาง', 'กีดขวาง', 'คนจรจัด', 'คลอง', 'ความปลอดภัย', 
              'ความสะอาด', 'จราจร', 'ต้นไม้', 'ถนน', 'ทางเท้า', 'ท่อระบายน้ำ', 
              'น้ำท่วม', 'ป้าย', 'ป้ายจราจร', 'ร้องเรียน', 'สอบถาม', 'สะพาน', 
              'สัตว์จรจัด', 'สายไฟ', 'ห้องน้ำ', 'เสนอแนะ', 'เสียงรบกวน', 'แสงสว่าง']

st.title("เลือกหมวดหมู่ที่เกี่ยวข้อง")

# Create 4 columns to represent 4 columns of checkboxes
cols = st.columns(4)

# Initialize the binary array with all 0s
selection_array = [0] * len(categories)

# Render checkboxes in a 6x4 table
for i in range(6):  # 6 rows
    for j in range(4):  # 4 columns
        index = i * 4 + j  # Calculate index for each checkbox in the list
        if index < len(categories):  # Ensure we don't go beyond the list
            # Place the checkbox in the correct column and update the selection array
            if cols[j].checkbox(categories[index]):
                selection_array[index] = 1


m = folium.Map(location=[13.7563, 100.5018], zoom_start=12)

# Create a marker that updates with latitude and longitude on click
click_marker = folium.LatLngPopup()

# Add the click marker to the map
m.add_child(click_marker)

# Display the map
location = st_folium(m, width=700)

# Show the selected latitude and longitude if available
if location and location['last_clicked']:
    lat = location['last_clicked']['lat']
    lon = location['last_clicked']['lng']
    st.write(f"### ตำแหน่งที่เลือก: Latitude: {lat}, Longitude: {lon}")

# Show the binary array
st.markdown("### ผลลัพธ์เป็นอาเรย์:")
st.write(selection_array)