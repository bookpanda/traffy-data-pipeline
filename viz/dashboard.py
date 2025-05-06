import streamlit as st
import pandas as pd
from sklearn.cluster import DBSCAN
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/bangkok_traffy.csv')
    final_df = pd.read_csv('data/final_df.csv')
    return df, final_df

def preprocess_data(df):
    df[['longitude', 'latitude']] = df['coords'].str.split(',', expand=True).astype(float)
    df['type_cleaned'] = df['type'].str.strip('{}').str.replace(' ', '')
    return df

def extract_unique_types(df):
    type_lists = df['type'].dropna().apply(lambda x: x.strip('{}').replace(' ', '').split(','))
    unique_types = sorted(set(t for sublist in type_lists for t in sublist if t))
    return unique_types


raw_df,final_df = load_data()
df = preprocess_data(raw_df)

all_types = extract_unique_types(df)
# all_types = ["All"] + extract_unique_types(df)
# all_districts = ["All"] + sorted(df['district'].dropna().unique())

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(df.head())

st.sidebar.header('Select Type')
selected_type = st.sidebar.selectbox(
    'Select Issue Type', 
    options = all_types,
    index = 0
)

df_selected = df[df['type_cleaned'].str.contains(selected_type, na=False)].copy()
# if selected_type != "All":
#     df_selected = df[df['type_cleaned'].str.contains(selected_type, na=False)].copy()
# else:
#     df_selected = df.copy()
all_districts = ["All"] + sorted(df_selected['district'].dropna().unique())

st.sidebar.header("Type's Map Settings")
map_style = st.sidebar.selectbox(
    'Select Base Map Style',
    options = ['Dark', 'Light', 'Road', 'Satellite'],
    index = 0
)
MAP_STYLES = {
    'Dark': 'mapbox://styles/mapbox/dark-v10',
    'Light': 'mapbox://styles/mapbox/light-v10',
    'Road': 'mapbox://styles/mapbox/streets-v11',
    'Satellite': 'mapbox://styles/mapbox/satellite-v9'
}

selected_district = st.sidebar.selectbox(
    'Select District',
    options = all_districts,
    index = 0  # Default is "All"
)
if selected_district != "All":
    df_selected = df_selected[df_selected['district'] == selected_district]

min_samples_value = st.sidebar.slider(
    'DBSCAN min_samples', 
    min_value = 1, 
    max_value = 20, 
    value = 5
)

eps_value = st.sidebar.slider(
    'DBSCAN eps', 
    min_value = 0.001, 
    max_value = 0.05, 
    value = 0.01, 
    step = 0.001
)

all_orgs = sorted(final_df['organization'].dropna().unique())
st.sidebar.header("Organization Filter")
selected_org = st.sidebar.selectbox(
    "Select Organization", 
    options=all_orgs, 
    index=0
)

# df_selected['timestamp'] = pd.to_datetime(df_selected['timestamp'])
df_selected['timestamp'] = pd.to_datetime(df_selected['timestamp'], format='mixed')
df_selected['year'] = df_selected['timestamp'].dt.year
yearly_count = df_selected.groupby('year').size().reset_index(name='ticket_count')
yearly_count['year'] = yearly_count['year'].astype(str) 

st.header("Raw Data")

st.subheader(f"Number of Tickets for type '{selected_type}' by Year")
fig = px.bar(
    yearly_count,
    x='year',
    y='ticket_count',
    # category_orders={'year': list(yearly_count['year'])},
    labels={'ticket_count': 'Number of Tickets', 'year': 'Year'},
    # title=f"จำนวน Ticket ของประเภท '{selected_type}' แยกตามปี"
)
fig.update_layout(
    xaxis=dict(
        type='category',  # 👈 บอกว่าแกนนี้เป็น category จริง ๆ
        categoryorder='array',
        categoryarray=sorted(yearly_count['year'].tolist(), key=int)  # เรียงปี
    )
)
st.plotly_chart(fig, use_container_width=True)

