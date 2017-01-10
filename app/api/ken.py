from flask import Flask, jsonify
from kenessa import Province
from kenessa import District
from app import *


@app.route('/api/v1/kenessa/province/province/<value>')
def province(value):
    province = Province(value).province()
    return jsonify(province)

@app.route('/api/v1/kenessa/province/district/<value>')
def district(value):
    district = Province(value).district()
    return jsonify(district)

@app.route('/api/v1/kenessa/province/sector/<value>')
def sector(value):
    sector = Province(value).sector()
    return jsonify(sector)

@app.route('/api/v1/kenessa/district/district/<value>')
def dist(value):
    district = District(value).district()
    return jsonify(district)

@app.route('/api/v1/kenessa/district/sector/<value>')
def sect(value):
    sector = District(value).sector()
    return jsonify(sector)
