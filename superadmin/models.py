from decimal import Decimal
from django.db import models
# models.py
from djongo import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('quality', 'Quality'),
        ('telecaller', 'Telecaller'),
        ('distributer', 'Distributer'),
        ('rescue', 'Rescue'),
        ('hr', 'HR'),
        ('driver', 'Driver'),  # Added driver type
        ('author','Author'),

    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    profile_id = models.AutoField(primary_key=True)  # Added primary key field
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed to ForeignKey
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    company_format = models.CharField(max_length=255, unique=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='profile_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='profile_updated', on_delete=models.SET_NULL, null=True, blank=True)

class ProfileHistory(models.Model):
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('quality', 'Quality'),
        ('telecaller', 'Telecaller'),
        ('distributer', 'Distributer'),
        ('rescue', 'Rescue'),
        ('hr', 'HR'),
        ('driver', 'Driver') ,
        ('author','Author'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    profile_id = models.IntegerField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed to ForeignKey
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    company_format = models.CharField(max_length=255, blank=True)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True) 
    updated_by = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return f"History for profile_id {self.profile_id} on {self.updated_on}"

#######################################################################################################################################

class VehicleType(models.Model):
    vehicle_type_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=10, unique=True, blank=True)
    vehicle_type_name = models.CharField(max_length=100) 
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='vehicletypes_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='vehicletypes_updated', on_delete=models.SET_NULL, null=True, blank=True) 

class VehicleTypeHistory(models.Model):
    vehicle_type_id = models.IntegerField()
    company_format = models.CharField(max_length=10, blank=True)
    vehicle_type_name = models.CharField(max_length=100) 
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return f"History for vehicle_type_id {self.vehicle_type_id}"
    
#######################################################################################################################################

class Ridetype(models.Model):
    ridetype_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=100, unique=True, blank=True)
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='ridetypes_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='ridetypes_updated', on_delete=models.SET_NULL, null=True, blank=True)

class RidetypeHistory(models.Model):
    ridetype_id = models.IntegerField()
    company_format = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=100)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"History for ridetype_id {self.ridetype_id} on {self.updated_on}"
    
#######################################################################################################################################