if len(df_selected) > 0:
    coords = df_selected[['latitude', 'longitude']]
    db = DBSCAN(eps=eps_value, min_samples=min_samples_value).fit(coords)
    df_selected['cluster'] = db.labels_

    # Filter out noise points
    df_selected = df_selected[df_selected['cluster'] != -1]

    # Count the number of points in each cluster and identify the largest clusters
    clusters_count = df_selected['cluster'].value_counts()

    # Exclude the '-1' cluster, which represents noise
    clusters_count = clusters_count[clusters_count.index != -1]

    unique_clusters = df_selected['cluster'].unique()
    num_clusters = len(unique_clusters)

    # Use a continuous colormap to generate colors, ensure we have enough colors for all clusters.
    colormap = plt.get_cmap('hsv')
    cluster_colors = {cluster: [int(x*255) for x in colormap(i/num_clusters)[:3]]
                        for i, cluster in enumerate(unique_clusters)}
        
    # Map cluster ID to color for each row in the dataframe
    df_selected['color'] = df_selected['cluster'].map(cluster_colors)

    st.subheader(f"Raw Data's DBSCAN of '{selected_type}' ")

    # Define the scatter plot layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        df_selected,
        get_position="[longitude, latitude]",
        get_color='color',
        get_radius=200,
        opacity=0.5,
        pickable=True
    )

    # Define the heatmap layer
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        df_selected,
        get_position="[longitude, latitude]",
        opacity=0.4,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=df_selected['latitude'].mean(),
        longitude=df_selected['longitude'].mean(),
        zoom=10
    )

    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer, heatmap_layer], 
        initial_view_state=view_state, 
        map_style=MAP_STYLES[map_style]
    ))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Summary")
        st.metric(label="Number of Tickets", value=len(df_selected))
        st.metric(label="Number of Clusters", value=num_clusters)
    with col2:
        top_3_clusters = clusters_count.head(3).reset_index()
        top_3_clusters.columns = ['Cluster ID', 'Ticket Count']

        st.markdown("### 🔝 Top 3 Clusters")
        st.table(top_3_clusters)
else:
    st.warning("⚠️ ไม่มีข้อมูลสำหรับประเภทและเขตที่เลือก")

st.header("Clean Data")

# st.subheader("🏢 Top 10 most responsible organizations")

st.subheader("🏢 Top 10 most responsible organizations")

org_counts = final_df['organization'].value_counts().reset_index()
org_counts.columns = ['organization', 'count']
top_orgs = org_counts.head(10)
fig = px.pie(
    top_orgs,
    # top_orgs_all,
    names='organization',
    values='count',
    title='All Type',
    hole=0.3  # ทำให้เป็น donut chart (ถ้าไม่ต้องการเอาออกได้)
)
st.plotly_chart(fig, use_container_width=True)

# st.subheader(f"🏢 Top 10 organizations responsible for '{selected_type}' ")
filtered_final_df = final_df[final_df[selected_type] == 1]
org_counts = filtered_final_df['organization'].value_counts().reset_index()
org_counts.columns = ['organization', 'count']

# Top 10
top_orgs = org_counts.head(10)

# Plot
fig = px.pie(
    top_orgs,
    names='organization',
    values='count',
    title=f"'{selected_type}' Type",
    hole=0.3
)
st.plotly_chart(fig, use_container_width=True)

# นับจำนวน Ticket ของแต่ละประเภท (type column ที่เป็น 1)
type_cols = [col for col in final_df.columns if col not in ['Unnamed: 0','ticket_id', 'organization', 'comment', 'longitude', 'latitude', 'district', 'subdistrict', 'timestamp']]
type_counts = final_df[type_cols].sum().reset_index()
type_counts.columns = ['type', 'count']
# Pie Chart
fig = px.pie(
    type_counts,
    names='type',
    values='count',
    title="Proportion of Each Issue Type",
    hole=0.3  # Optional: donut style
)
st.plotly_chart(fig, use_container_width=True)

