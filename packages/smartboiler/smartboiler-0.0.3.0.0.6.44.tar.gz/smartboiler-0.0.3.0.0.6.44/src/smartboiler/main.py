from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from flask import Flask, request, make_response, render_template
from jinja2 import Environment, PackageLoader
from requests import get
from waitress import serve
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import os, json, argparse, pickle, yaml, logging
from distutils.util import strtobool
import pandas as pd

from smartboiler.command_line import set_input_data_dict
from smartboiler.command_line import perfect_forecast_optim, dayahead_forecast_optim, naive_mpc_optim
from smartboiler.command_line import forecast_model_fit, forecast_model_predict, forecast_model_tune
from smartboiler.command_line import publish_data
from smartboiler.utils import get_injection_dict, get_injection_dict_forecast_model_fit, \
    get_injection_dict_forecast_model_tune, build_params
# Define the Flask instance
app = Flask(__name__)

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='The URL to your Home Assistant instance, ex the external_url in your hass configuration')
    parser.add_argument('--key', type=str, help='Your access key. If using smartboiler in standalone this should be a Long-Lived Access Token')
    parser.add_argument('--addon', type=strtobool, default='False', help='Define if we are usinng EMHASS with the add-on or in standalone mode')
    args = parser.parse_args()
    
    use_options = os.getenv('USE_OPTIONS', default=False)
    # Define the paths
    if args.addon==1:
        OPTIONS_PATH = os.getenv('OPTIONS_PATH', default="/data/options.json")
        options_json = Path(OPTIONS_PATH)
        CONFIG_PATH = os.getenv("CONFIG_PATH", default="/usr/src/config_smartboiler.yaml")
        hass_url = args.url
        key = args.key
        # Read options info
        if options_json.exists():
            with options_json.open('r') as data:
                options = json.load(data)
        else:
            app.logger.error("options.json does not exists")
        DATA_PATH = "/share/" #"/data/"
    else:
        if use_options:
            OPTIONS_PATH = os.getenv('OPTIONS_PATH', default="/app/options.json")
            options_json = Path(OPTIONS_PATH)
            # Read options info
            if options_json.exists():
                with options_json.open('r') as data:
                    options = json.load(data)
            else:
                app.logger.error("options.json does not exists")
        else:
            options = None
        CONFIG_PATH = os.getenv("CONFIG_PATH", default="/app/config_emhass.yaml")
        DATA_PATH = os.getenv("DATA_PATH", default="/app/data/")

    config_path = Path(CONFIG_PATH)
    data_path = Path(DATA_PATH)
    
    # Read the example default config file
    if config_path.exists():
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        retrieve_smartboiler_conf = config['retrieve_smartboiler_conf']
        optim_conf = config['optim_conf']
        plant_conf = config['plant_conf']
    else:
        app.logger.error("Unable to open the default configuration yaml file")
        app.logger.info("Failed config_path: "+str(config_path))

    params = {}
    params['retrieve_smartboiler_conf'] = retrieve_smartboiler_conf
    params['optim_conf'] = optim_conf
    params['plant_conf'] = plant_conf
    web_ui_url = '0.0.0.0'

    # Initialize this global dict
    if (data_path / 'injection_dict.pkl').exists():
        with open(str(data_path / 'injection_dict.pkl'), "rb") as fid:
            injection_dict = pickle.load(fid)
    else:
        injection_dict = None
    
    if args.addon==1:
        # The cost function
        costfun = options.get('costfun', 'profit')
        # Some data from options
        logging_level = options.get('logging_level','INFO')
        url_from_options = options.get('hass_url', 'empty')
        if url_from_options == 'empty' or url_from_options == '':
            url = hass_url+"/config"
        else:
            hass_url = url_from_options
            url = hass_url+"/api/config"
        token_from_options = options.get('long_lived_token', 'empty')
        if token_from_options == 'empty' or token_from_options == '':
            long_lived_token = key
        else:
            long_lived_token = token_from_options
        headers = {
            "Authorization": "Bearer " + long_lived_token,
            "content-type": "application/json"
        }
        response = get(url, headers=headers)
        config_hass = response.json()
        params_secrets = {
            'hass_url': hass_url,
            'long_lived_token': long_lived_token,
            'time_zone': config_hass['time_zone'],
            'lat': config_hass['latitude'],
            'lon': config_hass['longitude'],
            'alt': config_hass['elevation']
        }
    else:
        costfun = os.getenv('LOCAL_COSTFUN', default='profit')
        logging_level = os.getenv('LOGGING_LEVEL', default='INFO')
        with open(os.getenv('SECRETS_PATH', default='/app/secrets_emhass.yaml'), 'r') as file:
            params_secrets = yaml.load(file, Loader=yaml.FullLoader)
        hass_url = params_secrets['hass_url']
        
    # Build params
    if use_options:
        params = build_params(params, params_secrets, options, 1, app.logger)
    else:
        params = build_params(params, params_secrets, options, args.addon, app.logger)
    with open(str(data_path / 'params.pkl'), "wb") as fid:
        pickle.dump((config_path, params), fid)

    # Define logger
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    if logging_level == "DEBUG":
        app.logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    elif logging_level == "INFO":
        app.logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)
    elif logging_level == "WARNING":
        app.logger.setLevel(logging.WARNING)
        ch.setLevel(logging.WARNING)
    elif logging_level == "ERROR":
        app.logger.setLevel(logging.ERROR)
        ch.setLevel(logging.ERROR)
    else:
        app.logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    app.logger.propagate = False
    app.logger.addHandler(ch)
    
    # Launch server
    port = int(os.environ.get('PORT', 5000))
    app.logger.info("Launching the emhass webserver at: http://"+web_ui_url+":"+str(port))
    app.logger.info("Home Assistant data fetch will be performed using url: "+hass_url)
    app.logger.info("The data path is: "+str(data_path))
    try:
        app.logger.info("Using core emhass version: "+version('emhass'))
    except PackageNotFoundError:
        app.logger.info("Using development emhass version")
    serve(app, host=web_ui_url, port=port, threads=8)