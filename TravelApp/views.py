from datetime import datetime
from decimal import Decimal
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.utils.safestring import mark_safe

from .models import Admin, Employee, User, Hotel, Itinerary, Transport


def parse_date(date_str):
    """Safely parse DD-MM-YYYY, DD/MM/YYYY, or YYYY-MM-DD into YYYY-MM-DD."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    date_str = str(date_str).strip()
    sep = '/' if '/' in date_str else '-'
    parts = date_str.split(sep)
    if len(parts) == 3:
        if len(parts[0]) == 4:  # YYYY-MM-DD
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        elif len(parts[2]) == 4:  # DD-MM-YYYY
            return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
    return datetime.now().strftime('%Y-%m-%d')


def clean_price(val):
    """Strip currency symbols, commas, and whitespace from price strings."""
    if val is None:
        return "0.00"
    cleaned = str(val).replace('$', '').replace(',', '').strip()
    return cleaned if cleaned else "0.00"


# ==============================================================================
# Public / Authentication Views
# ==============================================================================

def index(request):
    return render(request, 'index.html')


def FAQ(request):
    return render(request, 'FAQ.html')


def Logout(request):
    request.session.flush()
    return redirect('index')


# --- User Authentication ---

def UserLogin(request):
    if request.session.get('user') and request.session.get('role') == 'user':
        return redirect('SearchItinerary')
    return render(request, 'UserLogin.html')


def UserLoginAction(request):
    if request.method == 'POST':
        uname = request.POST.get('t1', '').strip()
        upass = request.POST.get('t2', '').strip()
        user_account = User.objects.filter(username=uname, password=upass).first()

        if user_account:
            request.session['user'] = uname
            request.session['role'] = 'user'
            return redirect('SearchItinerary')
        else:
            return render(request, 'UserLogin.html', {'data': 'Invalid Login'})
    if request.session.get('user') and request.session.get('role') == 'user':
        return redirect('SearchItinerary')
    return render(request, 'UserLogin.html')


def Register(request):
    return render(request, 'Register.html')


def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', '').strip()
        password = request.POST.get('t2', '').strip()
        contact = request.POST.get('t3', '').strip()
        email = request.POST.get('t4', '').strip()
        address = request.POST.get('t5', '').strip()

        if User.objects.filter(username=username).exists():
            data = f"Given {username} already exists"
            return render(request, 'Register.html', {'data': data})

        try:
            User.objects.create(
                username=username,
                password=password,
                phone_no=contact,
                email=email,
                address=address
            )
            data = "Signup Done! You can login now"
            return render(request, 'Register.html', {'data': data})
        except Exception as e:
            return render(request, 'Register.html', {'data': f"Error in signup process: {str(e)}"})

    return render(request, 'Register.html')


# --- Employee Authentication ---

def checkUser(uname, password, utype):
    try:
        if str(utype).lower() == 'admin':
            user = Admin.objects.filter(username=uname, password=password).first()
            if not user and uname == 'admin' and password == 'admin':
                return "success"
        elif str(utype).lower() == 'employee':
            user = Employee.objects.filter(username=uname, password=password).first()
        else:
            user = User.objects.filter(username=uname, password=password).first()

        if user:
            return "success"
    except Exception as e:
        print(f"Login error: {e}")
    return "Invalid Login Details"


def EmployeeLogin(request):
    if request.session.get('employee'):
        return render(request, 'EmployeeScreen.html')
    return render(request, 'EmployeeLogin.html')


def EmployeeLoginAction(request):
    if request.method == 'POST':
        u = request.POST.get('t1', '').strip()
        p = request.POST.get('t2', '').strip()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if checkUser(u, p, 'Employee') == "success":
            request.session['user'] = u
            request.session['employee'] = u
            request.session['role'] = 'employee'

            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO notification (employee_name, login_date, login_status) VALUES (%s, %s, %s)",
                        [u, now_str, 'Login Successful']
                    )
            except Exception as e:
                print(f"Notification log error: {e}")

            return render(request, 'EmployeeScreen.html')
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO notification (employee_name, login_date, login_status) VALUES (%s, %s, %s)",
                        [u if u else 'Unknown', now_str, 'Failed Login']
                    )
            except Exception as e:
                print(f"Notification log error: {e}")

            return render(request, 'EmployeeLogin.html', {'data': 'Invalid Employee Credentials'})

    if request.session.get('employee'):
        return render(request, 'EmployeeScreen.html')
    return render(request, 'EmployeeLogin.html')


def EmployeeScreen(request):
    return render(request, 'EmployeeScreen.html')


# --- Admin Authentication & Dashboard ---

def AdminLogin(request):
    if request.session.get('admin'):
        return render(request, "AdminScreen.html")
    return render(request, "AdminLogin.html")


def AdminLoginAction(request):
    if request.method == "POST":
        username = request.POST.get("t1", "").strip()
        password = request.POST.get("t2", "").strip()

        admin_obj = Admin.objects.filter(username=username, password=password).first()
        if admin_obj or (username == "admin" and password == "admin"):
            request.session['admin'] = username
            request.session['role'] = 'admin'
            return render(request, "AdminScreen.html")
        else:
            return render(request, "AdminLogin.html", {"data": "Invalid Login"})

    if request.session.get('admin'):
        return render(request, "AdminScreen.html")
    return render(request, "AdminLogin.html")


def AdminScreen(request):
    return render(request, "AdminScreen.html")


# ==============================================================================
# Admin Section: Employee Management & Audit Logs
# ==============================================================================

def AddEmployee(request):
    return render(request, 'AddEmployee.html')


def AddEmployeeAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', '').strip()
        password = request.POST.get('t2', '').strip()
        contact = request.POST.get('t3', '').strip()
        email = request.POST.get('t4', '').strip()
        address = request.POST.get('t5', '').strip()

        if Employee.objects.filter(username=username).exists():
            return render(request, 'AddEmployee.html', {'data': f"Employee '{username}' already exists."})

        try:
            Employee.objects.create(
                username=username,
                password=password,
                phone_no=contact,
                email=email,
                address=address
            )
            return render(request, 'AddEmployee.html', {'data': f"Employee '{username}' added successfully."})
        except Exception as e:
            return render(request, 'AddEmployee.html', {'data': f"Error adding employee: {str(e)}"})

    return render(request, 'AddEmployee.html')


def ViewEmployee(request):
    employees = Employee.objects.all().order_by('-id')
    return render(request, 'ViewEmployee.html', {'employees': employees})


def ViewAuthEmployee(request):
    return render(request, 'ViewAuthEmployee.html')


def ViewAuthEmployeeAction(request):
    if request.method == 'POST':
        t1 = request.POST.get('t1', '').strip()
        t2 = request.POST.get('t2', '').strip()

        if not t1 or not t2:
            return render(request, 'ViewAuthEmployee.html', {'data': 'Please select both dates.'})

        try:
            from_date = f"{parse_date(t1)} 00:00:00"
            to_date = f"{parse_date(t2)} 23:59:59"

            with connection.cursor() as cursor:
                sql = """SELECT employee_name, login_date, login_status 
                         FROM notification 
                         WHERE login_date BETWEEN %s AND %s 
                         ORDER BY login_date DESC"""
                cursor.execute(sql, [from_date, to_date])
                res_logs = cursor.fetchall()

            if not res_logs:
                return render(request, 'ViewAuthEmployee.html', {'data': 'No records found for these dates.'})

            # Template ViewAuthEmployee.html expects dictionary objects with username, login_date, login_status
            log_list = [{'username': r[0], 'login_date': r[1], 'login_status': r[2]} for r in res_logs]
            return render(request, 'ViewAuthEmployee.html', {'logs': log_list})

        except Exception as e:
            return render(request, 'ViewAuthEmployee.html', {'data': f'System Error: {str(e)}'})

    return render(request, 'ViewAuthEmployee.html')


# ==============================================================================
# Itinerary Management
# ==============================================================================

def itinerary_view(request):
    return render(request, 'Itinerary.html')


def ItineraryPage(request):
    return render(request, 'Itinerary.html')


def CreateItinerary(request):
    if request.method == 'POST':
        name = request.POST.get('t1', '').strip()
        desc = request.POST.get('t2', '').strip()
        price = clean_price(request.POST.get('t3', '0'))

        try:
            Itinerary.objects.create(
                package_name=name,
                description=desc,
                price=Decimal(price)
            )
            messages.success(request, f"Success! {name} has been published to the catalog.")
            return redirect('ViewItinerary')
        except Exception as e:
            return render(request, 'CreateItinerary.html', {'data': f"Error saving to database: {e}"})

    return render(request, 'CreateItinerary.html')


def CreateItineraryAction(request):
    return CreateItinerary(request)


def ViewItinerary(request):
    data = Itinerary.objects.all().order_by('-package_id')
    return render(request, 'ViewItinerary.html', {'itineraries': data})


def ModifyItinerary(request):
    pid = request.POST.get('pid') or request.GET.get('pid') or request.POST.get('t1')
    item = get_object_or_404(Itinerary, package_id=pid)

    if request.method == 'POST':
        item.package_name = request.POST.get('t1', '').strip()
        item.description = request.POST.get('t2', '').strip()
        try:
            item.price = Decimal(clean_price(request.POST.get('t3', '0')))
        except Exception:
            pass
        item.save()
        messages.success(request, f"Itinerary '{item.package_name}' updated successfully.")
        return redirect('ViewItinerary')

    return render(request, 'ModifyItinerary.html', {'item': item})


def ModifyItineraryAction(request):
    return ModifyItinerary(request)


def DeleteItinerary(request):
    pid = request.GET.get('pid')
    if pid:
        Itinerary.objects.filter(package_id=pid).delete()
        messages.success(request, "Itinerary removed successfully.")
    return redirect('ViewItinerary')


# ==============================================================================
# Hotel Management
# ==============================================================================

def Hotels(request):
    return render(request, 'Hotels.html')


def AddHotel(request):
    return render(request, 'AddHotel.html')


def AddHotelAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', '').strip()
        room = request.POST.get('t2', '').strip()
        entry = request.POST.get('t3', '').strip()
        ending = request.POST.get('t4', '').strip()
        duration = request.POST.get('t5', '').strip()
        loc = request.POST.get('t6', '').strip()
        price = clean_price(request.POST.get('t7', '0'))
        amenities = request.POST.get('t8', '').strip()

        try:
            Hotel.objects.create(
                hotel_name=name,
                room_number=room,
                entry_time=entry,
                ending_time=ending,
                duration_desc=duration,
                location=loc,
                price_night=Decimal(price),
                amenities=amenities
            )
            return redirect('ViewHotel')
        except Exception as e:
            return render(request, 'AddHotel.html', {'data': f"Error registering hotel: {str(e)}"})

    return render(request, 'AddHotel.html')


def ViewHotel(request):
    hotels = Hotel.objects.all().order_by('-hotel_id')
    return render(request, 'ViewHotel.html', {'hotels': hotels})


def ModifyHotel(request):
    pid = request.POST.get('hotel_id') or request.GET.get('pid')
    hotel = get_object_or_404(Hotel, hotel_id=pid)

    context = {
        'hotel_id': hotel.hotel_id,
        'hotel_name': hotel.hotel_name,
        'room_number': hotel.room_number,
        'entry_time': hotel.entry_time,
        'ending_time': hotel.ending_time,
        'duration_desc': hotel.duration_desc,
        'location': hotel.location,
        'price_night': hotel.price_night,
        'amenities': hotel.amenities
    }
    return render(request, 'ModifyHotel.html', context)


def ModifyHotelAction(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        hotel = Hotel.objects.filter(hotel_id=hotel_id).first()
        if hotel:
            hotel.hotel_name = request.POST.get('t1', '').strip()
            hotel.room_number = request.POST.get('t2', '').strip()
            hotel.entry_time = request.POST.get('t3', '').strip()
            hotel.ending_time = request.POST.get('t4', '').strip()
            hotel.duration_desc = request.POST.get('t5', '').strip()
            hotel.location = request.POST.get('t6', '').strip()
            try:
                hotel.price_night = Decimal(clean_price(request.POST.get('t7', '0')))
            except Exception:
                pass
            hotel.amenities = request.POST.get('t8', '').strip()
            hotel.save()
            messages.success(request, f"Hotel '{hotel.hotel_name}' updated successfully.")
        return redirect('ViewHotel')

    return redirect('ViewHotel')


def DeleteHotelAction(request):
    pid = request.GET.get('pid')
    if pid:
        Hotel.objects.filter(hotel_id=pid).delete()
        messages.success(request, f"Hotel Asset #{pid} purged from the database.")
    return redirect('ViewHotel')


# ==============================================================================
# Transport Management
# ==============================================================================

def TransportPage(request):
    return render(request, 'Transport.html')


def AddTransport(request):
    return render(request, 'AddTransport.html')


def AddTransportAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', '').strip()
        source = request.POST.get('t2', '').strip()
        dest = request.POST.get('t3', '').strip()
        dep = request.POST.get('t4', '').strip()
        arr = request.POST.get('t5', '').strip()
        price = clean_price(request.POST.get('t6', '0'))

        try:
            Transport.objects.create(
                transport_name=name,
                source=source,
                destination=dest,
                departure_time=dep,
                arrival_time=arr,
                price=Decimal(price)
            )
            messages.success(request, f"Success! {name} has been deployed to the network.")
        except Exception as e:
            messages.error(request, f"Error adding transport: {str(e)}")

        return render(request, 'AddTransport.html')

    return render(request, 'AddTransport.html')


def ViewTransport(request):
    items = Transport.objects.all().order_by('-id')
    return render(request, 'ViewTransport.html', {'items': items})


def ModifyTransport(request):
    pid = request.POST.get('t0') or request.GET.get('pid')
    item = get_object_or_404(Transport, id=pid)

    if request.method == 'POST':
        item.transport_name = request.POST.get('t1', '').strip()
        item.source = request.POST.get('t2', '').strip()
        item.destination = request.POST.get('t3', '').strip()
        item.departure_time = request.POST.get('t4', '').strip()
        item.arrival_time = request.POST.get('t5', '').strip()
        try:
            item.price = Decimal(clean_price(request.POST.get('t6', '0')))
        except Exception:
            item.price = Decimal('0.00')
        item.save()
        messages.success(request, f"Transport '{item.transport_name}' updated successfully.")
        return redirect('ViewTransport')

    return render(request, 'ModifyTransport.html', {'item': item})


def ModifyTransportAction(request):
    return ModifyTransport(request)


def DeleteTransport(request):
    pid = request.GET.get('pid')
    if pid:
        Transport.objects.filter(id=pid).delete()
        messages.success(request, "Transport record deleted successfully.")
    return redirect('ViewTransport')


# ==============================================================================
# User Search & Booking Services
# ==============================================================================

def SearchItinerary(request):
    itineraries = Itinerary.objects.all().order_by('-package_id')
    data = [{'id': r.package_id, 'name': r.package_name, 'desc': r.description, 'price': str(r.price)} for r in itineraries]
    return render(request, 'UserScreen.html', {'itineraries': data})


def SearchTransport(request):
    transports = Transport.objects.all().order_by('-id')
    data = [{
        'id': r.id,
        'name': r.transport_name,
        'desc': f"Route: {r.source} -> {r.destination} (Dep: {r.departure_time}, Arr: {r.arrival_time})",
        'price': str(r.price)
    } for r in transports]
    return render(request, 'UserScreen.html', {'itineraries': data})


def SearchHotels(request):
    hotels = Hotel.objects.all().order_by('-hotel_id')
    return render(request, 'SearchHotels.html', {'itineraries': hotels})


# --- Book Itinerary ---

def BookItinerary(request):
    pid = request.GET.get('pid', '0')
    price = clean_price(request.GET.get('price', '0'))
    output = f'''
        <div class="flex justify-between items-center mb-2">
            <span class="text-gray-400 text-[10px] font-bold uppercase">Package Reference</span>
            <span class="text-slate-800 font-bold">PKG-0{pid}</span>
            <input type="hidden" name="t1" value="{pid}">
        </div>
        <div class="flex justify-between items-center border-t pt-2">
            <span class="text-gray-400 text-[10px] font-bold uppercase">Grand Total</span>
            <span class="text-[#990000] font-black text-lg">${price}</span>
            <input type="hidden" name="t2" value="{price}">
        </div>
    '''
    return render(request, 'BookItinerary.html', {'data1': mark_safe(output)})


def BookItineraryAction(request):
    if request.method == 'POST':
        current_user = request.session.get('user')
        if not current_user:
            return redirect('UserLogin')

        pid = request.POST.get('t1')
        price = clean_price(request.POST.get('t2', '0'))
        travel_date = parse_date(request.POST.get('t3'))
        card_no = request.POST.get('t4', '').replace(' ', '').strip()
        cvv = request.POST.get('t5', '').strip()
        booking_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(booking_id) FROM BookItinerary")
                row = cursor.fetchone()
                bid = (row[0] + 1) if row and row[0] is not None else 1

                sql = """INSERT INTO BookItinerary 
                         (booking_id, username, package_id, price, travel_date, card_no, cvv_no, booking_date, booking_type) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, [bid, current_user, pid, price, travel_date, card_no, cvv, booking_timestamp, 'Itinerary'])
                messages.success(request, f"Payment Successful for {current_user}! Ref: #0{bid}")
        except Exception as e:
            messages.error(request, f"Database Error: {str(e)}")

        return redirect(f'/BookItinerary?pid={pid}&price={price}')

    return redirect('SearchItinerary')


