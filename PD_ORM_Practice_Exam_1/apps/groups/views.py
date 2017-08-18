# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.messages import error
from .models import *

def index(request):

    try:
        request.session['name']
    except:
        request.session['name'] = ""
        
    try:
        request.session['age']
    except:
        request.session['age'] = 0
        
    return render(request, "groups/index.html")

def login(request):
    
    result = User.objects.validate(request.POST)
    
    if type(result) == dict:
        for field, message in result.iteritems():
            error(request, message, extra_tags=field)
        
        return redirect('/')
    
    request.session['name'] = result.name
    request.session['age'] = int(result.age)
    return redirect("/groups/age_groups")

def age_groups(request):

    context = {
        'groups': User.objects.get_age_group_count()
    }
    
    return render(request, "groups/age_groups.html", context)

def group_members(request, age_range):
    ages = age_range.split("-")
    min = int(ages[0])
    max = int(ages[1])

    age_range_display = age_range
    
    if max == 0:
        age_range_display = "51+"
    
    print "min: {}".format(min)
    print "max: {}".format(max)
    print "request.session['name']: {}".format(request.session['name'])
    print "request.session['age']: {}".format(request.session['age'])
    context = {
        'age_range_display': age_range_display,
        'age_range': age_range,
        'users' : User.objects.get_group_members(min, max),
        'comments': Comment.objects.get_group_comments(min, max),
        'min': min,
        'max': max,
    }
    
    return render(request, "groups/group_members.html", context)
    
    
def add_comment(request, age_range):
    ages = age_range.split("-")
    min = int(ages[0])
    max = int(ages[1])

    age_range_display = age_range
    
    if max == 0:
        age_range_display = "51+"
    
    
    context = {
        'age_range_display': age_range_display,
        'age_range': age_range,
        'users' : User.objects.get_group_members(min, max)
    }
    return render(request, "groups/add_comment.html", context)

def save_comment(request, age_range):
    
    result = Comment.objects.validate(request.POST, request.session['name'], request.session['age'])
    
    if type(result) == dict:
        for field, message in result.iteritems():
            error(request, message, extra_tags=field)
    
            return redirect("/groups/add_comment/{}".format(age_range))
    
    return redirect("/groups/group_members/{}".format(age_range))

def logout(request):
    request.session.flush()
    return redirect('/')