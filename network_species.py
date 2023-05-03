import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)
df = pd.read_csv('network_data.csv')
# Set header title
st.title('Madagascar Camera Trap Network')
st.write('source data: Wampole, Erin M., Gerber, Brian D., Farris, Zach J., Razafimahaimodison, Jean Claude, Andrianarisoa, Mahandry Hugues, Ralazampirenena, Claude Jacquot, Wright, Patricia C., et al. 2022. Madagascar Terrestrial Camera Survey Database 2021: A Collation of Protected Forest Camera Surveys from 2007–2021. Ecology 103( 6): e3687. https://doi.org/10.1002/ecy.3687')


st.markdown('---')
st.subheader('Species Data')
sp_filter = st.selectbox("Select/Type the Species", pd.unique(df["common_name"].str.upper().sort_values()))
df2 = df[df["common_name"].str.upper() == sp_filter]

if sp_filter:
    species = nx.from_pandas_edgelist(df2, 'common_name', 'site', 'weight')

    # Initiate PyVis network object
    anim_net = Network(height='465px', bgcolor='white', font_color='blue')

    # Take Networkx graph and translate it to a PyVis graph format
    anim_net.from_nx(species)

    # Generate network with specific layout settings
    anim_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        anim_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        anim_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=600)
    st.dataframe(df2)

#si_filter = st.selectbox("Select/Type the Site", pd.unique(df["site"].str.upper().sort_values()))
#df3 = df[df["site"].str.upper() == si_filter]

st.markdown('---')
st.subheader('Site Data')
site_list = ['MAK','ASSR','BET','MAS','MTD','RNP','TGK']
site_list.sort()
selected_sites = st.multiselect('Select site(s) to visualize', site_list)
if len(site_list) == 0:
    st.text('Please select 1 or more sites')
else:
    si_select = df.loc[df['site'].isin(selected_sites)]
    si_select = si_select.reset_index(drop=True)

    sites = nx.from_pandas_edgelist(si_select, 'common_name', 'site')

    # Initiate PyVis network object
    site_net = Network(height='1000px', bgcolor='white', font_color='blue')

    # Take Networkx graph and translate it to a PyVis graph format
    site_net.from_nx(sites)

    # Generate network with specific layout settings
    site_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)

    for node in site_net.nodes:
        if node['id'] == 'MAK':
            node['color'] = '#440154ff'
        elif node['id'] == 'ASSR':
            node['color'] = '#453781ff'
        elif node['id'] == 'BET':
            node['color'] = '#33638dff'
        elif node['id'] == 'MAS':
            node['color'] = '#238a8dff'
        elif node['id'] == 'MTD':
            node['color'] = '#29af7fff'
        elif node['id'] == 'RNP':
            node['color'] = '#73d055ff'
        elif node['id'] == 'TGK':
            node['color'] = '#dcde319ff'
        else:
            node ['color'] = 'black'
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        site_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        site_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=1100)
    #st.dataframe(sites)