class Category(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    seats = models.IntegerField()
    image = models.ImageField(upload_to='documents',null=True)
    category_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='categories_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='categories_updated', on_delete=models.SET_NULL, null=True, blank=True)

class CategoryHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    category_id = models.IntegerField()
    category_name = models.CharField(max_length=100)
    seats = models.IntegerField()
    image = models.ImageField(upload_to='documents',null=True)
    category_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return f"History for category_id {self.category_id} on {self.updated_on}"
    

#######################################################################################################################################

class Brand(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    brand_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='brands', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='brands_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='brands_updated', on_delete=models.SET_NULL, null=True, blank=True)

class BrandHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    brand_id = models.IntegerField()
    category = models.ForeignKey(Category, related_name='brands_history', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"History for brand_id {self.brand_id} on {self.updated_on}"
    
#######################################################################################################################################

class Model(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    model_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand,related_name='models', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    # price_per_kms = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True) 
    created_by = models.ForeignKey(User, related_name='models_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='models_updated', on_delete=models.SET_NULL, null=True, blank=True)


class ModelHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    model_id = models.IntegerField()
    brand = models.ForeignKey(Brand, related_name='models_history', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    # price_per_kms = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"History for model_id {self.model_id} on {self.updated_on}"
    
#  Transmission ###########################################   

class Transmission(models.Model):
    transmission_id = models.AutoField(primary_key=True)
    transmission_name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='transmission_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='transmission_updated', on_delete=models.SET_NULL, null=True, blank=True)

class TransmissionHistory(models.Model):
    transmission_id = models.IntegerField()
    transmission_name = models.CharField(max_length=100)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"History for transmission_id {self.transmission_id} on {self.updated_on}" 

# color #####################################################################
class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='color_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='color_updated', on_delete=models.SET_NULL, null=True, blank=True)

class ColorHistory(models.Model):
    color_id = models.IntegerField()
    name = models.CharField(max_length=100)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return f"History for color_id {self.color_id} on {self.updated_on}"       


#######################################################################################################################################

class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    customer_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=10, unique=True, blank=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=128)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    block_reason = models.CharField(max_length=1000,null=True)
    total_rides = models.IntegerField(default=0) 
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='customers_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='customers_updated', on_delete=models.SET_NULL, null=True, blank=True)

class CustomerHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    customer_id = models.IntegerField()
    company_format = models.CharField(max_length=10, blank=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=128)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    block_reason = models.CharField(max_length=1000,null=True)
    total_rides = models.IntegerField(default=0,null=True)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)


    def _str_(self):
        return f"History for customer_id {self.customer_id} on {self.updated_on}"
    
#######################################################################################################################################

class VehicleOwner(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]

    owner_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    image = models.ImageField(upload_to='documents',null=True)
    address_proof = models.ImageField(upload_to='documents',null=True)
    identity = models.ImageField(upload_to='documents',null=True)  # Changed to FileField for general file types
    holdername = models.CharField(max_length=100)
    ac_number = models.CharField(max_length=100)
    bankname = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    block_reason = models.CharField(max_length=1000,null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='vehicleowners_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='vehicleowners_updated', on_delete=models.SET_NULL, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

class VehicleOwnerHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]

    owner_id = models.IntegerField()
    company_format = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    image = models.ImageField(upload_to='documents',null=True)
    address_proof = models.ImageField(upload_to='documents',null=True)
    identity = models.ImageField(upload_to='documents',null=True)  # Changed to FileField for general file types
    holdername = models.CharField(max_length=100)
    ac_number = models.CharField(max_length=100)
    bankname = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    block_reason = models.CharField(max_length=1000,null=True)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

    def _str_(self):
        return f"History for owner_id {self.owner_id} on {self.updated_on}"
    

#######################################################################################################################################
    
class CommissionType(models.Model):
    commission_id = models.AutoField(primary_key=True)
    commission_name = models.CharField(max_length=1000)
    commission_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='commission_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='commission_updated', on_delete=models.SET_NULL, null=True, blank=True)


class CommissionHistory(models.Model):
    commission_id = models.IntegerField()
    commission_name = models.CharField(max_length=1000)
    commission_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return f"History for commission_id {self.commission_id} on {self.updated_on}"
    
#######################################################################################################################################


class Vehicle(models.Model):
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]
    
    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]
    DRIVE_STATUS = [
    ('selfdrive', 'selfdrive'),
    ('otherdrive', 'otherdrive'),
    ]

    vehicle_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=10, unique=True, blank=True)
    Vehicle_Number = models.CharField(max_length=10, unique=True)
    model = models.ForeignKey(Model, related_name='vehicles', on_delete=models.CASCADE)
    year = models.CharField(max_length=500)
    insurance_expiry = models.DateField()
    car_type = models.CharField(max_length=500)
    registration_certificate = models.ImageField(upload_to='documents',null=True,blank=True)
    fc_certificate = models.ImageField(upload_to='documents',null=True)
    insurance_policy = models.ImageField(upload_to='documents',null=True)
    tax_details = models.ImageField(upload_to='documents',null=True)
    permit_details = models.ImageField(upload_to='documents',null=True)
    emission_test = models.ImageField(upload_to='documents',null=True)
    owner = models.ForeignKey(VehicleOwner, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)  
    commission_type = models.ForeignKey(CommissionType, on_delete=models.CASCADE,null=True)  
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True)  
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE,null=True)  
    vehicle_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    block_reason = models.CharField(max_length=1000,null=True)
    drive_status = models.CharField(max_length=50, choices=DRIVE_STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='vehicles_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='vehicles_updated', on_delete=models.SET_NULL, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

class VehicleHistory(models.Model):
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]
    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]
    DRIVE_STATUS = [
    ('selfdrive', 'selfdrive'),
    ('otherdrive', 'otherdrive'),
    ]

    vehicle_id = models.IntegerField()
    company_format = models.CharField(max_length=10, blank=True)
    Vehicle_Number = models.CharField(max_length=10, blank=True)
    model = models.ForeignKey(Model, related_name='vehicles_history',on_delete=models.CASCADE)
    year = models.CharField(max_length=500)
    insurance_expiry = models.DateField()
    car_type = models.CharField(max_length=500)
    registration_certificate = models.ImageField(upload_to='documents',null=True)
    fc_certificate = models.ImageField(upload_to='documents',null=True)
    insurance_policy = models.ImageField(upload_to='documents',null=True)
    tax_details = models.ImageField(upload_to='documents',null=True)
    permit_details = models.ImageField(upload_to='documents',null=True)
    emission_test = models.ImageField(upload_to='documents',null=True)
    owner = models.ForeignKey(VehicleOwner, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE) 
    commission_type = models.ForeignKey(CommissionType, on_delete=models.CASCADE,null=True) 
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True)  
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE,null=True)   
    vehicle_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    block_reason = models.CharField(max_length=1000,null=True)
    drive_status = models.CharField(max_length=50, choices=DRIVE_STATUS)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"History for vehicle_id {self.vehicle_id} on {self.updated_on}"
    

