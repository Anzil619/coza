
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from userprofile.models import Address
from order.models import Order, OrderItem
from dashboard.forms import ProductForm
from store.models import Product, Variation
from category.models import Category,Sub_Category
from django.db.models.functions import TruncDay,Cast
from order.models import Coupon, UserCoupon
from django.db.models import Sum,DateField
from accounts.models import CustomUser

# Create your views here.
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_superuser:
            request.session['email'] = email
            auth.login(request, user)
            print('admin logged in ')
            messages.success(request, 'successfully signed up!')
            return redirect('dashboard')
        else:
            print('Not autherised')
            messages.error(request, 'Not autherised')
            return redirect('adminlogin')
        
    return render(request, 'dashboard/adminlogin.html')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='adminlogin')
# Create your views here.
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    delivered_items = OrderItem.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price

    top_selling = OrderItem.objects.annotate(total_quantity= Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    # orders = Order.objects.filter(created_at_gte=four_days_ago, created_at_lte=today)
    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)
    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    print(sales_by_day,"daxii")
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':CustomUser.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'dashboard/admin_home.html',context)



def users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render (request,'dashboard/users.html',context)


def blockuser(request,id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request,'user successfully blocked')
    else:
        user.is_active = True
        user.save()
        messages.success(request,'user successfully unblocked')
    return redirect('users')



def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')


