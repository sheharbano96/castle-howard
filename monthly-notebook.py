#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import time, datetime, os, gc
from datetime import date, timedelta
import tables
mydate = datetime.datetime.now()
month = mydate.strftime("%b")
month = 'Dec'

year = mydate.strftime("%Y")
year = '2021'
# TODO - generate the right paths for each month instead of updating by hand

# We need to run MQAF with two different schemes, one gives stats for existence at high level 
# categories the second gives stats for existence per field (with some grouping allowed)

# These two outputs will be read in by pandas and written out in HD5 format so they can be read back in
# without each notebook needing to run the same DataFrame creation from csv each time
gc.collect()

base_path = os.path.dirname((os.path.dirname(os.path.realpath("__file__"))))
print(base_path)
current_path = f'{base_path}/data-lfs/objects/{year}/{month}'
print(current_path)
# Concept
# concept_df = pd.concat(map(pd.read_csv, glob.glob(f'{current_path}/concept/*.csv')))
# concept_df.to_hdf(f"{current_path}/concept-{year}-{month}.h5", key=f'vam_concept_{year}_{month}', complevel=7, mode='w')
# gc.collect()

# # Field
# field_df = pd.concat(map(pd.read_csv, glob.glob(f'{current_path}/field/*.csv')))
# field_df.to_hdf(f"{current_path}/field-{year}-{month}.h5", key=f'vam_field_{year}_{month}', complevel=7, mode='w')
# gc.collect()

# # Retrieval
# retrieval_df = pd.concat(map(pd.read_csv, glob.glob(f'{current_path}/retrieval/*.csv')))
# retrieval_df.to_hdf(f"{current_path}/retrieval-{year}-{month}.h5", key=f'vam_retrieval_{year}_{month}', complevel=7, mode='w')
# gc.collect()

