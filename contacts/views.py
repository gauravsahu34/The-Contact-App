from django.shortcuts import render,redirect
import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from twilio.rest import Client
from contactsite import settings
from random import randint
from .models import Message
from django.utils import timezone
from django.contrib import messages
# Create your views here.

text_message = 'Hi, Your Otp is:'
def about(request):
    return render(request, 'about.html', {})

#This view is for rendering the list of all the contacts that we retrieve from static json file
def contact_list(request):
    #contact_list will be a list object that will contain the dictionary of contacts
    with open('contacts/contact_data.json', 'r') as f:
        contact_list = json.load(f) #json.load takes a json object and coverts it into python dictionary
    return render(request, 'contact_list.html', {'contacts':contact_list})

#This view if for rendering the detail of a contact whose id will be passed to the view
def contact_detail(request, id):
    with open('contacts/contact_data.json', 'r') as f:
        contact_list = json.load(f)
    #checking in the list of contacts for the contact that we have to show details for
    for contact in contact_list:
        if (contact['id'] == id):
            return render(request, 'contact_detail.html', {'contact':contact})
    return render(request, 'contact_detail.html', {})

#This view will be called when we click on send button provided on the contact profile page
#The id here is the id of the contact we want to send message to
def send_message(request, id):
    with open('contacts/contact_data.json', 'r') as f:
        contact_list = json.load(f)
    for contact in contact_list:
        if (contact['id'] == id):
            # we will get a rendom 6 digit number that we will used for OTP
            otp = generate_random_otp()
            #This will create a Message object with the generated OTP but the flag sent will be false for this message object
            #because we haven't sent this message to the recepient yet.
            message = Message.objects.create(OTP=otp, text=text_message,
                contact_id=id, sent=False, name = contact['Name']['first_name'] +" "+ contact['Name']['last_name']
            )
            context = {
                'message': message
            }
            # render the template with this message object asking user to send the message
            return render(request, 'send_message.html', context)
    return render(request, 'send_meassage.html', {})

#This view wiil be called when user clicks the send on the message to be sent to a particular contact
def send_otp(request, id):
    #we will get the message object
    sent_message = Message.objects.get(pk=id)
    #cid is the contact id of a contact to whom message is to be sent
    cid = sent_message.contact_id
    #a send function will be called with the OTP associated with a message object
    message = send(cid, sent_message.OTP)
    #Check Weather the message has bee sucessfully sent or not
    if (message.status == "failed"):
        messages.error(request, "Message is not sent successfully!")
        return redirect(reverse('contacts:messages_list'))
    #we will now turn the sent flag for that sent_message to be true
    messages.success(request,"The message has been sent successfully!")
    sent_message.sms_time = timezone.now()
    sent_message.sent = True
    sent_message.save()
    return redirect(reverse('contacts:messages_list'))

#This view will be responsible to render all the sent messages with descending sent time
def messages_list(request):
    messages = Message.objects.all().filter(sent=True).order_by('-sms_time')
    return render(request, 'sent_messages.html', {'sent_messages':messages})

#This function will send the message to the contact
def send(id, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    with open('contacts/contact_data.json', 'r') as f:
        contact_list = json.load(f)
    for contact in contact_list:
        if (contact['id'] == id):
            message = client.messages \
                .create(
                     body=text_message + " " + str(otp),
                     from_=settings.TWILIO_PHONE_NUMBER,
                     to=contact['Phone_number']
                 )
            message_dict = client.messages(message.sid).fetch()
            return message_dict

#It is used to gerate a 6 digit random otp
def generate_random_otp():
    range_start = 100000
    range_end = 999999
    return randint(range_start, range_end)