#######################################################################################################################################

class Driver(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    DRIVER_STATUS_CHOICES = [
        ('free', 'Free'),
        ('occupied', 'Occupied'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]

    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=15,null=True)
    address = models.TextField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    company_format = models.CharField(max_length=10, unique=True, blank=True)
    profile_image = models.ImageField(upload_to='documents',null=True)  
    address_proof = models.ImageField(upload_to='documents',null=True)  
    police_clearance = models.ImageField(upload_to='documents',null=True)  
    pfrom_date = models.DateField(null=True)
    pto_date = models.DateField(null=True)
    driving_license = models.ImageField(upload_to='documents',null=True)  
    dfrom_date = models.DateField(null=True)
    dto_date = models.DateField(null=True)
    driver_status = models.CharField(max_length=20, choices=DRIVER_STATUS_CHOICES, default='free')
    block_reason = models.CharField(max_length=255,null=True)
    number_of_rides = models.IntegerField(default=0,null=True) 
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True) 
    created_by = models.ForeignKey(User, related_name='drivers_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='drivers_updated', on_delete=models.SET_NULL, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

class DriverHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    DRIVER_STATUS_CHOICES = [
        ('free', 'Free'),
        ('occupied', 'Occupied'),
    ]

    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]
    driver_id = models.IntegerField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=15,null=True)
    address = models.TextField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Driver.STATUS_CHOICES)
    company_format = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='documents',null=True)  
    address_proof = models.ImageField(upload_to='documents',null=True)  
    police_clearance = models.ImageField(upload_to='documents',null=True)  
    pfrom_date = models.DateField(null=True)
    pto_date = models.DateField(null=True)
    driving_license = models.ImageField(upload_to='documents',null=True)  
    dfrom_date = models.DateField(null=True)
    dto_date = models.DateField(null=True) 
    driver_status = models.CharField(max_length=20, choices=DRIVER_STATUS_CHOICES, default='free')
    block_reason = models.CharField(max_length=255,null=True)
    number_of_rides = models.IntegerField(null=True) 
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)  # Timestamp of when the history record was created
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')
    verified_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"History for driver_id {self.driver_id} on {self.updated_on}"    
    
############################################################################################################

class Pricing(models.Model):
    STATUS_CHOICES = [
    ('12AM - 6AM', '12AM - 6AM'),
    ('6AM - 12PM', '6AM - 12PM'),
    ('12PM - 6PM','12PM - 6PM'),
    ('6PM - 12AM','6PM - 12AM'),
    ]

    TRIP_CHOICES = [
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
    ]

    pricing_id = models.AutoField(primary_key=True)
    ridetype = models.ForeignKey(Ridetype, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slots = models.CharField(max_length=50, choices=STATUS_CHOICES)
    driver_beta = models.DecimalField(max_digits=5, decimal_places=2)
    toll_price = models.DecimalField(max_digits=5, decimal_places=2)
    permit = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=5, decimal_places=2)
    car_type = models.CharField(max_length=10)
    trip_type = models.CharField(max_length=10, choices=TRIP_CHOICES, null=True, blank=True)  # New field
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='pricing_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='pricing_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # class Meta:
    #     unique_together = ('category', 'ridetype', 'car_type')

