#Our webapp libraries
from flask import (Blueprint, flash, g, render_template, request, session)
from EE_CafeWeb.db import get_db
from EE_CafeWeb.home import login_required

#Our os 
import os


#We will use both the sdk and api for Cisco Meraki this is the library SDK
import requests
from requests_oauthlib import OAuth1Session
import meraki


import seaborn as sns


os.environ.get('XCiscoMerakiAPIKey')
url = 'https://api.meraki.com/api/v1'
headers = {
    'Content-Type': 'application/json',
    'X-Cisco-Meraki-API-Key': 'YOUR_API_KEY'
}

organization_Id = "EnterOrgId Here"
network_dict = {}
device_dict = {}

blueprint_dash = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def get_networks_and_devices(api_key):
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
    }
    url = 'https://api.meraki.com/api/v1/organizations/<ORGANIZATION_ID>/networks'
    response = requests.get(url, headers=headers)
    networks = response.json()

    networks_with_devices = []
    for network in networks:
        url = f'https://api.meraki.com/api/v1/networks/{network["id"]}/devices'
        response = requests.get(url, headers=headers)
        devices = response.json()
        network_with_devices = {
            'name': network['name'],
            'devices': devices
        }
        networks_with_devices.append(network_with_devices)

    return networks_with_devices

@blueprint_dash.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    api_key = '<YOUR_API_KEY>'
    networks_with_devices = get_networks_and_devices(api_key)

    # Create a Seaborn plot
    sns.set_style('whitegrid')
    for network in networks_with_devices:
        sns.scatterplot(x='serial', y='name', data=network['devices'])

    # Render the plot as an image and display it in the template
    figure = sns.plotting_context().get_figure()
    figure.savefig('static/plot.png')
    return render_template('index.html', networks_with_devices=networks_with_devices)
