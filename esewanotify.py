#!/usr/bin/python

import requests
import pdb
import json
import os

loginUrl = 'https://esewa.com.np/authenticate'
flightDates = ['2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05']
MAXPRICE = 5900
prefixUrl = 'https://esewa.com.np/api/web/auth/airlines/availabilities?airline_code=&destination=DHI'
suffixUrl = '&no_of_adult=1&no_of_child=0&origin=KTM&return_date=2018-10-30&trip_type=O'


headers = { 'Content-Type': 'application/json;charset=UTF-8', 'esewa_id': '******','password': '******'}
session = requests.Session()
resp = session.post(loginUrl, headers=headers)

def formatFlightDetails(flight_details, flight_date):
    for flight_detail in flight_details:
        flight_detail_formatted = {}
        adult_fare = float(flight_detail['adult_fare'])
        fuel_surcharge = float(flight_detail['fuel_surcharge'])
        cashback  = float(flight_detail['cashback'])
        tax  = float(flight_detail['tax'])
        flight_name = flight_detail['display_name']
        totalPrice = adult_fare + fuel_surcharge + tax
        if totalPrice>MAXPRICE:
            continue

        message  = "Price is " + str(totalPrice) + " in " + flight_name + ' on ' + flight_date 
        cmd = "DISPLAY=:0.0 /usr/bin/notify-send --urgency=low '{0}'".format(message)
        os.system(cmd)
        flight_detail_formatted[flight_name]= totalPrice
        print (flight_detail_formatted)
    return 0

for date in flightDates:
    print 'Date: ' + date
    airlinesUrl = prefixUrl + '&flight_date=' + date + suffixUrl
    airlinesResp = session.get(airlinesUrl)
    json_data = airlinesResp.json()
    formatFlightDetails(json_data['outbound_flight_details'], date)
    print '\n'