class PricingHistory(models.Model):
    STATUS_CHOICES = [
    ('12AM - 6AM', '12AM - 6AM'),
    ('6AM - 12PM', '6AM - 12PM'),
    ('12PM - 6PM','12PM - 6PM'),
    ('6PM - 12AM','6PM - 12AM'),
    ]

    TRIP_CHOICES = [
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
    ]
    pricing_id = models.IntegerField()
    ridetype = models.ForeignKey(Ridetype, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slots = models.CharField(max_length=50, choices=STATUS_CHOICES)
    driver_beta = models.DecimalField(max_digits=5, decimal_places=2)
    toll_price = models.DecimalField(max_digits=5, decimal_places=2)
    permit = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=5, decimal_places=2)
    car_type = models.CharField(max_length=10)
    trip_type = models.CharField(max_length=10, choices=TRIP_CHOICES, null=True, blank=True)  # New field
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"History for pricing_id {self.pricing_id} on {self.updated_on}" 
    
#######################################################################################################################################

class RideDetails(models.Model):
    STATUS_CHOICES = [
    ('currentbookings', 'currentbookings'),
    ('assignbookings', 'assignbookings'),
    ('ongoingbookings','ongoingbookings'),
    ('completedbookings','completedbookings'),
    ('advancebookings','advancebookings'),
    ('pendingbookings','pendingbookings'),
    ('cancelledbookings','cancelledbookings'),
    ('assignlaterbookings', 'assignlaterbookings'),

]
    ride_id = models.AutoField(primary_key=True)
    company_format = models.CharField(max_length=100, unique=True, blank=True)
    pricing = models.ForeignKey(Pricing,on_delete=models.CASCADE,null=True)
    ridetype = models.ForeignKey(Ridetype,on_delete=models.CASCADE)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    assigned_by = models.ForeignKey(User, related_name='assigned_by', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_on = models.DateTimeField(auto_now=True)
    cancelled_by = models.ForeignKey(User, related_name='cancelled_by', on_delete=models.SET_NULL, null=True, blank=True)
    cancelled_on = models.DateTimeField(auto_now=True)
    total_fare = models.IntegerField()    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customer_notes = models.CharField(max_length=100,null=True)
    ride_status = models.CharField(max_length=50, choices=STATUS_CHOICES,null=True)
    quality_comments = models.CharField(max_length=1000,null=True)
    verified_by = models.ForeignKey(User, related_name='verified_by', on_delete=models.SET_NULL, null=True, blank=True)
    verified_on = models.DateTimeField(auto_now=True)
    booking_datetime = models.DateTimeField(auto_now_add=True)
    bookings_from = models.CharField(max_length=100,null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='rides_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='rides_updated', on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.CharField(max_length=1000,null=True)
    drop_date = models.DateField(null=True)
    drop_time = models.TimeField(null=True)

class RideDetailsHistory(models.Model):
    STATUS_CHOICES = [
    ('currentbookings', 'currentbookings'),
    ('assignbookings', 'assignbookings'),
    ('ongoingbookings','ongoingbookings'),
    ('pendingbookings','pendingbookings'),
    ('completedbookings','completedbookings'),
    ('advancebookings','advancebookings'),
    ('cancelledbookings','cancelledbookings'),
    ('assignlaterbookings', 'assignlaterbookings'),

]
    ride_id = models.IntegerField()
    company_format = models.CharField(max_length=100, unique=True, blank=True)
    ridetype = models.ForeignKey(Ridetype,on_delete=models.CASCADE)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    assigned_by = models.CharField(max_length=100, null=True, blank=True)
    assigned_on = models.DateTimeField(auto_now=True)
    cancelled_by = models.CharField(max_length=100, null=True, blank=True)
    cancelled_on = models.DateTimeField(auto_now=True)
    total_fare = models.IntegerField()    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customer_notes = models.CharField(max_length=100,null=True)
    ride_status = models.CharField(max_length=50, choices=STATUS_CHOICES,null=True)
    quality_comments = models.CharField(max_length=1000,null=True)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_on = models.DateTimeField(auto_now=True)
    booking_datetime = models.DateTimeField(auto_now_add=True)
    bookings_from = models.CharField(max_length=100,null=True)
    created_on = models.DateField()
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=1000,null=True)
    drop_date = models.DateField(null=True)
    drop_time = models.TimeField(null=True)

    def str(self):
        return f"History for ride_id {self.ride_id} on {self.updated_on}"
    
######################### accounts #######################################    
    
class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    date = models.DateField()
    day_name = models.CharField(max_length=1000)
    vehicle_atm = models.DecimalField(max_digits=50, decimal_places=2)
    tripsheet = models.DecimalField(max_digits=50, decimal_places=2)
    total_credit = models.DecimalField(max_digits=50, decimal_places=2)
    cash_recieved = models.DecimalField(max_digits=50, decimal_places=2)
    balance_bd = models.DecimalField(max_digits=50, decimal_places=2)
    total_balance = models.DecimalField(max_digits=50, decimal_places=2)
    expense = models.DecimalField(max_digits=50, decimal_places=2)
    cash_transfer = models.DecimalField(max_digits=50, decimal_places=2)
    total_expense = models.DecimalField(max_digits=50, decimal_places=2)
    balance = models.DecimalField(max_digits=50, decimal_places=2)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='accounts_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='accounts_updated', on_delete=models.SET_NULL, null=True, blank=True)


class DailyVehicleComm(models.Model):
    comm_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    total_driver_commission = models.DecimalField(max_digits=10, decimal_places=2)
    total_company_commission = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('vehicle', 'date')

class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

class Enquiry(models.Model):
    enquiry_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(max_length=100)
    cust_phone_number = models.CharField(max_length=15)
    cust_email = models.EmailField()
    service = models.TextField()
    cust_message = models.TextField()



class PackageCategories(models.Model):
    package_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 
    created_by = models.ForeignKey(User, related_name='package_category_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='package_category_updated', on_delete=models.SET_NULL, null=True, blank=True)

class PackageCategoriesHistory(models.Model):
    package_category_id = models.IntegerField()
    category_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True) 

class PackageName(models.Model):
    package_name_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 

class PackageNameHistory(models.Model):
    package_name_id = models.IntegerField()
    package_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)     
           

