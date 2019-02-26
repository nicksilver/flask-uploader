
from flask import render_template, flash, redirect, request
from app import app
from app.forms import UploadForm
import pandas as pd
import numpy as np
from datetime import datetime

# Helper functions
def get_cols(df_level, level):
    # Returns columns to be concatenated
    f = df_level.level_formula[df_level.level_value==level].iloc[0]
    return f.split('+')

def get_area_table(df_hist, df_level, level):
    # Returns area table for specified level
    cols = get_cols(df_level, level)
    parent_level = level+1
    if level == df_level.level_value.max():
        area_ids = np.repeat('DOTA', len(df_hist))
        parent_ids = np.repeat('NA', len(df_hist))
    elif level == df_level.level_value.max()-1:
        parent_ids = np.repeat('DOTA', len(df_hist))
        area_ids = df_hist.apply(lambda row: "".join([str(row[col]) for col in cols]), axis=1)
    else:
        area_ids = df_hist.apply(lambda row: "".join([str(row[col]) for col in cols]), axis=1)
        parent_cols = get_cols(df_level, parent_level)
        parent_ids = df_hist.apply(lambda row: "".join([str(row[col]) for col in parent_cols]), axis=1)
    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    time_stamps = np.repeat(created, len(df_hist))
    levels = np.repeat(level, len(df_hist))
    org_id = df_level.org_id[df_level.level_value==level].iloc[0]
    org_ids = np.repeat(org_id, len(df_hist))

    dict = {
        'time_stamp': time_stamps.tolist(),
        'org_id': org_ids.tolist(),
        'level': levels.tolist(),
        'area_id': area_ids.tolist(),
        'parent_id': parent_ids.tolist()
    }
    return pd.DataFrame(dict)

# Flask routing
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file_level = request.files['file_level']
        file_historical = request.files['file_histyield']
        if file_level and file_historical:
            df_level = pd.read_csv(file_level)
            df_hist = pd.read_csv(file_historical)
            df = pd.DataFrame()
            for level in df_level.level_value:
                df_new = get_area_table(df_hist, df_level, level)
                df = pd.concat([df, df_new], ignore_index=True)
            return render_template('uploader.html', title='File Upload', df = df.to_html(index=False))
    return render_template('upload.html', title='File Upload', form = form)
