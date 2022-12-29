import pandas as pd
import numpy as np
import streamlit as st
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.graph_objects as go
import leafmap
import leafmap.foliumap as leafmap


APP_TITLE = 'Visualisasi Data POI'
df_desa= pd.read_csv('C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/CSV/demografi_jakarta_utara.csv')

def display_filter_desa(join_right_df):
    desa_list = ['ALL']+list(join_right_df['nama_desa'].unique())
    desa_list.sort()
    desa = st.sidebar.selectbox('Nama Desa', desa_list)
    return desa

def display_kategori_filters(df_jkt):
    kategori_list = ['Belum Memilih']+list(df_jkt['nama_kategori'].unique())
    kategori_list.sort()
    kategori = st.sidebar.selectbox('Pilih Kategori POI :', kategori_list)
    return kategori

def multiselect_kategori_filters(df_jkt):
    kategori_list = ['Belum Memilih']+list(df_jkt['nama_kategori'].unique())
    kategori_list.sort()
    selectbox = st.sidebar.multiselect('Pilih Kategori POI :', kategori_list)
    return selectbox

def radiobox_pilih_kategori():
    radio= st.sidebar.radio(
        "Pilih Value",
        ('Jumlah Kategori POI', 'Jumlah Penduduk'))
    return radio

    
def ratio(df):
    agg_tips=df[['nama_desa', 'PRIA', 'WANITA', 'JUMLAH_PEN']]
    agg_tips=agg_tips.sort_values('JUMLAH_PEN')
    agg_tips=agg_tips[['nama_desa', 'PRIA', 'WANITA']]
    agg_tips=agg_tips.set_index('nama_desa')

    fig, ax = plt.subplots()

    # Initialize the bottom at zero for the first set of bars.
    colors = ['#24b1d1', '#ae24d1']
    bottom = np.zeros(len(agg_tips))

    # Plot each layer of the bar, adding each bar to the "bottom" so
    # the next bar starts higher.
    for i, col in enumerate(agg_tips.columns):
        ax.bar(agg_tips.index, agg_tips[col], bottom=bottom, width=0.35, label=col
            ,color=colors[i])
        bottom += np.array(agg_tips[col])
    
    # # Sum up the rows of our data to get the total value of each bar.
    # totals = agg_tips.sum(axis=1)
    # # Set an offset that is used to bump the label up a bit above the bar.
    # y_offset = 4
    # # Add labels to each bar.
    # for i, total in enumerate(totals):
    #     ax.text(totals.index[i], total + y_offset, round(total), ha='center', weight='bold')
    
    ax.set_xlabel('Nama Desa')
    ax.set_ylabel('Jumlah Populasi')
    ax.set_xticks(df_desa['nama_desa'])
    ax.set_xticklabels(df_desa['nama_desa'], rotation=80)
    ax.set_title('Rasio Pria dan Wanita')
    ax.legend()

    st.pyplot(fig)

def ratio_Pria_dan_Wanita(df, desa):
    df_filter = df[(df['nama_desa'] == desa)]
    df_filter = df_filter[['PRIA', 'WANITA']].drop_duplicates().T
    df_filter = df_filter.reset_index().rename(columns={'index': 'gender'})
    df_filter = df_filter.rename(columns={ df_filter.columns[1]: "jumlah" })


    pie_colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',  
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)', 'RGB(186,85,211)', 'RGB(224,102,255)',
          'RGB(209,95,238)', 'RGB(180,82,205)', 'RGB(122,55,139)']
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df_filter['gender'].to_list(),
        values=df_filter.jumlah.to_list(),
        name='gender',
        hoverinfo="label+percent+value",
        marker_colors=pie_colors
    ))

    fig.update_layout(
        title="Responden Form Berdasarkan Gender",
        height= 330,
        width= 345,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)'
    )
    st.plotly_chart(fig)

