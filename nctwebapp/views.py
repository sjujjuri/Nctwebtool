from django.shortcuts import render,HttpResponseRedirect
#import csv
import json
#from collections import namedtuple, OrderedDict
#import operator
#import copy
import os
import pandas as pd
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import numpy as np


# Create your views here.

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
con = sqlite3.connect('db.sqlite3')
df = pd.read_sql_query("select * from NCT201519", con)

def index(request):
    #makes = list(data_dict_rates.keys())
    makes=list(df['VehicleMake'].drop_duplicates().values)
    return render(request,'index.html',{'make' : makes})

@csrf_exempt
def getModel(request):
    #con = sqlite3.connect('db.sqlite3')
    #df = pd.read_sql_query("select * from NCT201519", con)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        make=body['make']
        #models = list(data_dict_rates[make].keys())
        models=list(df[(df['VehicleMake'] == make)]['VehicleModel'].drop_duplicates().values)
        models = json.dumps(models)
        print(models)
    return HttpResponse(models)


@csrf_exempt
def get_year(request):
    #con = sqlite3.connect('db.sqlite3')
    #df = pd.read_sql_query("select * from NCT201519", con)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        make=body['make']
        model=body['model']
        #years = list(data_dict_rates[make][model].keys())
        if model.isdigit():
            model = int(model)

        years=list(df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)]['YearOfBirth'].drop_duplicates().values)
        years = json.dumps(years,cls=NpEncoder)
        print(years)
    return HttpResponse(years)


def pass_faults_vechicles(request):
    try:
     if request.POST['make'] == 'make' or request.POST['model'] == "model":
            error = 'You did not select any car model. Please select a car model to proceed.'
            return render(request, "error.html", {"error":error})
    except:
        return HttpResponseRedirect('/')
    #df = pd.read_excel('NCT2015-19.xlsx')
    con = sqlite3.connect('db.sqlite3')
    df = pd.read_sql_query("select * from NCT201519", con)
    df=df.fillna(0)
    #df=df.replace('nan',0)

    if request.POST['submit-button'] == 'Display Top Faults':
        make = request.POST['make']
        model = request.POST['model']
        if model.isdigit():
             model=int(model)
        year = request.POST['year']

        if request.POST['year'] != "choose year":
            perslist = (s for s in list(df.columns) if '%' in s)
            labels = []
            values = []
            for s in perslist:
                values.append(
                    df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model) & (
                        df['YearOfBirth'] == int(year))][
                        s].mean())
                labels.append(s)
            results = zip(labels[2:], values[2:])
            res = dict(results)
            return render(request, 'failsrateyear.html',{ "results":res, "make": make, "model": model, "year": year, "total": values[1]})
        else:
            perslist = (s for s in list(df.columns) if '%' in s)
            labels = []
            values = []
            for s in perslist:
                values.append(df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)][s].mean())
                labels.append(s)
                results = zip(labels[2:], values[2:])
                res=dict(results)
            return render(request, 'failsrate.html', {"results": res, "make": make, "model": model, "total": values[1]})

    else:
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        # model = body['model']
        total = df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)]['Total'].sum()/5
        #avgPassRate = df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)]['PASS%'].mean().round(2).astype(int)
        avgPassRate = df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)]['PASS%'].mean()
        TotalPassCount = df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model)]['PASS'].sum()/5
        if request.POST['year'] != "choose year":
            total = \
                df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model) & (df['YearOfBirth'] == int(year))][
                    'Total'].sum()
            avgPassRate = \
                df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model) & (
                    df['YearOfBirth'] == int(year))][
                    'PASS%'].mean()
            TotalPassCount = \
                df[(df['VehicleMake'] == make) & (df['VehicleModel'] == model) & (
                    df['YearOfBirth'] == int(year))][
                    'PASS'].sum()
            return render(request, "passrateyear.html",
                          {"make": make, "model": model, "year": year, "count_pass": TotalPassCount,
                           "Total": total, "rate": avgPassRate})
        else:
            return render(request, "passrate.html",
                          {"make": make, "model": model, "count_pass": TotalPassCount, "total": total,
                           "results": avgPassRate})

def  about(request):
    return  render(request,'about.html')






