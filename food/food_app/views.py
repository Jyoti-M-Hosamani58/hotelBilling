from django.shortcuts import render,redirect,get_object_or_404
from django.utils.dateparse import parse_date
from food_app.models import UserLogin,UserReg,AddTable,AddItem,AddCompany,ItemOrder,Orders,Pracel,Printorders, Expenses,Salary
from django.urls import reverse

import json
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from datetime import datetime



# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_nav(request):
    return render(request,'admin_nav.html')



def admin_home(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # List of stored table names
    return render(request, 'admin_home.html', {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})
def userHome(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # Example: list of stored table names

    return render(request, 'userHome.html', {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})

def register(request):
    if request.method=="POST":
        email=request.POST.get('t1')
        number= request.POST.get('t2')
        password = request.POST.get('t3')
        username = request.POST.get('t4')
        utype=request.POST.get('utype')
        ucount=UserReg.objects.filter(email=email).count()
        if ucount>=1:
            return render(request,'register.html',{'msg':'This is already exists'})
        else:
            UserReg.objects.create(email=email,number=number,password=password,usertype=utype,username=username)
            UserLogin.objects.create(utype=utype, username=email, password=password)
            return render(request,'register.html',{'msg':'Thank you for registration'})
    return render(request,'register.html')

def register_list(request):
    userdata=UserReg.objects.all()
    return render(request,'register_list.html',{'userdata':userdata})

def delete_register(request,pk):
    udata = UserReg.objects.get(id=pk)

    udata.delete()
    base_url = reverse('register_list')
    return redirect(base_url)

def login(request):
    if request.method == "POST":
        username = request.POST.get('t1')
        password = request.POST.get('t2')
        request.session['username'] = username
        ucount = UserLogin.objects.filter(username=username).count()
        if ucount >= 1:
            udata = UserLogin.objects.get(username=username)
            upass = udata.password
            utype = udata.utype
            if password == upass:
                if utype == 'staff':
                    return redirect('userHome')
                if utype == 'admin':
                    return redirect('admin_home')
            else:
                return render(request, 'login.html', {'msg': 'Invalid Password'})
        else:
            return render(request, 'login.html', {'msg': 'Invalid Username'})
    return render(request, 'login.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('t1')
        password = request.POST.get('t2')
        request.session['username'] = username
        ucount = UserLogin.objects.filter(username=username).count()
        if ucount >= 1:
            udata = UserLogin.objects.get(username=username)
            upass = udata.password
            utype = udata.utype
            if password == upass:
                if utype == 'admin':
                    return redirect('admin_home')
                else:
                    return render(request, 'admin_login.html', {'msg': 'Invalid Login Type'})
            else:
                return render(request, 'admin_login.html', {'msg': 'Invalid Password'})
        else:
            return render(request, 'admin_login.html', {'msg': 'Invalid Username'})
    return render(request, 'admin_login.html')
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('t1')
        password = request.POST.get('t2')
        request.session['username'] = username
        ucount = UserLogin.objects.filter(username=username).count()
        if ucount >= 1:
            udata = UserLogin.objects.get(username=username)
            upass = udata.password
            utype = udata.utype
            if password == upass:
                if utype == 'user':
                    return redirect('userHome')
                else:
                    return render(request, 'user_login.html', {'msg': 'Invalid Login Type'})
            else:
                return render(request, 'user_login.html', {'msg': 'Invalid Password'})
        else:
            return render(request, 'user_login.html', {'msg': 'Invalid Username'})
    return render(request, 'user_login.html')


def add_item(request):
    if request.method == "POST":
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        item_gst = request.POST.get('t3')
        item_price = request.POST.get('t4')
        cat = request.POST.get('t5')

        # Generate a numeric unique identifier for the barcode (though not used for barcode generation anymore)

        # Create the item entry in the database without barcode information
        item = AddItem.objects.create(
            Item_code=item_code,
            Item_name=item_name,
            Item_GST=item_gst,
            Item_price=item_price,
            Category=cat,
        )

        # Instead of generating and saving the barcode, just return a success message
        return render(request, 'add_item.html', {'msg': 'Item added successfully!'})

    return render(request, 'add_item.html')

def view_item(request):
    userdata=AddItem.objects.all()
    return render(request,'view_item.html',{'userdata':userdata})

def delete_item(request,pk):
    udata = AddItem.objects.get(id=pk)
    udata.delete()
    base_url = reverse('view_item')
    return redirect(base_url)

def edit_item(request, pk):
    rdata = get_object_or_404(AddItem, id=pk)
    if request.method == "POST":
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        item_gst = request.POST.get('t3')
        item_price = request.POST.get('t4')
        cat = request.POST.get('t5')
        AddItem.objects.filter(id=pk).update(
            Item_code=item_code,
            Item_name=item_name,
            Item_GST=item_gst,
            Item_price=item_price,
            Category=cat
        )
        base_url = reverse('view_item')
        return redirect(base_url)
    return render(request, 'edit_item.html', {'rdata': rdata})


def add_table(request):
    if request.method=="POST":
        table_name=request.POST.get('t1')
        cat=request.POST.get('t2')
        AddTable.objects.create(Table_name=table_name,Category=cat)
        return render(request, 'add_table.html', {'msg': 'Added'})
    return render(request, 'add_table.html')

def view_table(request):
    udata=AddTable.objects.all()
    return render(request,'view_table.html',{'udata':udata})

def delete_table(request, pk):
    udata = AddTable.objects.get(id=pk)
    udata.delete()
    base_url = reverse('view_table')
    return redirect(base_url)

def edit_table(request, pk):
    rdata = get_object_or_404(AddTable, id=pk)
    if request.method == "POST":
        table_name = request.POST.get('t1')
        cat = request.POST.get('t2')
        AddTable.objects.filter(id=pk).update(
            Table_name=table_name,
            Category=cat
        )
        base_url = reverse('view_table')
        return redirect(base_url)
    return render(request, 'edit_table.html', {'rdata': rdata})

def add_company(request):
    if request.method=="POST":
        company_name=request.POST.get('t1')
        company_addres=request.POST.get('t2')
        company_gst=request.POST.get('t3')
        company_number=request.POST.get('t4')
        AddCompany.objects.create(Company_name=company_name,Company_address=company_addres,Company_GST=company_gst,Company_number=company_number)
        return render(request, 'add_company.html', {'msg': 'Added'})
    return render(request,'add_company.html')

def view_company(request):
    udata=AddCompany.objects.all()
    return render(request, 'view_company.html',{'udata':udata})

def edit_company(request,pk):
    udata=AddCompany.objects.get(id=pk)
    if request.method=="POST":
        company_name=request.POST.get('t1')
        company_address=request.POST.get('t2')
        company_gst=request.POST.get('t3')
        company_number=request.POST.get('t4')
        udata=AddCompany.objects.filter(id=pk).update(
            Company_name=company_name,
            Company_address=company_address,
            Company_GST=company_gst,
            Company_number=company_number
        )
        base_url = reverse('view_company')
        return redirect(base_url)
    return render(request,'edit_company.html',{'udata':udata})

def delete_company(request,pk):
    udata=AddCompany.objects.get(id=pk)
    udata.delete()
    base_url = reverse('view_company')
    return redirect(base_url)


def add_order(request):
    if request.method == 'GET':
        table_name = request.GET.get('table', '')  # Fetch the table name from the URL parameter

        # Get the last order's bill number (if exists) and generate the next one
        last_order = Orders.objects.order_by('-bill_no').first()
        if last_order:
            bill_no = int(last_order.bill_no) + 1
        else:
            bill_no = 1000

        # Render the add bill form with the table name and generated bill number
        context = {
            'Table_name': table_name,
            'Bill_no': bill_no,
        }
        return render(request, 'add_order.html', context)

    elif request.method == 'POST':
        # Handle form submission (optional: you can process form data as needed)
        return redirect('admin_home')

def add_order_user(request):
    if request.method == 'GET':
        table_name = request.GET.get('table', '')  # Fetch the table name from the URL parameter

        # Get the last order's bill number (if exists) and generate the next one
        last_order = Orders.objects.order_by('-bill_no').first()

        if last_order:
            last_bill_no = last_order.bill_no
            bill_no = str(int(last_bill_no) + 1)
        else:
            BASE_NUMBER = 1001
            bill_no = str(BASE_NUMBER)
        # Render the add bill form with the table name and generated bill number
        context = {
            'Table_name': table_name,
            'Bill_no': bill_no,
        }
        return render(request, 'add_order_user.html', context)

    elif request.method == 'POST':
        # Handle form submission (optional: you can process form data as needed)
        return redirect('userHome')

@require_http_methods(["GET"])
def fetch_item_details(request, item_code):
    try:
        # Use `iexact` for case-insensitive matching
        item = AddItem.objects.get(Item_code__iexact=item_code)
        data = {
            'item_cat': item.Category,
            'item_name': item.Item_name,
            'price': item.Item_price,
            'gst': item.Item_GST,
        }
        return JsonResponse(data)
    except AddItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)



@require_http_methods(["POST"])
def save_order(request):
    now = datetime.now().replace(microsecond=0)
    current_time = now.strftime("%H:%M:%S")

    data = json.loads(request.body)
    bill_details = data['billDetails']
    bill_items = data['billItems']

    table_name = bill_details['table_name']
    bill_no = bill_details['bill_no']
    bill_date = bill_details['bill_date']

    for item in bill_items:
        item_code = item['item_code']
        item_cat = item['item_cat']
        item_name = item['item_name']
        price = float(item['price'])
        gst = float(item['gst'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total_gst = float(item['total_gst'])
        total = float(item['total'])

        # Create or update the item order, but allow duplicate entries (don't check if it exists)
        ItemOrder.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )

        # Create or update the corresponding record in the Orders table
        Orders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )
        Printorders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )

    return JsonResponse({'success': True, 'redirect_url': reverse('admin_home')})

@require_http_methods(["POST"])
def save_order_user(request):
    now = datetime.now().replace(microsecond=0)
    current_time = now.strftime("%H:%M:%S")

    data = json.loads(request.body)
    bill_details = data['billDetails']
    bill_items = data['billItems']

    table_name = bill_details['table_name']
    bill_no = bill_details['bill_no']
    bill_date = bill_details['bill_date']

    for item in bill_items:
        item_code = item['item_code']
        item_cat = item['item_cat']
        item_name = item['item_name']
        price = float(item['price'])
        gst = float(item['gst'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total_gst = float(item['total_gst'])
        total = float(item['total'])

        # Create or update the item order, but allow duplicate entries (don't check if it exists)
        ItemOrder.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )

        # Create or update the corresponding record in the Orders table
        Orders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )
        Printorders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,  # Correct field name
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total
        )

    return JsonResponse({'success': True, 'redirect_url': reverse('userHome')})