def bar_chart_filter(df, desa):
    df_filter=df[(df['nama_desa'] == desa)]
    df_sort=df_filter.groupby('nama_kategori')['gid'].count().sort_values(ascending=True)
    df_sort_to_frame=df_sort.to_frame()
    data=df_sort_to_frame.reset_index()
    
    kategori = data['nama_kategori']
    jumlah_data = data['gid']

    x = np.arange(len(kategori)) # the label locations
    width = 0.8 # the width of the bars

    fig, ax = plt.subplots()

    #bar_labels = ['red', 'yellow', 'green', 'blue', 'navy', 'black', 'purple', 'orange', 'brown', 'grey', 'pink', 'gold']
    bar_colors = ['red', 'yellow', 'green', 'blue', 'navy', 'black', 'purple', 'orange', 'brown', 'grey', 'pink', 'gold']
    ax.set_xlabel('Nama Kategori')
    ax.set_ylabel('Jumlah Kategori')
    ax.set_title('Visualisasi Data POI')
    ax.set_xticks(x)
    ax.set_xticklabels(kategori, rotation=80)

    pps = ax.bar(x - width/2, jumlah_data, width, color=bar_colors)
    for p in pps:
        height = p.get_height()
        ax.annotate('{}'.format(height),
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 3), # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    st.pyplot(fig)

def bar_chart(data):
    kategori = data['nama_kategori']
    jumlah_data = data['gid']

    x = np.arange(len(kategori)) # the label locations
    width = 0.80 # the width of the bars

    fig, ax = plt.subplots()

    bar_colors = ['red', 'yellow', 'green', 'blue', 'navy', 'black', 'purple', 'orange', 'brown', 'grey', 'pink', 'gold']
    ax.set_xlabel('Nama Kategori')
    ax.set_ylabel('Jumlah Kategori')
    ax.set_title('Visualisasi Data POI')
    ax.set_xticks(x)
    ax.set_xticklabels(kategori, rotation=80)

    pps = ax.bar(x - width/2, jumlah_data, width, color=bar_colors)
    for p in pps:
        height = p.get_height()
        ax.annotate('{}'.format(height),
        xy=(p.get_x() + p.get_width() / 2, height),
        xytext=(0, 3), # 3 points vertical offset
        textcoords="offset points",
        ha='center', va='bottom')

    st.pyplot(fig)

# def display_map(df_jkt, kategori, selectbox):
#     map = folium.Map(location=[-6.2, 106.90], zoom_start=11, scrollWhileZoom=False, tiles='cartodbdark_matter')

#     # choropleth = folium.Choropleth(
#     #     geo_data='demografi_jakarta_utara.geojson',
#     #     data=df_jkt,
#     #     columns=('nama_desa', 'JUMLAH_PEN'),
#     #     key_on='feature.properties.nama_desa',
#     #     fill_color='YlOrRd',
#     #     line_opacity=0.8,
#     #     legend_name='nama_desa',
#     #     highlight=True
#     # )
#     # choropleth.geojson.add_to(map)
#     #Loop through each row in the dataframe

#     selectbox=selectbox
#     df_jkt = df_jkt.query("nama_kategori in @selectbox")
#     for _, r in df_jkt.iterrows():
        
#         # Without simplifying the representation of each borough,
#         # the map might not be displayed
#         sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
#         geo_j = sim_geo.to_json()
#         geo_j = folium.GeoJson(data=geo_j)
#         #folium.Popup(r['nama_kategori']).add_to(geo_j)
#         folium.Popup(r['nama_merchant']).add_to(geo_j)
#         # folium.Marker(icon = folium.Icon(color='red'))
#         geo_j.add_to(map)

#     #selectbox=st.write(selectbox)
#     st_map=st_folium(map, width=700, height=450)
#     return st_map