class Packages(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    package_id = models.AutoField(primary_key=True)
    package_category = models.ForeignKey(PackageCategories, on_delete=models.CASCADE) 
    package_name = models.ForeignKey(PackageName, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()
    extra_km = models.CharField(max_length=100)
    extra_charges = models.CharField(max_length=100)
    car_type = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, related_name='packages_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='packages_updated', on_delete=models.SET_NULL, null=True, blank=True)

class PackagesHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    package_id = models.IntegerField()
    package_category = models.ForeignKey(PackageCategories, on_delete=models.CASCADE) 
    package_name = models.ForeignKey(PackageName, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()
    extra_km = models.CharField(max_length=100)
    extra_charges = models.CharField(max_length=100)
    car_type = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) 
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)   

class PackageOrder(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inactive')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_method = models.CharField(max_length=50,null=True)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
class PackageOrderHistory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    order_id = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_method = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pickup_date = models.DateField()
    pickup_time = models.TimeField() 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Blogs(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    blogs_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image_link = models.CharField(max_length=1000, blank=True, null=True)
    facebook = models.CharField(max_length=1000)
    instagram = models.CharField(max_length=1000)
    whatsapp = models.CharField(max_length=1000)
    backlink = models.CharField(max_length=1000)
    related_bloglink = models.CharField(max_length=1000)
    tags = models.CharField(max_length=1000)
    meta_title = models.CharField(max_length=1000)
    meta_description = models.CharField(max_length=1000)
    meta_keywords = models.CharField(max_length=1000)
    h1tag = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_website_blogs')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_website_blogs')


class WebsitePackages(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    webpackage_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    package_category = models.ForeignKey(PackageCategories, on_delete=models.CASCADE)
    description = models.TextField(help_text="Detailed description of the package")
    top_attraction = models.TextField(help_text="Main attractions for this package, e.g., Mysore Palace")
    why_visit = models.TextField(help_text="Reasons to visit the destination")
    package_highlights = models.TextField(help_text="Key highlights of the package")
    image = models.ImageField(upload_to='packages_images/', blank=True, null=True)
    image_link = models.CharField(max_length=1000, blank=True, null=True)
    facebook_link = models.CharField(max_length=1000, blank=True, null=True)
    instagram_link = models.CharField(max_length=1000, blank=True, null=True)
    whatsapp_link = models.CharField(max_length=1000, blank=True, null=True)
    tags = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=1000)
    meta_description = models.CharField(max_length=1000)
    meta_keywords = models.CharField(max_length=1000)
    h1tag = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_website_packages')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_website_packages')
