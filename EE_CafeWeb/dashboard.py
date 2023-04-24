
import functools

#Our webapp libraries
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, Response)
from EE_CafeWeb.db import get_db
from EE_CafeWeb.home import login_required

#Our os 
import os
import io
import json

#We will use both the sdk and api for Cisco Meraki this is the library SDK
import requests
import asyncio
from requests_oauthlib import OAuth1Session
import meraki
import meraki.aio


# For drawing visualizatins directly with python
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import time

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

class NoRebuildAuthSession():
 def rebuild_auth(self, prepared_request, response):
   '''
   No code here means requests will always preserve the Authorization header when redirected.
   Be careful not to leak your credentials to untrusted hosts!
   '''

@blueprint_dash.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    if g.user is not None:
        if request.method == "GET":
            return render_template('dashboard/dashboard.html')
        elif request.method == "POST":
            return render_template('dashboard/dashboard.html')
        else:
            #return render_template('auth.login'), 405, {'Content-Type': 'application/json'}
            return render_template('dashboard/dashboard.html')
    else:
        #return render_template('auth.login')
        #only use login less dash under testing conditions.
        return render_template('dashboard/dashboard.html')

@blueprint_dash.route('/meraki_user_authorize_API', methods=('GET', 'POST'))
@login_required
def meraki_user_authorize_API():
    try:
        session = NoRebuildAuthSession()
        API_KEY = X-Cisco-Meraki-API-Key
        response = session.get('https://api.meraki.com/api/v1/organizations/', headers={'Authorization': f'Bearer {API_KEY}'})
        auth_data = response.json()
        auth_df = pd.DataFrame(auth_data) 
        return render_template('dashboard/dashboard.html', response=response)
    except Exception as error:
        return render_template('dashboard/dashboard.html', personal_auth=error)   
 

@blueprint_dash.route('/meraki_user_authorize_SDK', methods=('GET', 'POST'))
@login_required
def meraki_user_authorize_SDK():
    try:
        dashboard = meraki.DashboardAPI(API_KEY)
        response = dashboard.organizations.getOrganizations()
        authorize_data =response 
        return render_template('dashboard/dashboard.html', response=response)
    except Exception as error:
        return render_template('dashboard/dashboard.html', personal_auth=error)   
 

@blueprint_dash.route('/orgs', methods=('GET', 'POST'))
@login_required
async def get_orgs(organization_Id):
    payload = {'bandwidthLimits': bandwidth_limits}
    response = requests.put(f'{url} /organizations/{organizationId}/summary/top/clients/byUsage', headers=headers, json=payload)
    if response.status_code == 200:
        return render_template('dashboard/dashboard.html', health_alerts=health_alerts)
    else:
        return response.status_code

#Combine response API data to create one graph visualization that refreshes instead of several seperate functions.  
@blueprint_dash.route('/health_alerts', methods=('GET', 'POST'))
@login_required
async def get_health_alerts(network_id):
    payload = {'networks': network_id}
    response = requests.put(f'{url}/networks/{network_id}/health/alerts', headers=headers, json=payload)
    if response.status_code == 200:
        return render_template('dashboard/dashboard.html', response=response)
    else:
        return response.status_code

 

@blueprint_dash.route('/networks', methods=('GET', 'POST'))
#@login_required
async def get_networks(aiomeraki: meraki.aio.AsyncDashboardAPI, org):
    try:
        networks = await aiomeraki.clients.getOrganizationNetworks(
            org["id"]
        )
    except meraki.AsyncAPIError as eM:
        return eM
    except Exception as e:
        return e
    else:
        if clients:
            #update dashboard on webpage.
            return networks
    return org["id"], None

@blueprint_dash.route('/devices', methods=('GET', 'POST'))
@login_required
async def get_devices(aiomeraki: meraki.aio.AsyncDashboardAPI, network):
    try:
        clients = await aiomeraki.clients.getNetworkClients(
            network["id"],
            timespan=60*60*24,
            perPage=1000,
            total_pages="all",
        )
    except meraki.AsyncAPIError as eM:
        return eM
    except Exception as e:
        return e
    else:
        if clients:
            #update dashboard on webpage.
            return network["name"], field_names
    return network["name"], None


@blueprint_dash.route('/bandwidth_perc', methods=('GET', 'POST'))
@login_required
async def allocate_bandwidth(network_id, bandwidth_limits):
    payload = {'bandwidthLimits': bandwidth_limits}
    response = requests.put(f'{url}/networks/{network_id}/trafficShaping', headers=headers, json=payload)
    if response.status_code == 200:
        return response
    else:
        return response.status_code

#Need to store original network plan or state...
# Then continue to wipe DB and reset original
# Maybe add warning flash prompt? 
@blueprint_dash.route('/resetNetworks', methods=('GET','POST'))
@login_required
def reset_Networks(network_id):
    payload = {}
    response = requests.put(f'{url}/networks/{network_id}/' , headers=headers, json=payload)
    return response.status_code


@blueprint_dash.route('/graph', methods=('GET', 'POST'))
@login_required
def graph():
    while(session):
        try:
            networks = get_networks()
            devices = get_devices()
            health_alets = get_health_alerts()

            networks_df = pd.DataFrame(networks)
            devices_df = pd.DataFrame(devices)
            health_alets_df = pd.DataFrame(health_alets)

            sns.set_style("whitegrid")
            networks_graph = sns.countplot(x="Network Name", data=networks_df)
            devices_graph = sns.countplot(x="Device Name", data=devices_df)
            health_alerts_graph = sns.countplot(x="Health Alerts", data=health_alerts_df)

            return render_template("dashboard/dashboard.html", networks_graph=networks_graph, devices_graph=devices_graph, health_alerts_graph=health_alerts_graph) 
        except:
            flash("Connection to Meraki failed.")
        finally:
            time.sleep(30)
   
    return render_template('dashboard/dashboard.html', personal_auth=error)
       