def display_map(df_poi,selectbox):
    map=leafmap.Map(center=[-6.2, 106.90], zoom=12)
    df_jkt='C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/Geojson/demografi_jakarta_utara.geojson'
    selectbox=selectbox
    df_poi= df_poi.query("nama_kategori in @selectbox")
    map.add_geojson(df_jkt, layer_name='POI Jakarta Utara')
    map.add_data(df_jkt, column='JUMLAH_PEN', scheme='EqualInterval', cmap='OrRd', legend_title='Population',layer_name="Jumlah Penduduk")
    map.add_points_from_xy(
        df_poi,
        x="longitude",
        y="latitude",
        color_column='nama_kategori',
        #icon_names=['gear', 'map', 'leaf', 'globe','balance-scale', 'truck'],
        spin=True,
        add_legend=True,
    )
    map.to_streamlit(width=705, height=500)

def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

def display_bubble_map_all(df_poi, radio):
    n = folium.Map(location=[-6.2, 106.90], zoom_start=11, scrollWhileZoom=False, tiles='cartodbdark_matter')
    radio=radio
    if radio=='Jumlah Kategori POI':
        df_poi=df_poi.copy()
        jumlah_poi=[]
        for i in df_poi.nama_desa:
            nama_desa=df_poi[(df_poi['nama_desa'] == i)]
            jumlah_poi.append(len(nama_desa.gid))
        df_poi['jumlah_poi']=jumlah_poi

        #Pembagian minimal value radius
        x1=max(jumlah_poi)-1
        x2=int(x1/2)
        radius=[]
        color_radius=[]
        for i in df_poi.jumlah_poi:
            if i > x1:
                radius.append(15)
                color_radius.append('red')
            elif i > x2:
                radius.append(10)
                color_radius.append('yellow')
            else:
                radius.append(5)
                color_radius.append('blue')
        df_poi['radius']=radius
        df_poi['color_radius']=color_radius
        data=df_poi.copy()
        for row in data.iterrows():
            row_values = row[1]
            location = [row_values['lat_centroid'], row_values['lon_centroid']]
            popup = (row_values['nama_desa'])
            color=(row_values['color_radius'])
            radius=(row_values['radius'])

            marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
            marker.add_to(n)
    
        legend_map = add_categorical_legend(n,'Legend',
                                            colors = ['green', 'blue', 'yellow', 'red'],
                                            labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
                                            )
        fs=folium_static(legend_map, width = 705, height = 500)  
    else:
        df_poi=df_poi.copy()
        #Pembagian minimal value radius
        x1=int(df_poi.JUMLAH_PEN.max())-1
        x2=int(x1/2)
        radius=[]
        color_radius=[]
        for i in df_poi.JUMLAH_PEN:
            if i > x1:
                radius.append(15)
                color_radius.append('red')
            elif i > x2:
                radius.append(10)
                color_radius.append('yellow')
            else:
                radius.append(5)
                color_radius.append('blue')
        df_poi['radius_jumlah_pen']=radius
        df_poi['color_radius_jumlah_pen']=color_radius
        data=df_poi.copy()
        for row in data.iterrows():
            row_values = row[1]
            location = [row_values['lat_centroid'], row_values['lon_centroid']]
            popup = (row_values['nama_desa'])
            color=(row_values['color_radius_jumlah_pen'])
            radius=(row_values['radius_jumlah_pen'])

            marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
            marker.add_to(n)
    
        legend_map = add_categorical_legend(n,'Legend',
                                            colors = ['green', 'blue', 'yellow', 'red'],
                                            labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
                                            )
        fs=folium_static(legend_map, width = 705, height = 500)
    return fs

