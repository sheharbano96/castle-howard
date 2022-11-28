# Created new file to send through the stats as a single message to slack. 

import csv, argparse, os, datetime
import pandas as pd
import seaborn as sn
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import numpy as np

date = datetime.datetime.now().strftime("%d_%B_%Y")
day = datetime.datetime.now().strftime("%A")
iso_date_format = "%Y/%b/%d"
data_date = datetime.datetime.now().strftime(iso_date_format)

# Path to the files
base_path = '/srv/explore-the-collections'
csvFilePath = f'{base_path}/stats/{data_date}/daily_export_stats_{date}.csv'
image_path = f"{base_path}/stats/{data_date}/daily_export_stats_{date}.png"
example_id_path = f'{base_path}/stats/{data_date}/daily_export_example_object.txt'

class css:
    cell_hover = {  
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #0D669D; color: white;'
    }

class config:
    # channel_id = 'C03GJPTPABD' #testing
    channel_id = 'C026C3J8M71' #updates-etc
    url = "https://hooks.slack.com/services/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"
    bot_token = "xoxb-2804676283-3576291316401-8mPxAj9UWdFNHM5i5EAGAuVr"



def highlight_max(df_styled, props=''):
    return np.where(df_styled.isin([0]), props, '')


# Reading in the csv file, creating table visualization and creating an image of it.
df = pd.read_csv(csvFilePath)
df.sort_values(by="Total Record Count", ascending=False, inplace= True)
### Not using dataframe_image package as it requires chrome to create an image and we can't have it on the server. ###
# import dataframe_image as dfi
# cm = sn.color_palette("Greens", as_cmap=True)
# df_styled = df.style.background_gradient(cmap=cm).set_table_attributes("style='display:inline'").set_properties(**{'text-align': 'left'}).set_table_styles([css.cell_hover, css.index_names, css.headers]).set_precision(3)
# df_styled.apply(highlight_max, props='color:white;background-color:red', axis= None)
# dfi.export(df_styled, image_path)

### Using plotly to create an image of csv instead.###
import plotly.graph_objects as go


fig = go.Figure(data=[go.Table(header=dict(values=df.columns.to_list(), line_color='darkslategray',
    fill_color='#0D669D',
    align=['left','center'],
    font=dict(color='white', size=24),
    height=40),
    cells=dict(values=[df['Export Scope'].to_list(), df['Type'].to_list() ,df['Total Record Count'].to_list(), df['New Records Count'].to_list()],     
    line_color='darkslategray',
    fill_color= np.select([df.T.values == 0], ["#e3646e"], "white"),
    align=['left', 'center'],
    font_size=22,
    height=30,
    font_color='black'))
                     ])
# Change margins
fig.update_layout(
    autosize=False,
    margin=dict(
        l=2,
        r=0,
        b=1,
        t=1,
        pad=2
    ),
    height = 600
)
fig.update_xaxes(automargin=True)
fig.write_image(image_path)


line = ''

# Sending the stats as a slack msg
try:
    client = WebClient(token=config.bot_token)

    if df.loc[df['Type'] == 'Objects', 'Total Record Count'].iloc[0] == 0 and day != 'Monday':
        text = ':warning: *WARNING! ZERO OBJECTS EXPORTED FROM SSL.*'
        desc = ''
    else:
        text = "Today's export stats :calendar:!"
        if os.path.exists(example_id_path):
            with open(example_id_path, 'r') as f: line = f.readline() 
            desc = f'Example created object: {line}'
        else: 
            desc = ''

    result = client.files_upload(channels=config.channel_id, file=image_path, filename=f"Daily Export Stats {date}", title= f"Daily Export Stats {date}", initial_comment= text)
    
    if line != '':
        response = client.chat_postMessage(channel = config.channel_id, text=desc)


except SlackApiError as e:
    print(f"Error uploading file: {e}")