# --- Book Transport ---

def BookTransport(request):
    pid = request.GET.get('pid', '0')
    price = clean_price(request.GET.get('price', '0'))
    output = f'''
        <div class="flex justify-between items-center mb-1">
            <span class="text-gray-400 text-[10px] font-black uppercase">Fleet Reference</span>
            <span class="text-slate-800 font-bold">#TR-0{pid}</span>
            <input type="hidden" name="t1" value="{pid}">
        </div>
        <div class="flex justify-between items-center border-t border-slate-100 pt-2 mt-1">
            <span class="text-gray-400 text-[10px] font-black uppercase">Grand Total</span>
            <span class="text-[#990000] font-black text-lg">${price}</span>
            <input type="hidden" name="t2" value="{price}">
        </div>
    '''
    return render(request, 'BookTransport.html', {'data1': mark_safe(output)})


def BookTransportAction(request):
    if request.method == 'POST':
        current_user = request.session.get('user')
        if not current_user:
            return redirect('UserLogin')

        pid = request.POST.get('t1')
        price = clean_price(request.POST.get('t2', '0'))
        formatted_travel_date = parse_date(request.POST.get('t3'))
        card = request.POST.get('t4', '').replace(' ', '').strip()
        cvv = request.POST.get('t5', '').strip()
        today_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with connection.cursor() as dbcursor:
                dbcursor.execute("SELECT MAX(booking_id) FROM BookItinerary")
                row = dbcursor.fetchone()
                bid = (row[0] + 1) if row and row[0] is not None else 1

                qry = """INSERT INTO BookItinerary 
                         (booking_id, username, package_id, price, travel_date, card_no, cvv_no, booking_date, booking_type) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                dbcursor.execute(qry, [bid, current_user, pid, price, formatted_travel_date, card, cvv, today_timestamp, 'Transport'])
                messages.success(request, f"Payment Successful! Transport Asset TR-0{pid} secured for user: {current_user}. Ref ID: #{bid}")
        except Exception as e:
            messages.error(request, f"Terminal Connection Error: {str(e)}")

        return redirect(f'/BookTransport?pid={pid}&price={price}')

    return redirect('SearchTransport')


# --- Book Hotel ---

def BookHotel(request):
    pid = request.GET.get('pid', '0')
    price = clean_price(request.GET.get('price', '0'))
    output = f'''
        <div class="flex justify-between items-center mb-1">
            <span class="text-gray-400 text-[10px] font-black uppercase tracking-widest">Asset Reference</span>
            <span class="text-slate-800 font-bold">#HTL-0{pid}</span>
            <input type="hidden" name="t1" value="{pid}">
        </div>
        <div class="flex justify-between items-center border-t border-slate-100 pt-2 mt-1">
            <span class="text-gray-400 text-[10px] font-black uppercase tracking-widest">Grand Total</span>
            <span class="text-[#990000] font-black text-lg">${price}</span>
            <input type="hidden" name="t2" value="{price}">
        </div>
    '''
    return render(request, 'BookHotel.html', {'data1': mark_safe(output)})


def BookHotelAction(request):
    if request.method == 'POST':
        current_user = request.session.get('user')
        if not current_user:
            messages.warning(request, "Session expired. Please re-authenticate.")
            return redirect('UserLogin')

        pid = request.POST.get('t1')
        price = clean_price(request.POST.get('t2', '0'))
        db_date = parse_date(request.POST.get('t3'))
        card = request.POST.get('t4', '').replace(' ', '').strip()
        cvv = request.POST.get('t5', '').strip()
        today_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with connection.cursor() as dbcursor:
                dbcursor.execute("SELECT MAX(booking_id) FROM BookItinerary")
                res = dbcursor.fetchone()[0]
                bid = (res + 1) if res else 1

                qry = """INSERT INTO BookItinerary 
                         (booking_id, username, package_id, price, travel_date, card_no, cvv_no, booking_date, booking_type) 
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                dbcursor.execute(qry, [bid, current_user, pid, price, db_date, card, cvv, today_timestamp, 'Hotel'])
                messages.success(request, f"Payment Successful! Hotel Asset #HTL-0{pid} secured for {current_user}. Ref ID: #{bid}")
        except Exception as e:
            messages.error(request, f"Terminal Database Error: {str(e)}")

        return redirect(f'/BookHotel?pid={pid}&price={price}')

    return redirect('SearchHotels')


