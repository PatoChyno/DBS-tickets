from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django import forms
from tickets import db_interface
from tickets.models import BuyTicketForm, UpdatePricesForm, DeleteEventForm

def index(request):
    response = {}
    return render(request, 'index.html', response)

def render_delete_event(request):
    events = db_interface.get_all_events()
    if request.method == 'POST':
        form = DeleteEventForm(request.POST)
        if form.is_valid():
            events = submit_delete_event(form.cleaned_data)
        else:
            print("nooooot")

    return render(request, 'delete.html', {"events": events})

def submit_delete_event(data):
    kwargs = {
            "event": data['event'],
    }
    events = db_interface.delete_event(**kwargs)
    return events

def render_stats(request):
    response = {}
    return render(request, 'stats.html', response)

def submit_buy_tickets(data):
    kwargs = {
            "name": data['name'], 
            "birthday": data['birthday'],
            "gender": data['gender'],
            "phone": data['phone'],
            "event": data['event'],
            "adult": data['adults'],
            "student": data['students'],
            "child": data['children']
    }
    tickets = db_interface.buy_ticket(**kwargs)
    return tickets

def submit_update_prices(data):
    kwargs = {
            "event": data['event'],
            "adult": data['adults'],
            "student": data['students'],
            "child": data['children']
    }
    return db_interface.update_prices(**kwargs)

def buy_ticket(request):
    events = db_interface.get_all_events()
    if request.method == 'POST':
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            tickets = submit_buy_tickets(form.cleaned_data)
            return render(request, 'bought.html', {"tickets": tickets})

    return render_to_response( 'buy.html', {'events' : events}, context_instance=RequestContext(request))

def update_prices(request):
    events = db_interface.get_all_date_events()
    prices = db_interface.get_prices()
    if request.method == 'POST':
        form = UpdatePricesForm(request.POST)
        if form.is_valid():
            prices = submit_update_prices(form.cleaned_data)

    return render(request, 'update.html', {'events' : events, 'prices': prices})