#addcolor colom
def categorycolors(counter):
    if counter['nama_kategori'] == 'Law & Defend':
        return 'green'
    elif counter['nama_kategori'] == 'Transportation and Logistic':
        return 'blue'
    elif counter['nama_kategori'] == 'Entertainment':
        return 'red'
    elif counter['nama_kategori'] == 'Market':
        return 'purple'
    elif counter['nama_kategori'] == 'Education':
        return 'orange'
    elif counter['nama_kategori'] == 'Property':
        return 'darkred'
    elif counter['nama_kategori'] == 'Social Economy':
        return 'lightred'
    elif counter['nama_kategori'] == 'Sport':
        return 'beige'
    elif counter['nama_kategori'] == 'Tourism':
        return 'darkblue'
    elif counter['nama_kategori'] == 'Medical':
        return 'darkgreen'
    elif counter['nama_kategori'] == 'Commercial':
        return 'cadetblue'
    else:
        return 'gray'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)

    #load_data
    df_poi = pd.read_csv('C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/CSV/poi.csv')
    df_desa= pd.read_csv('C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/CSV/demografi_jakarta_utara.csv')

    df_jkt = gpd.read_file('C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/Geojson/demografi_jakarta_utara.geojson')
    geoPOI=gpd.read_file('C:/Users/ajiba/OneDrive/Documents/streamlit/Dataset/Geojson/poi.geojson')

    #Join
    geoPOI.crs = df_jkt.crs
    join_right_df = geoPOI.sjoin(df_jkt, how="right")
    join_left_df = geoPOI.sjoin(df_jkt, how="left")

    #addcolor
    df_poi['color']=df_poi.apply(categorycolors, axis=1)
    join_right_df['color']=join_right_df.apply(categorycolors, axis=1)
    join_right_df = join_right_df.to_crs(4326)
    join_right_df['lon_centroid'] = join_right_df.centroid.x  
    join_right_df['lat_centroid'] = join_right_df.centroid.y
    jumlah_poi=[]
    for i in join_right_df.nama_desa:
        nama_desa=join_right_df[(join_right_df['nama_desa'] == i)]
        jumlah_poi.append(len(nama_desa.gid))
    join_right_df['jumlah_poi']=jumlah_poi

    # Display Visual and maps
    #maps
    # kategori = display_kategori_filters(df_jkt=join_left_df)
    #selectbox= multiselect_kategori_filters(df_jkt=join_left_df)
    selectbox= multiselect_kategori_filters(df_jkt=df_poi)
    desa=display_filter_desa(join_right_df)
    
    #display_map(df_jkt=join_left_df, kategori=kategori, selectbox=selectbox)
    display_map(df_poi,selectbox)
    col1, col2 = st.columns(2)

    with col1:
        if desa=='ALL':
            jumlah_kategori=df_poi.groupby('nama_kategori')['gid'].count().sort_values(ascending=True)
            data=jumlah_kategori.to_frame()
            data=data.reset_index()
            st.markdown('Visualisasi Jumlah Kategori POI.')
            bar_chart(data)
            
        else:
            st.markdown('Visualisasi Jumlah Kategori POI.')
            bar_chart_filter(df=join_right_df, desa=desa)
            

    with col2:
        if desa=='ALL':
            jumlah_kategori=df_poi.groupby('nama_kategori')['gid'].count().sort_values(ascending=True)
            data=jumlah_kategori.to_frame()
            data=data.reset_index()
            st.markdown('Visualisasi Ratio Pria dan Wanita.')
            ratio(df_desa)
        else:
            st.markdown('Visualisasi Ratio Pria dan Wanita.')
            ratio_Pria_dan_Wanita(df=join_right_df, desa=desa)
    radio = radiobox_pilih_kategori()
    st.markdown('Visualisasi Bubble Maps.')
    display_bubble_map_all(df_poi=join_right_df, radio=radio)

    # if desa=='ALL':
    #     jumlah_kategori=df_poi.groupby('nama_kategori')['gid'].count().sort_values(ascending=True)
    #     data=jumlah_kategori.to_frame()
    #     data=data.reset_index()
    #     st.markdown('Visualisasi Jumlah Kategori POI.')
    #     bar_chart(data)
    #     st.markdown('Visualisasi Ratio Pria dan Wanita.')
    #     ratio(df_desa)
    # else:
    #     st.markdown('Visualisasi Jumlah Kategori POI.')
    #     bar_chart_filter(df=join_right_df, desa=desa)
    #     st.markdown('Visualisasi Ratio Pria dan Wanita.')
    #     ratio_Pria_dan_Wanita(df=join_right_df, desa=desa)

if __name__ == "__main__":
    main()