def product_list(request):
    if 'email' in request.session:
        products = Product.objects.all()
        categories = Category.objects.all()
        sub_categories = Sub_Category.objects.all()

        
        context = {
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        return render(request, 'dashboard/product_list.html',context)
    else:
        return redirect('adminlogin')


def product_delete(request, id):
    products = Product.objects.filter(id=id)
    products.delete()
    return redirect('product_list')


def add_product(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    context = {
            'category' : categories,
            'sub_category' : sub_categories,
        }
    if request.method == "POST":
        product_name = request.POST['product_name']
        stock = request.POST['stock']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES.get('image', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3',None)
        category = request.POST.get('category')
        print(category,'sifan')
        sub_category = request.POST.get('sub_category')

        # validation product already exist

        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product name already exist')
            return redirect('product_list')
        

        if product_name == '':
            messages.error(request,"name field are empty")
            return redirect('product_list')
        

        try:
            check_number = int(price)
            check_number = int(stock)
        except:
            messages.info(request,'number field got unexpected values')
            return redirect('product_list')
        
        #validation for product price and stock less than zero

        check_pos =[int(price),int(stock)]
        for value in check_pos:
            if value < 0 or value == '':
                messages.info(request,'price and quantity should be positive number')
                return redirect('product_list')
            else:
                pass

        if image or image1 or image2 or image3 == None:
            messages.error(request, 'image field is empty')
            return redirect('product_list')

       


        try:
            cat = Category.objects.get(category_name=category)
        except Category.DoesNotExist:
    # Handle the case when the category does not exist
            messages.error(request, 'Invalid category')
            return redirect('product_list')

        try:
           sub_cate = Sub_Category.objects.get(sub_category_name=sub_category)
        except Sub_Category.DoesNotExist:
    # Handle the case when the sub-category does not exist
            messages.error(request, 'Invalid sub-category')
            return redirect('product_list')
        


        new = Product.objects.create(
                product_name=product_name,
                stock=stock,
                price=price,
                images=image,
                image1=image1,
                image2=image2,
                image3=image3,
                category=cat,
                sub_category=sub_cate,
                description=description
        )

        
        new.is_available=True
        new.save()

        return redirect('product_list')
    

    return render(request, 'dashboard/product_list.html',context)

    



def product_edit(request, product_id):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product_name = request.POST.get('product_name')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')

        if Product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('add_product')

        if not (product_name and price):
            messages.error(request, "Name or price field is empty")
            return redirect('product_list')

        cat = get_object_or_404(Category, category_name=category)
        sub_cate = get_object_or_404(Sub_Category, sub_category_name=sub_category)

        product.product_name = product_name
        product.stock = stock
        product.price = price
        product.description = description
        product.category = cat
        product.sub_category = sub_cate
        product.is_available = True

        
        if image:
            product.images = image
        
        if image1:
            product.image1 = image1
        if image2:
            product.image2 = image2
        if image3:
            product.image3 = image3

        product.save()

        return redirect('product_list')

    context = {
        'category': categories,
        'sub_category': sub_categories,
        'product': product,
    }
    return render(request, 'dashboard/product_list.html', context)




def category_list(request):
    category = Category.objects.all()
    context={
        'category' : category
    }

    return render(request, 'dashboard/category_list.html',context)


def add_category(request):
    if request.method == "POST":
        category_name = request.POST['category_name']
        description = request.POST['description']
        
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category name already exist')
            return redirect('category_list')
        

        if category_name == '':
            messages.error(request,"name or slug field are empty")
            return redirect('category_list')
        
        

        new = Category.objects.create(
                category_name=category_name,
        
                description=description
        )

        new.save()

        return redirect('category_list')
    

    return render(request, 'dashboard/category_list.html')


def category_delete(request, category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')

def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        
        
        description = request.POST.get('description')
        
        print(category_name)

        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('add_product')

        
        category.category_name = category_name
        category.description = description
        category.save()

        return redirect('category_list')

    
    return render(request, 'dashboard/category_list.html')
    
    
def sub_category_list(request):
    sub = Sub_Category.objects.all()
    cat = Category.objects.all()
    context = {

        'sub_category' : sub,
        'category' : cat,

    }
    return render(request, 'dashboard/sub_category_list.html',context)


def add_sub_category(request):
    if request.method == "POST":
        sub_category_name = request.POST['sub_category_name']
        category_name = request.POST['category']

        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exists():
            messages.error(request, 'Sub Category name already exist')
            return redirect('sub_category_list')
        

        if sub_category_name == '':
            messages.error(request,"name field are empty")
            return redirect('sub_category_list')
        
        

        category = Category.objects.get(category_name=category_name)
        
        new = Sub_Category.objects.create(
                sub_category_name=sub_category_name,
        
                category=category
        )

        new.save()

        return redirect('sub_category_list')
    

    return render(request, 'dashboard/sub_category_list.html')


def sub_category_delete(request,sub_id):
    sub= Sub_Category.objects.get(id=sub_id)
    sub.delete()
    return redirect('sub_category_list')

def sub_category_edit(request,sub_id):
    sub_category = Sub_Category.objects.get(id=sub_id)

    if request.method == "POST":
        sub_category_name = request.POST.get('sub_category_name')
        
        
        category_name = request.POST.get('category')
        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=sub_id).exists():
            messages.error(request, 'sub category name already exists')
            return redirect('sub_category_list')

        # if not (category_name):
        #     messages.error(request, "Name  field is empty")
        #     return redirect('product_list')
        

        category = Category.objects.get(category_name=category_name)
        
        sub_category.sub_category_name = sub_category_name
        sub_category.category = category
        
        
        sub_category.save()

        return redirect('sub_category_list')

    
    return render(request, 'dashboard/sub_category_list.html')


def order_management(request):
    order_items = OrderItem.objects.all()
    order = Order.objects.all()


    context = {
        'orders' : order,
    }

    return render(request, 'dashboard/admin_order_list.html',context)

def admin_single_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('order_management')
    address_id=order.address.id
    address = Address.objects.get(id=address_id)
    print(address,"aami")
    order_items = OrderItem.objects.filter(order_id=id)
    print(order_items,"aami")

    context ={
        'order_item' : order_items,
        'address'    : address,
        'order'   : order,
    }

    return render (request, 'dashboard/single_order_admin.html', context)


def update_order(request, id):
  if request.method == "POST":
    order_item = get_object_or_404(OrderItem, id=id)
    status = request.POST.get('status')
    order_item.status = status 
    order_item.save()
    
    return redirect('admin_single_order',id)

    

def coupon_management(request):
    coupon = Coupon.objects.all()

    context = {
        'coupon' : coupon
    }
    return render(request, 'dashboard/admin_coupon.html',context)


def add_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')



        if is_available == None:
            is_available = False




        Coupon.objects.create(
            code=coupon_code,
            discount=discount,
            min_value=min_value,
            valid_till=valid_till,
            active = is_available,
        )

        return redirect('coupon_management')
def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')

        if is_available == None:
            is_available = False

        coupon.code = coupon_code
        coupon.discount = discount
        coupon.min_value = min_value
        coupon.valid_till = valid_till
        coupon.active = is_available
        coupon.save()

        return redirect('coupon_management')
    
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('coupon_management')
    
def variants(request):
    variant = Variation.objects.all()
    product = Product.objects.all()
    variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),)   
    


    context = {
        'variants' : variant,
        'products' : product,
        'choices' : variation_category_choice,

    }
    return render(request, 'dashboard/variation.html', context)

def add_variants(request):
    if request.method == "POST":
        product_name = request.POST.get('product')
        variation_category = request.POST.get('variation_category')
        variation_value = request.POST.get('variation_value')
        is_available = request.POST.get('is_available')
        print(variation_value,"daxo")
        product = Product.objects.get(product_name=product_name)
        if is_available == None:
            is_available = False

        Variation.objects.create(product=product, variation_category=variation_category,variation_value=variation_value,is_active=is_available)


        return redirect('variants')
    
def edit_variants(request,id):
    pass