@require_http_methods(["GET"])
def fetch_table_data(request):
    table_name = request.GET.get('table')
    if not table_name:
        return JsonResponse({'error': 'Table name is required'})

    items = ItemOrder.objects.filter(table_name=table_name).values(
        'item_code', 'item_cat', 'item_name', 'price', 'gst', 'qty', 'tax_amt', 'total_gst', 'total', 'bill_no', 'bill_date')

    if items.exists():
        bill = items.first()
        response_data = {
            'bill_no': bill['bill_no'],
            'bill_date': bill['bill_date'],
            'items': list(items)
        }
        print("Fetched data: ", response_data)  # Debug print statement
        return JsonResponse(response_data)
    else:
        print("No items found for table: ", table_name)  # Debug print statement
        return JsonResponse({'error': 'Table data not found'})

def edit_table(request, pk):
    rdata = get_object_or_404(AddTable, id=pk)
    if request.method == "POST":
        table_name = request.POST.get('t1')
        cat = request.POST.get('t2')
        AddTable.objects.filter(id=pk).update(
            Table_name=table_name,
            Category=cat
        )
        base_url = reverse('view_table')
        return redirect(base_url)
    return render(request, 'edit_table.html', {'rdata': rdata})


def exchange_tbl(request):
    table=AddTable.objects.all()
    if request.method == "POST":
        old_table = request.POST.get('oldTable')
        new_table = request.POST.get('newTable')

        # Update only the items associated with the old table
        ItemOrder.objects.filter(table_name=old_table).update(table_name=new_table)

        base_url = reverse('admin_home')
        return redirect(base_url)

    return render(request, 'exchange_tbl.html',{'table':table})

