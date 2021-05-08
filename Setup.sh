#!/bin/bash

# Author: Iliana Papadopoulou

# Create new conda environmen
conda create --name network_visual_env python=3.7.3

# Activate the environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate network_visual_env

# Install the application requirements:

pip install plotly==4.14.3
pip install dash==1.20.0
pip install networkx==2.5.1
pip install pandas==1.2.4
pip install xlrd==2.0.1
pip install openpyxl==3.0.7
pip install matplotlib==3.4.1
pip install gunicorn==20.1.0 *

# Run the application locally:
python app.py