# --- User Bookings & Cancellations ---

def CancelBookings(request):
    current_user = request.session.get('user')
    if not current_user:
        return redirect('UserLogin')

    with connection.cursor() as cursor:
        sql = """SELECT booking_id, booking_type, price, travel_date 
                 FROM BookItinerary 
                 WHERE username = %s 
                 ORDER BY booking_id DESC"""
        cursor.execute(sql, [current_user])
        rows = cursor.fetchall()
        user_bookings = [{'id': r[0], 'name': r[1], 'price': r[2], 'desc': r[3]} for r in rows]

    return render(request, 'UserScreen.html', {'itineraries': user_bookings})


def CancelBookingAction(request):
    pid = request.GET.get('pid') or request.POST.get('pid')
    referer = request.META.get('HTTP_REFERER', '')

    if pid:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT booking_type, price FROM BookItinerary WHERE booking_id=%s", [pid])
                details = cursor.fetchone()

                if details:
                    cursor.execute("DELETE FROM BookItinerary WHERE booking_id=%s", [pid])
                    msg = f"PURGE SUCCESS: {details[0]} Asset (Valued at ${details[1]}) removed from system."
                    messages.success(request, msg)
                else:
                    messages.error(request, "ERROR: Asset Reference not found in current sector.")
        except Exception as e:
            messages.error(request, f"SYSTEM FAILURE: {str(e)}")

    if 'ViewBookings' in referer:
        return redirect('ViewBookings')
    return redirect('CancelBookings')