def print_table(request):
    # Get distinct table names from ItemOrder
    tableName = Printorders.objects.values('table_name').distinct()
    return render(request, 'print_table.html', {'tableName': tableName})
# views.py

def print_bill(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

    if selected_table_name:
        # Fetch related ItemOrder objects
        item_orders = Printorders.objects.filter(table_name=selected_table_name)
        table_data = {
            'table_name': selected_table_name,
            'items': []
        }

        for item_order in item_orders:
            item_data = {
                'table_name': item_order.table_name,
                'bill_no': item_order.bill_no,
                'bill_date': item_order.bill_date,
                'bill_time': item_order.bill_time,
                'item_name': item_order.item_name,
                'qty': item_order.qty,
            }
            table_data['items'].append(item_data)

        return render(request, 'print_bill.html', {'table_data': table_data, 'company': company})
    else:
        error_message = "Please select a table name."
        return render(request, 'print_bill.html', {'error_message': error_message})

    return render(request, 'print_bill.html')

def settle_table(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table.html', {'tableName': tableName})


def settle_bill(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],
                'total_cgst': 0,  # Initialize total CGST for all items
                'total_sgst': 0,  # Initialize total SGST for all items
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                # Calculate CGST and SGST based on GST and price
                gst = item_order.gst  # Assuming gst is a percentage (e.g., 18%)
                cgst_rate = gst / 2
                sgst_rate = gst / 2

                # Calculate CGST and SGST amounts for each item
                cgst_amt = (cgst_rate / 100) * item_order.price * item_order.qty
                sgst_amt = (sgst_rate / 100) * item_order.price * item_order.qty

                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'gst': gst,
                    'cgst_rate': cgst_rate,
                    'sgst_rate': sgst_rate,
                    'cgst': cgst_amt,
                    'sgst': sgst_amt,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                # Accumulate total CGST, SGST, subtotal, and total quantity for the bill
                table_data['total_cgst'] += cgst_amt
                table_data['total_sgst'] += sgst_amt
                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.total

            # Calculate total CGST and SGST for all items combined
            total_cgst_all_items = sum(item['cgst'] for item in table_data['items'])
            total_sgst_all_items = sum(item['sgst'] for item in table_data['items'])

            # Update table_data with total CGST and SGST for all items combined
            table_data['total_cgst'] = total_cgst_all_items
            table_data['total_sgst'] = total_sgst_all_items

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'settle_bill.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'settle_bill.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'settle_bill.html')
def parcel(request):
    return render(request,'parcel.html')


@require_http_methods(["POST"])
def save_pracel_user(request):
    data = json.loads(request.body)
    bill_items = data['billItems']
    parcel_charge = float(data.get('parcelCharge', 0.0))  # Note the key should match what you use in JS

    # Get the current date
    bill_date = timezone.now().date()

    # Determine the next bill_no
    last_pracel = Pracel.objects.all().order_by('-bill_no').first()
    if last_pracel:
        bill_no = int(last_pracel.bill_no) + 1
    else:
        bill_no = 1000

    for item in bill_items:
        item_code = item['item_code']
        item_name = item['item_name']
        price = float(item['price'])
        gst = float(item['gst'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total_gst = float(item['total_gst'])
        total = float(item['total'])
        Pracel.objects.create(
            bill_no=bill_no,
            bill_date=bill_date,
            item_code=item_code,
            item_name=item_name,
            price=price,
            gst=gst,
            qty=qty,
            tax_amt=tax_amt,
            total_gst=total_gst,
            total=total,
            pracel_charge=parcel_charge  # Ensure this matches your model field
        )

    return JsonResponse({'success': True, 'bill_no': bill_no, 'redirect_url': reverse('userHome')})

from django.db.models import Sum, F,FloatField
from decimal import Decimal


def print_pracel(request, bill_no):
    # Fetch the pracels for the given bill_no
    pracels = Pracel.objects.filter(bill_no=bill_no)

    # Calculate totals and aggregates
    total_qty = pracels.aggregate(total_qty=Sum('qty'))['total_qty'] or 0
    subtotal = pracels.aggregate(subtotal=Sum('tax_amt'))['subtotal'] or 0

    # Initialize CGST and SGST totals
    total_cgst_amt = 0
    total_sgst_amt = 0

    # Calculate CGST and SGST amounts
    for pracel in pracels:
        gst_rate = pracel.gst
        price = pracel.price
        qty = pracel.qty
        tax_amt = pracel.tax_amt

        cgst_amt = (gst_rate / 2 / 100) * price * qty
        sgst_amt = (gst_rate / 2 / 100) * price * qty

        total_cgst_amt += cgst_amt
        total_sgst_amt += sgst_amt

    # Get parcel charge from the first item (assuming all items have the same parcel charge)
    parcel_charge = pracels.first().pracel_charge if pracels.exists() else 0

    # Calculate grand total
    grand_total = subtotal + total_cgst_amt + total_sgst_amt + parcel_charge

    # Fetch company details
    company = AddCompany.objects.all()

    context = {
        'pracels': pracels,
        'total_qty': total_qty,
        'subtotal': subtotal,
        'total_cgst_amt': total_cgst_amt,
        'total_sgst_amt': total_sgst_amt,
        'parcel_charge': parcel_charge,
        'grand_total': grand_total,
        'company': company
    }

    return render(request, 'print_pracel.html', context)


from collections import defaultdict


def sales_report(request):
    from collections import defaultdict
    from django.db.models import Q
    from .models import Orders  # Adjust the import based on your project structure

    selected_month = request.POST.get('salesmonth')
    sales_data = []
    total_amount = 0  # Initialize total amount

    if request.method == 'POST' and selected_month:
        # Extract year and month from the selected month
        year, month = selected_month.split('-')

        # Filter orders by year and month
        salesreport = Orders.objects.filter(
            Q(bill_date__year=year) & Q(bill_date__month=month)
        )

        # Create a dictionary to store the grouped data
        grouped_sales = defaultdict(lambda: {
            'bill_no': None,
            'bill_date': None,
            'items': [],
            'quantities': [],
            'total': 0
        })

        # Iterate through each sale and group by bill_no
        for sales in salesreport:
            bill_no = sales.bill_no
            grouped_sales[bill_no]['bill_no'] = sales.bill_no
            grouped_sales[bill_no]['bill_date'] = sales.bill_date
            grouped_sales[bill_no]['items'].append(sales.item_name)
            grouped_sales[bill_no]['quantities'].append(str(sales.qty))
            grouped_sales[bill_no]['total'] += sales.total

        # Prepare the sales data for rendering
        for key, value in grouped_sales.items():
            # Join items and quantities with commas
            items = ', '.join(value['items'])
            quantities = ', '.join(value['quantities'])
            sales_data.append({
                'bill_no': value['bill_no'],
                'bill_date': value['bill_date'],
                'items': items,
                'quantities': quantities,
                'total': value['total'],
            })
            total_amount += value['total']  # Add to total amount

    return render(
        request,
        'sales_report.html',
        {
            'sales_data': sales_data,
            'selected_month': selected_month,
            'total_amount': total_amount  # Pass total amount to the template
        }
    )


from django.db.models import Sum

def item_report(request):
    # Get distinct categories from AddItem
    category = AddItem.objects.values('Category').distinct()
    selectedmonth = None
    selectedcat = None
    total_amount = 0  # Initialize total amount
    orders = None  # Initialize orders

    if request.method == 'POST':
        selectedmonth = request.POST.get('salesmonth')
        selectedcat = request.POST.get('selectedcat')

        # Query the Orders table based on the selected month and category
        orders = Orders.objects.all()

        if selectedmonth:
            orders = orders.filter(bill_date__month=selectedmonth.split('-')[1])
        if selectedcat and selectedcat.strip() != "":
            orders = orders.filter(item_cat=selectedcat)  # Adjust the field based on your actual schema

        # Aggregate quantities and totals for the same item_name
        orders = orders.values('item_name').annotate(
            total_qty=Sum('qty'),
            total_amount=Sum('total')
        ).order_by('item_name')

        # Calculate the total amount for all items
        total_amount = orders.aggregate(grand_total=Sum('total_amount'))['grand_total'] or 0

    return render(request, 'item_report.html', {
        'category': category,
        'orders': orders if request.method == 'POST' else None,
        'selectedmonth': selectedmonth,
        'selectedcat': selectedcat,
        'total_amount': total_amount,  # Pass total amount to the template
    })


def daily_report(request):
    # Default to today's date in case no date is selected
    selected_date = datetime.now().date()

    if request.method == 'POST':
        selected_date_input = request.POST.get('date')
        if selected_date_input:
            # Convert the selected date to a datetime object for querying
            selected_date = datetime.strptime(selected_date_input, '%Y-%m-%d').date()
            orders = Orders.objects.filter(bill_date=selected_date)

            # Calculate the grand total by summing up the total field
            grand_total = orders.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        else:
            orders = Orders.objects.none()  # No data if no date is selected
            grand_total = 0

        return render(request, 'daily_report.html', {
            'selected_date': selected_date,  # Pass the selected date to the frontend
            'orders': orders,
            'grand_total': grand_total
        })

    # If it's a GET request or no date is selected, use today's date as default
    return render(request, 'daily_report.html', {
        'selected_date': selected_date  # Pass selected_date to the template
    })

def print_bill_delete(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = Printorders.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('admin_home'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('admin_home'))

def settle_bill_delete(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = ItemOrder.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('admin_home'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('admin_home'))

def settle_bill_delete_user(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = ItemOrder.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('userHome'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('userHome'))


def exchange_tbl_user(request):
    table=AddTable.objects.all()
    if request.method == "POST":
        old_table = request.POST.get('oldTable')
        new_table = request.POST.get('newTable')

        # Update only the items associated with the old table
        ItemOrder.objects.filter(table_name=old_table).update(table_name=new_table)

        base_url = reverse('userHome')
        return redirect(base_url)

    return render(request, 'exchange_tbl_user.html',{'table':table})

def print_table_user(request):
    # Get distinct table names from ItemOrder
    tableName = Printorders.objects.values('table_name').distinct()
    return render(request, 'print_table_user.html', {'tableName': tableName})
# views.py

def print_bill_user(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

    if selected_table_name:
        # Fetch related ItemOrder objects
        item_orders = Printorders.objects.filter(table_name=selected_table_name)
        table_data = {
            'table_name': selected_table_name,
            'items': []
        }

        for item_order in item_orders:
            item_data = {
                'table_name': item_order.table_name,
                'bill_no': item_order.bill_no,
                'bill_date': item_order.bill_date,
                'bill_time': item_order.bill_time,
                'item_name': item_order.item_name,
                'qty': item_order.qty,
            }
            table_data['items'].append(item_data)

        return render(request, 'print_bill_user.html', {'table_data': table_data, 'company': company})
    else:
        error_message = "Please select a table name."
        return render(request, 'print_bill_user.html', {'error_message': error_message})

    return render(request, 'print_bill_user.html')

def settle_table_user(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table_user.html', {'tableName': tableName})


def settle_bill_user(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],
                'total_cgst': 0,  # Initialize total CGST for all items
                'total_sgst': 0,  # Initialize total SGST for all items
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                # Calculate CGST and SGST based on GST and price
                gst = item_order.gst  # Assuming gst is a percentage (e.g., 18%)
                cgst_rate = gst / 2
                sgst_rate = gst / 2

                # Calculate CGST and SGST amounts for each item
                cgst_amt = (cgst_rate / 100) * item_order.price * item_order.qty
                sgst_amt = (sgst_rate / 100) * item_order.price * item_order.qty

                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'gst': gst,
                    'cgst_rate': cgst_rate,
                    'sgst_rate': sgst_rate,
                    'cgst': cgst_amt,
                    'sgst': sgst_amt,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                # Accumulate total CGST, SGST, subtotal, and total quantity for the bill
                table_data['total_cgst'] += cgst_amt
                table_data['total_sgst'] += sgst_amt
                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.total

            # Calculate total CGST and SGST for all items combined
            total_cgst_all_items = sum(item['cgst'] for item in table_data['items'])
            total_sgst_all_items = sum(item['sgst'] for item in table_data['items'])

            # Update table_data with total CGST and SGST for all items combined
            table_data['total_cgst'] = total_cgst_all_items
            table_data['total_sgst'] = total_sgst_all_items

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'settle_bill_user.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'settle_bill_user.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'settle_bill_user.html')

def checkTables(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'checkTables.html', {'tableName': tableName})


def checkItems(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],
                'total_cgst': 0,  # Initialize total CGST for all items
                'total_sgst': 0,  # Initialize total SGST for all items
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                # Calculate CGST and SGST based on GST and price
                gst = item_order.gst  # Assuming gst is a percentage (e.g., 18%)
                cgst_rate = gst / 2
                sgst_rate = gst / 2

                # Calculate CGST and SGST amounts for each item
                cgst_amt = (cgst_rate / 100) * item_order.price * item_order.qty
                sgst_amt = (sgst_rate / 100) * item_order.price * item_order.qty

                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'gst': gst,
                    'cgst_rate': cgst_rate,
                    'sgst_rate': sgst_rate,
                    'cgst': cgst_amt,
                    'sgst': sgst_amt,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                # Accumulate total CGST, SGST, subtotal, and total quantity for the bill
                table_data['total_cgst'] += cgst_amt
                table_data['total_sgst'] += sgst_amt
                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.total

            # Calculate total CGST and SGST for all items combined
            total_cgst_all_items = sum(item['cgst'] for item in table_data['items'])
            total_sgst_all_items = sum(item['sgst'] for item in table_data['items'])

            # Update table_data with total CGST and SGST for all items combined
            table_data['total_cgst'] = total_cgst_all_items
            table_data['total_sgst'] = total_sgst_all_items

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'checkItems.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'checkItems.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'checkItems.html')


def checkTablesUser(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'checkTablesUser.html', {'tableName': tableName})


def checkItemsUser(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],
                'total_cgst': 0,  # Initialize total CGST for all items
                'total_sgst': 0,  # Initialize total SGST for all items
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                # Calculate CGST and SGST based on GST and price
                gst = item_order.gst  # Assuming gst is a percentage (e.g., 18%)
                cgst_rate = gst / 2
                sgst_rate = gst / 2

                # Calculate CGST and SGST amounts for each item
                cgst_amt = (cgst_rate / 100) * item_order.price * item_order.qty
                sgst_amt = (sgst_rate / 100) * item_order.price * item_order.qty

                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'gst': gst,
                    'cgst_rate': cgst_rate,
                    'sgst_rate': sgst_rate,
                    'cgst': cgst_amt,
                    'sgst': sgst_amt,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                # Accumulate total CGST, SGST, subtotal, and total quantity for the bill
                table_data['total_cgst'] += cgst_amt
                table_data['total_sgst'] += sgst_amt
                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.total

            # Calculate total CGST and SGST for all items combined
            total_cgst_all_items = sum(item['cgst'] for item in table_data['items'])
            total_sgst_all_items = sum(item['sgst'] for item in table_data['items'])

            # Update table_data with total CGST and SGST for all items combined
            table_data['total_cgst'] = total_cgst_all_items
            table_data['total_sgst'] = total_sgst_all_items

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'checkItemsUser.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'checkItemsUser.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'checkItemsUser.html')

def index1(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # List of stored table names
    return render(request, 'index1.html',
                  {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})

def addExpenses(request):
    return render(request, 'expenses.html')


def saveExpenses(request):
    if request.method == 'POST':
        # Parse and validate date
        date_str = request.POST.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")  # Debugging statement
            return redirect('adminExpenses')
        amount = request.POST.get('amt')
        reason = request.POST.get('reason')

        Expenses.objects.create(
            Date=date,
            Reason=reason,
            Amount=amount,
        )

    else:
        print("No username found in session.")  # Debugging statement

        return redirect('addExpenses')  # Replace with your desired success URL

    return render(request, 'expenses.html')

def viewExpenses(request):
    expenses = []
    grand_total = 0  # Initialize the grand total to 0

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        # Initialize the filter query
        filters = {}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter

            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        # Query the Expenses model with the combined filters
        expenses = Expenses.objects.filter(**filters)

        # Calculate the grand total of Amount
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0  # Aggregate sum of Amount

    return render(request, 'viewExpenses.html', {'expenses': expenses, 'grand_total': grand_total})


def get_staff_name(request):
    query = request.GET.get('query', '')
    if query:
        username = UserReg.objects.filter(username__icontains=query).values_list('username', flat=True)
        print('username numbers:', list(username))  # Debugging: check the data in the terminal
        return JsonResponse(list(username), safe=False)
    return JsonResponse([], safe=False)

def salary(request):
    return render(request, 'salary.html')

def saveSalary(request):
    if request.method == 'POST':
        # Parse and validate date
        date_str = request.POST.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")  # Debugging statement
            return redirect('adminExpenses')
        amount = request.POST.get('amt')
        reason = request.POST.get('reason')
        salaryDetails = request.POST.get('salaryDetails')

        Salary.objects.create(
            Date=date,
            desc=reason,
            Amount=amount,
            staffname=salaryDetails,
        )

    else:
        print("No username found in session.")  # Debugging statement

        return redirect('salary')  # Replace with your desired success URL

    return render(request, 'salary.html')


def viewSalary(request):
    expenses = []
    grand_total = 0  # Initialize the grand total to 0

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        staffname = request.POST.get('staffname')

        # Initialize the filter query
        filters = {}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter
            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        if staffname:
            filters['staff_name__icontains'] = staffname  # Staff name filter

        # Query the Salary model with the combined filters
        expenses = Salary.objects.filter(**filters)

        # Calculate the grand total of Amount
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0  # Aggregate sum of Amount

    return render(request, 'viewSalary.html', {'expenses': expenses, 'grand_total': grand_total})


from django.db.models import Sum
def profit_report(request):
    # Get the from_date and to_date from the request (if provided)
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    from_date = parse_date(from_date_str) if from_date_str else None
    to_date = parse_date(to_date_str) if to_date_str else None

    # Query all consignments and expenses
    consignments = Orders.objects.all()
    expenses = Expenses.objects.all()

    # Filter by date range if provided
    if from_date and to_date:
        consignments = consignments.filter(bill_date__range=[from_date, to_date])
        expenses = expenses.filter(Date__range=[from_date, to_date])

    # Track already processed track_ids
    processed_track_ids = set()

    # This list will store the unique consignments
    unique_consignments = []

    # Iterate over all consignments to ensure only unique track_id costs are added
    for consignment in consignments:
        track_id = consignment.bill_no
        # If track_id is not already processed, add its total_cost to the unique list
        if track_id not in processed_track_ids:
            processed_track_ids.add(track_id)
            unique_consignments.append(consignment)

    # Now group by date and branch, summing the total_cost of the unique consignments
    consignments_grouped = (
        Orders.objects.filter(id__in=[c.id for c in unique_consignments])
        .values('bill_date')
        .annotate(total=Sum('total'))
        .order_by('bill_date')
    )

    # Group expenses by Date and Reason, and calculate total Amount for each group
    expenses_grouped = expenses.values('Date', 'Reason').annotate(
        total_amount=Sum('Amount')
    ).order_by('Date', 'Reason')

    # Calculate grand totals for consignments and expenses
    grand_total_consignment = sum(item['total'] for item in consignments_grouped)
    grand_total_expenses = sum(item['total_amount'] for item in expenses_grouped)

    # Calculate combined grand total
    combined_grand_total = grand_total_consignment + grand_total_expenses

    # Calculate profit or loss
    total_balance = grand_total_consignment - grand_total_expenses

    # Set profit and loss
    profit = total_balance if total_balance > 0 else 0
    loss = abs(total_balance) if total_balance < 0 else 0

    # Pass the grouped data and totals to the template
    return render(request, 'profit_report.html', {
        'consignments': consignments_grouped,
        'expenses': expenses_grouped,
        'grand_total_consignment': grand_total_consignment,
        'grand_total_expenses': grand_total_expenses,
        'combined_grand_total': combined_grand_total,
        'profit': profit,
        'loss': loss,
        'from_date': from_date_str,
        'to_date': to_date_str,
    })

