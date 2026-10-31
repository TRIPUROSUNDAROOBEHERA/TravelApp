from django.urls import path
from . import views

urlpatterns = [
    # Public & Landing
    path('', views.index, name='index'),
    path('index.html', views.index, name='index_html'),
    path('FAQ.html', views.FAQ, name='FAQ'),
    path('FAQ', views.FAQ, name='FAQ_clean'),
    path('Logout', views.Logout, name='Logout'),

    # User Authentication
    path('UserLogin.html', views.UserLogin, name='UserLogin'),
    path('UserLogin', views.UserLogin, name='UserLogin_clean'),
    path('UserLoginAction', views.UserLoginAction, name='UserLoginAction'),
    path('Register.html', views.Register, name='Register'),
    path('Register', views.Register, name='Register_clean'),
    path('RegisterAction', views.RegisterAction, name='RegisterAction'),

    # Admin Authentication & Screens
    path('AdminLogin.html', views.AdminLogin, name='AdminLogin'),
    path('AdminLogin', views.AdminLogin, name='AdminLogin_clean'),
    path('AdminLoginAction', views.AdminLoginAction, name='AdminLoginAction'),
    path('AdminScreen.html', views.AdminScreen, name='AdminScreen_html'),
    path('AdminScreen', views.AdminScreen, name='AdminScreen'),

    # Employee Authentication & Screens
    path('EmployeeLogin.html', views.EmployeeLogin, name='EmployeeLogin'),
    path('EmployeeLogin', views.EmployeeLogin, name='EmployeeLogin_clean'),
    path('EmployeeLoginAction', views.EmployeeLoginAction, name='EmployeeLoginAction'),
    path('EmployeeScreen.html', views.EmployeeScreen, name='EmployeeScreen_html'),
    path('EmployeeScreen', views.EmployeeScreen, name='EmployeeScreen'),

    # Admin: Employee Management & Audit Logs
    path('AddEmployee.html', views.AddEmployee, name='AddEmployee'),
    path('AddEmployee', views.AddEmployee, name='AddEmployee_clean'),
    path('AddEmployeeAction', views.AddEmployeeAction, name='AddEmployeeAction'),
    path('ViewEmployee.html', views.ViewEmployee, name='ViewEmployee_html'),
    path('ViewEmployee', views.ViewEmployee, name='ViewEmployee'),
    path('ViewAuthEmployee.html', views.ViewAuthEmployee, name='ViewAuthEmployee'),
    path('ViewAuthEmployee', views.ViewAuthEmployee, name='ViewAuthEmployee_clean'),
    path('ViewAuthEmployeeAction', views.ViewAuthEmployeeAction, name='ViewAuthEmployeeAction'),

    # Itinerary Management
    path('Itinerary.html', views.itinerary_view, name='Itinerary'),
    path('Itinerary', views.itinerary_view, name='Itinerary_clean'),
    path('CreateItinerary.html', views.CreateItinerary, name='CreateItinerary'),
    path('CreateItinerary', views.CreateItinerary, name='CreateItinerary_clean'),
    path('CreateItineraryAction', views.CreateItineraryAction, name='CreateItineraryAction'),
    path('ViewItinerary.html', views.ViewItinerary, name='ViewItinerary_html'),
    path('ViewItinerary', views.ViewItinerary, name='ViewItinerary'),
    path('ModifyItinerary.html', views.ModifyItinerary, name='ModifyItinerary_html'),
    path('ModifyItinerary', views.ModifyItinerary, name='ModifyItinerary'),
    path('ModifyItineraryAction', views.ModifyItineraryAction, name='ModifyItineraryAction'),
    path('DeleteItinerary', views.DeleteItinerary, name='DeleteItinerary'),

    # Hotel Management
    path('Hotels.html', views.Hotels, name='Hotels'),
    path('Hotels', views.Hotels, name='Hotels_clean'),
    path('AddHotel.html', views.AddHotel, name='AddHotel'),
    path('AddHotel/', views.AddHotel, name='AddHotel_slash'),
    path('AddHotel', views.AddHotel, name='AddHotel_clean'),
    path('AddHotelAction', views.AddHotelAction, name='AddHotelAction'),
    path('ViewHotel.html', views.ViewHotel, name='ViewHotel_html'),
    path('ViewHotel/', views.ViewHotel, name='ViewHotel_slash'),
    path('ViewHotel', views.ViewHotel, name='ViewHotel'),
    path('ModifyHotel.html', views.ModifyHotel, name='ModifyHotel_html'),
    path('ModifyHotel', views.ModifyHotel, name='ModifyHotel'),
    path('ModifyHotelAction', views.ModifyHotelAction, name='ModifyHotelAction'),
    path('DeleteHotelAction', views.DeleteHotelAction, name='DeleteHotelAction'),

    # Transport Management
    path('Transport.html', views.TransportPage, name='Transport'),
    path('Transport/', views.TransportPage, name='Transport_slash'),
    path('Transport', views.TransportPage, name='Transport_clean'),
    path('AddTransport.html', views.AddTransport, name='AddTransport'),
    path('AddTransport/', views.AddTransport, name='AddTransport_slash'),
    path('AddTransport', views.AddTransport, name='AddTransport_clean'),
    path('AddTransportAction/', views.AddTransportAction, name='AddTransportAction'),
    path('AddTransportAction', views.AddTransportAction, name='AddTransportAction_clean'),
    path('ViewTransport/', views.ViewTransport, name='ViewTransport'),
    path('ViewTransport', views.ViewTransport, name='ViewTransport_clean'),
    path('ModifyTransport.html', views.ModifyTransport, name='ModifyTransport_html'),
    path('ModifyTransport', views.ModifyTransport, name='ModifyTransport'),
    path('ModifyTransportAction', views.ModifyTransportAction, name='ModifyTransportAction'),
    path('DeleteTransport', views.DeleteTransport, name='DeleteTransport'),

    # User Search & Booking
    path('SearchItinerary/', views.SearchItinerary, name='SearchItinerary_slash'),
    path('SearchItinerary', views.SearchItinerary, name='SearchItinerary'),
    path('BookItinerary', views.BookItinerary, name='BookItinerary'),
    path('BookItineraryAction', views.BookItineraryAction, name='BookItineraryAction'),

    path('SearchTransport/', views.SearchTransport, name='SearchTransport'),
    path('SearchTransport', views.SearchTransport, name='SearchTransport_clean'),
    path('BookTransport', views.BookTransport, name='BookTransport'),
    path('BookTransportAction', views.BookTransportAction, name='BookTransportAction'),

    path('SearchHotels/', views.SearchHotels, name='SearchHotels'),
    path('SearchHotels', views.SearchHotels, name='SearchHotels_clean'),
    path('BookHotel', views.BookHotel, name='BookHotel'),
    path('BookHotelAction', views.BookHotelAction, name='BookHotelAction'),

    path('CancelBookings/', views.CancelBookings, name='CancelBookings_slash'),
    path('CancelBookings', views.CancelBookings, name='CancelBookings'),
    path('CancelBookingAction/', views.CancelBookingAction, name='CancelBookingAction'),
    path('CancelBookingAction', views.CancelBookingAction, name='CancelBookingAction_clean'),
    path('ViewBookings', views.ViewBookings, name='ViewBookings'),

    # Feedback
    path('Feedbacks.html', views.Feedbacks, name='Feedbacks'),
    path('feedbacks/', views.Feedbacks, name='Feedbacks_slash'),
    path('feedback/', views.feedback_view, name='FeedbackRatings'),
    path('feedback', views.feedback_view, name='FeedbackRatings_clean'),
    path('feedback/submit/', views.FeedbacksAction, name='FeedbacksAction_slash'),
    path('FeedbacksAction', views.FeedbacksAction, name='FeedbacksAction'),
    path('ViewFeedback', views.ViewFeedback, name='ViewFeedback'),
]
