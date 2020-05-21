from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import razorpay
client = razorpay.Client(auth=("Key_ID", "SECRET_KEY"))


def testing(request):

    return render(request, 'order.html', {})


def create_order(request):

    context = {}
    if request.method == 'POST':
        print("INSIDE Create Order!!!")
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        product = request.POST.get('product')


        order_amount = 0
        if product == 'p1':
            order_amount = 1000
        elif product == 'p2':
            order_amount = 2000
        elif product == 'p3':
            order_amount = 5000
        elif product == 'p4':
            order_amount = 10000

        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}

        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        if order_status=='created':

            # Server data for user convinience
            context['product_id'] = product
            context['price'] = order_amount
            context['name'] = name
            context['phone'] = phone
            context['email'] = email

            # data that'll be send to the razorpay for
            context['order_id'] = order_id


            return render(request, 'confirm_order.html', context)


        # print('\n\n\nresponse: ',response, type(response))
    return HttpResponse('<h1>Error in  create order function</h1>')


@csrf_exempt
def payment_status(request):

    response = request.POST

    context = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    return render(request, 'order_summary.html', context)

