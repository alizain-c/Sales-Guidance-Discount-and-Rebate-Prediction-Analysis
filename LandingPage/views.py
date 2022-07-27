from django.shortcuts import render
from django.http import HttpResponse
import joblib
import pandas as pd
import os
from PIL import Image

# Create your views here.

load_model = joblib.load('./models/RFModelForDiscount.pkl')

load_model_rebate = joblib.load('./models/RFModelForRebate.pkl')

def index(request):
    context = {'a' : ''}
    return render(request, 'index.html',context)
    # return HttpResponse({'a':1})

def predictRebateRevenue(request):
    if request.method == 'POST':
        my_dict = {}
        my_dict['QUANTITY'] = request.POST.get('quantityVal')
        my_dict['FINAL_REVENUE'] = request.POST.get('desired_revVal')
        my_dict['LIST_PRICE'] = request.POST.get('list_priceVal')

        if float(my_dict['QUANTITY']) < 146: 
            my_dict['QUANTITY'] = str(float(my_dict['QUANTITY'])/164.7100000)
            my_dict['FINAL_REVENUE'] = str(float(my_dict['FINAL_REVENUE'])/89053.367700)
            my_dict['LIST_PRICE'] = str(float(my_dict['LIST_PRICE'])/609.236433)
        else: 
            my_dict['QUANTITY'] = str(float(my_dict['QUANTITY'])/168.000000)
            my_dict['FINAL_REVENUE'] = str(float(my_dict['FINAL_REVENUE'])/92302.166490)
            my_dict['LIST_PRICE'] = str(float(my_dict['LIST_PRICE'])/608.499513)

    testData_discount = pd.DataFrame({'x':my_dict}).transpose()
    testData_rebate = pd.DataFrame({'x2': my_dict}).transpose()

    scored_value_d = load_model.predict(testData_discount)[0]
    scored_value_r = load_model_rebate.predict(testData_rebate)[0]
    print("SCORED Discount:" ,scored_value_d)
    print("SCORED Rebate:" ,scored_value_r)

    # Figure:
    #image = os.listdir('./media')
    image = Image.open('./media/Figure.png')
    image 

    # context = ({'s_v': scored_value})
    return render(request, 'index.html', {'s_v': scored_value_d, 's_v_r': scored_value_r, 'image': image})