def ViewBookings(request):
    if request.method == 'GET':
        output = '<table style="width:100%; border-collapse:collapse;">'
        output += '''
            <thead>
                <tr style="background-color: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">ID</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Asset ID</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">User Name</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Price</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Schedule Date</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Card / CVV</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Booking Date</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Type</th>
                    <th style="padding:20px; color:#145bbe; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em; text-align:right;">Operations</th>
                </tr>
            </thead>
            <tbody>
        '''

        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT booking_id, username, package_id, price, travel_date, card_no, cvv_no, booking_date, booking_type 
                                  FROM BookItinerary 
                                  ORDER BY booking_id DESC""")
                lists = cursor.fetchall()

                for ls in lists:
                    card_display = f"****{str(ls[5])[-4:]}" if len(str(ls[5])) >= 4 else str(ls[5])
                    output += f'''
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding:20px; font-weight:800; color:#990000;">0{ls[0]}</td>
                        <td style="padding:20px; color:#475569; font-weight:600;">REF-{ls[2]}</td>
                        <td style="padding:20px; color:#1e293b; font-weight:600;">{ls[1]}</td>
                        <td style="padding:20px; color:#1e293b; font-weight:900;">${ls[3]}</td>
                        <td style="padding:20px; color:#64748b; font-size:12px;">{ls[4]}</td>
                        <td style="padding:20px; font-family:monospace; font-size:11px; color:#94a3b8;">{card_display} / {ls[6]}</td>
                        <td style="padding:20px; color:#94a3b8; font-size:11px;">{ls[7]}</td>
                        <td style="padding:20px;">
                            <span style="background:#f1f5f9; color:#54b3a4; padding:4px 10px; border-radius:99px; font-size:9px; font-weight:800; text-transform:uppercase;">{ls[8]}</span>
                        </td>
                        <td style="padding:20px; text-align:right;">
                            <a href="/CancelBookingAction?pid={ls[0]}" onclick="return confirm('Confirm permanent deletion of record 0{ls[0]}?')" 
                               style="background:#fff1f2; color:#e11d48; padding:8px 16px; border-radius:99px; font-size:10px; font-weight:800; text-decoration:none; text-transform:uppercase;">
                                Cancel
                            </a>
                        </td>
                    </tr>
                    '''

            if not lists:
                output += '<tr><td colspan="9" style="padding:80px; text-align:center; color:#cbd5e1; font-style:italic;">No transaction records found in the current sector.</td></tr>'

        except Exception as e:
            output += f'<tr><td colspan="9" style="padding:20px; color:#ef4444;">System Error: {str(e)}</td></tr>'

        output += '</tbody></table>'
        return render(request, 'ViewBookings.html', {'data': mark_safe(output)})


# ==============================================================================
# Feedback Management
# ==============================================================================

def ViewFeedback(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, feedback, ratings, feedback_date FROM feedback ORDER BY feedback_date DESC")
            rows = cursor.fetchall()
            feedback_list = [{'username': r[0], 'feedback': r[1], 'ratings': r[2], 'feedback_date': r[3]} for r in rows]
    except Exception as e:
        feedback_list = []

    return render(request, 'ViewFeedback.html', {'feedbacks': feedback_list})


def feedback_view(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('t1', '').strip()
        rating_value = request.POST.get('t2', '').strip()
        username = request.session.get('user', 'Anonymous')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO feedback(username, feedback, ratings, feedback_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, [username, feedback_text, rating_value, today])
            return render(request, 'Feedback.html', {'data': 'Intelligence Transmitted Successfully'})
        except Exception as e:
            return render(request, 'Feedback.html', {'data': f'Transmission Error: {str(e)}'})

    return render(request, 'Feedback.html')


def Feedbacks(request):
    return render(request, 'Feedbacks.html', {})


def FeedbacksAction(request):
    if request.method == 'POST':
        user = request.session.get('user', 'Anonymous')
        feedback = request.POST.get('t1', '').strip()
        rating = request.POST.get('t2', '').strip()
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO feedback(username, feedback, ratings, feedback_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, [str(user), feedback, rating, today])
            data = "Your feedback Accepted! Our employees will work on it"
        except Exception as e:
            data = f"Error: {str(e)}"

        return render(request, 'UserScreen.html', {'data': data})

    return redirect('FeedbackRatings')