org_df = final_df[final_df['organization'] == selected_org].copy()
org_df[['longitude', 'latitude']] = org_df['coords'].str.strip('[]').str.split(',', expand=True).astype(float)
# final_df[['longitude', 'latitude']] = final_df['coords'].apply(eval).apply(pd.Series)
# coords = final_df[['latitude', 'longitude']]
coords = org_df[['latitude', 'longitude']]
db = DBSCAN(eps=eps_value, min_samples=min_samples_value).fit(coords)
org_df['cluster'] = db.labels_
org_df = org_df[org_df['cluster'] != -1]
clusters_count = org_df['cluster'].value_counts()
clusters_count = clusters_count[clusters_count.index != -1]
unique_clusters = org_df['cluster'].unique()
num_clusters = len(unique_clusters)

colormap = plt.get_cmap('hsv')
cluster_colors = {cluster: [int(x*255) for x in colormap(i/num_clusters)[:3]]
                  for i, cluster in enumerate(unique_clusters)}
org_df['color'] = org_df['cluster'].map(cluster_colors)

st.subheader(f"🗺️ DBSCAN Clustering by '{selected_org}' Organization")

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    org_df,
    get_position="[longitude, latitude]",
    get_color='color',
    get_radius=200,
    opacity=0.5,
    pickable=True
)

heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    org_df,
    get_position="[longitude, latitude]",
    opacity=0.4,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=org_df['latitude'].mean(),
    longitude=org_df['longitude'].mean(),
    zoom=10
)

st.pydeck_chart(pdk.Deck(
    layers=[scatter_layer, heatmap_layer],
    initial_view_state=view_state,
    map_style=MAP_STYLES[map_style]
))

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📊 Summary (Organizations)")
    st.metric(label="Number of Tickets", value=len(org_df))
    st.metric(label="Number of Clusters", value=num_clusters)
with col2:
    top_3_clusters = clusters_count.head(3).reset_index()
    top_3_clusters.columns = ['Cluster ID', 'Ticket Count']
    st.markdown("### 🔝 Top 3 Clusters")
    st.table(top_3_clusters)

df_type_selected = final_df[final_df[selected_type] == 1].copy()
df_type_selected[['longitude', 'latitude']] = df_type_selected['coords'].str.strip('[]').str.split(',', expand=True).astype(float)
coords = df_type_selected[['longitude', 'latitude']] 
db = DBSCAN(eps=eps_value, min_samples=min_samples_value).fit(coords)
df_type_selected['cluster'] = db.labels_

# ตัด noise
df_type_selected = df_type_selected[df_type_selected['cluster'] != -1]

clusters_count = df_type_selected['cluster'].value_counts()
unique_clusters = df_type_selected['cluster'].unique()
num_clusters = len(unique_clusters)

# สร้างสี
colormap = plt.get_cmap('hsv')
cluster_colors = {cluster: [int(x*255) for x in colormap(i/num_clusters)[:3]]
                      for i, cluster in enumerate(unique_clusters)}
df_type_selected['color'] = df_type_selected['cluster'].map(cluster_colors)

# แสดงผล
st.subheader(f"🗺️ DBSCAN Clustering for Type '{selected_type}'")

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    df_type_selected,
    get_position='[longitude, latitude]',
    get_color='color',
    get_radius=200,
    opacity=0.5,
    pickable=True
)

heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    df_type_selected,
    get_position='[longitude, latitude]',
    opacity=0.4,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df_type_selected['latitude'].mean(),
    longitude=df_type_selected['longitude'].mean(),
    zoom=10
)

st.pydeck_chart(pdk.Deck(
    layers=[scatter_layer, heatmap_layer],
    initial_view_state=view_state,
    map_style=MAP_STYLES[map_style]
))
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📊 Summary (Type)")
    st.metric(label="Number of Tickets", value=len(df_type_selected))
    st.metric(label="Number of Clusters", value=num_clusters)
with col2:
    top_3_clusters = clusters_count.head(3).reset_index()
    top_3_clusters.columns = ['Cluster ID', 'Ticket Count']
    st.markdown("### 🔝 Top 3 Clusters")
    st.table(top_3_clusters)
