from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Coffee
from .serializers import CoffeeSerializer


@csrf_exempt
def success_view(request):
    return render(request, "order/success.html")

def order_view(request):
    if request.method == "GET":
        return render(request, 'order/order.html')
    
    if request.method == "POST":
        name = request.POST.get('name')
        currency = request.POST.get('currency')
        email_id = request.POST.get('email_id')
        mobile_number = request.POST.get('mobile_number')
        amount = int(request.POST.get('amount')) * 100

        client = razorpay.Client(auth =("rzp_test_B26WoI87939lmO" , "OKbtZsWWUs1SO6BnOHtCwzpK"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1' })
        
        coffee = Coffee(name=name, currency=currency, email_id=email_id, mobile_number=mobile_number, amount=amount, order_id= payment['id'], paid=True)
        coffee.save()
        
        return render(request, 'order/order.html' ,{'payment':payment})

@api_view(('GET','POST'))
def order_api_view(request):
    if request.method == "GET":
        return Response({'response':"POST request accept create order"})
    
    if request.method == "POST":
        data = {}
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():

            amount = int(request.POST.get('amount')) * 100

            client = razorpay.Client(auth =("rzp_test_B26WoI87939lmO" , "OKbtZsWWUs1SO6BnOHtCwzpK"))
            payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1' })
            
            order = serializer.save(amount=amount, order_id= payment['id'], paid=True)
            data['name'] = order.name
            data['amount'] = order.amount
            data['order_id'] = order.order_id
            data['razorpay_payment_id'] = order.razorpay_payment_id
            data['currency'] = order.currency
            data['email_id'] = order.email_id
            data['mobile_number'] = order.mobile_number
            data['paid'] = order.paid
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
