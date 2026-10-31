from django.db import models

# 1. Admin Model
class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'TravelApp_admin'

# 2. Employee Model
class Employee(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    class Meta:
        db_table = 'employee'

# 3. User Signup Model
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    class Meta:
        db_table = "user_signup"

# 4. Hotel Stay Model (Updated for your new UI)

class Hotel(models.Model):
    # Explicit Primary Key
    hotel_id = models.AutoField(primary_key=True)
    
    # Information Fields
    hotel_name = models.CharField(max_length=200)
    room_number = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    
    # Timing Fields
    entry_time = models.CharField(max_length=50)
    ending_time = models.CharField(max_length=50)
    
    # Descriptive Fields
    duration_desc = models.CharField(max_length=255) # e.g., "Full Day Stay"
    amenities = models.TextField() # e.g., "WiFi, Pool, Breakfast"
    
    # Pricing
    price_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.hotel_name} - Room {self.room_number}"

    class Meta:
        db_table = 'hotel' # Links to your specific database table name

# 5. Itinerary Model
class Itinerary(models.Model):
    # If your database column is 'package_id', you must set primary_key=True
    package_id = models.AutoField(primary_key=True) 
    package_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'itinerary' # Ensures it points to the 'itinerary' table
        
# 6. Transport Model
class Transport(models.Model):
    transport_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'transport'
        
    