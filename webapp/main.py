import streamlit as st

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

# Show the binary array
st.markdown("### ผลลัพธ์เป็นอาเรย์:")
st.write(selection_array)