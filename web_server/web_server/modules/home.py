import random

from web_server import app

from flask import request
from flask import render_template

from web_server.modules.server_requests import get

# HOME
@app.route("/")
def home():
    if 'interpolate_places' in request.args:
        get('places?interpolate_places')
        return ("Interpolation OK")
    elif 'rebuild_places' in request.args:
        get('places?rebuild_places')
        return ("Rebuild OK")

    msg = ""
    query = ""
    product = ""
    product_name = "todo"
    activity = ""
    activity_name = ""
    latitude = ""
    longitude = ""
    page = "1"
    here = False
    place_id = ""
    place_full_name = ""
    location_name = "cualquier lado"
    subtitle = ""
    page_description = "Alimentación Consciente, Vida Sustentable y Comercio Justo"
    items = []

    if 'store' in request.args:
        items = get('stores/{0}'.format(request.args['store']))
        product_name = items[0]['name']
        page_description = items[0]['description']

    elif 'product' in request.args and request.args['product']!='':
        product = request.args['product']
        product_db = get('products/{0}'.format(product))
        if product_db:
            product_name = product_db['name']
        query = request.args['product']
    elif 'activity' in request.args and request.args['activity']!='':
        activity = request.args['activity']
        activity_db = get('activities/{0}'.format(activity))
        #print (activity_db)
        if activity_db:
            activity_name = activity_db['name']

    if 'location_name' in request.args:
        location_name = request.args['location_name']
    if 'latitude' in request.args:
        latitude = request.args['latitude']
    if 'longitude' in request.args:
        longitude = request.args['longitude']
    if 'place_id' in request.args:
        place_id = request.args['place_id']
        if place_id != '':
            place = get('places/{0}'.format(place_id))
            if place:
                place_full_name = place['name']
    if 'page' in request.args:
        page = request.args['page']

    if latitude!='' and longitude!='':
        here = True
    if 'product' in request.args or 'activity' in request.args:
        items = get('stores?product={0}&activity={1}&latitude={2}&longitude={3}&place_id={4}&page={5}'.format(product, activity, latitude, longitude, place_id, page))
    
    subtitle = " - {0}".format(product_name)
    if place_id != '':
        subtitle = "{0} en {1}".format(subtitle, place_full_name)

    tiptrick = get('tipstricks')
    if len(tiptrick) > 0:
        tiptrick = random.choice(tiptrick)

    return render_template('home.html',
                           msg = msg,
                           items = items,
                           latitude = latitude,
                           longitude = longitude,
                           page = page,
                           here = here,
                           subtitle = subtitle,
                           page_description = page_description,
                           location_name = location_name,
                           product = product,
                           product_name = product_name,
                           activity = activity,
                           activity_name = activity_name,
                           place_full_name = place_full_name,
                           place_id = place_id,
                           tiptrick = tiptrick)
