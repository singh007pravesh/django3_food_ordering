import uuid 
#from var_dump import var_dump
from django.shortcuts import redirect,render
from django.http import HttpResponse

def categories_processor(request):
    
    message=""
    if 'adyty879aaa' not in request.session:
        cart=[]
        s_id=uuid.uuid4().hex[:10].upper()
        request.session['adyty879aaa']=cart
        request.session['s_id']=s_id
    else:
        cart=request.session['adyty879aaa']
        s_id=request.session['s_id']

    if request.method=='POST':
        if request.POST.get('pro_id')!=None:
            prod_id=request.POST['pro_id']
            cart.append(prod_id)
            request.session['adyty879aaa']=cart
            message="reload"

        if request.POST.get('remove_pro_id')!=None:
            remove_pro_id=request.POST['remove_pro_id']
            for cc in cart:
                if cc==remove_pro_id:
                    cart.remove(remove_pro_id)
            request.session['adyty879aaa']=cart
            # render(request,"<script>alert(1)</script>")
            # HttpResponse("<script>alert(1)</script>")
            message="reload"


        # if request.POST.get('check_out')!=None:
        #     print(request.POST.get('check_out'))


    cart=request.session['adyty879aaa']
    myset = set(cart)
    cart=list(myset)
    # print(cart)
    len_cart=len(cart)

    return {
            'len_cart':len_cart,
            'cart':cart,
            'message':message,
            's_id':s_id,
            }
