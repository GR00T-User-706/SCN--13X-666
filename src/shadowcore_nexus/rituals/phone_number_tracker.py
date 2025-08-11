import phonenumbers
from phonenumbers import carrier, geocoder
from tkinter import Tk, Label, Button, Entry, StringVar, OptionMenu
import argparse
import sys

# Supported country options - you can expand this list or dynamically load
COUNTRIES = {
    'US': 'United States',
    'GB': 'United Kingdom',
    'CA': 'Canada',
    'IN': 'India',
    'AU': 'Australia',
    'FR': 'France',
    'IT': 'Italy',
    'RO': 'Romania',
    'CH': 'Switzerland',
    # You can add more as needed
    }

class Track:
    def __init__(self, App):    
        self.window = App
        self.window.title("Phone number Tracker")
        self.window.geometry("600x400")
        self.window.configure(bg="#2f2212")
        self.window.resizable(True, True)  
        
        Label(App, text="Enter the phone number", fg="orange", font=("Times", 20), bg="#3f5edb").place(x=180, y=30)
        self.mobile_number = Entry(App, width=20, font=("Arial", 15), relief="flat")
        self.mobile_number.place(x=200, y=80)
        
        # Country Code Dropdown
        Label(App, text="Select country/region:", fg="orange", font=("Times", 16), bg="#3f5edb").place(x=190, y=130)
        self.selected_country = StringVar(App)
        self.selected_country.set('US') # default
        country_names = [f"{code} - {name}" for code, name in COUNTRIES.items()]






                         
        self.trackingbutton = Button(App, text="To track the number click here", bg="#22c6c3", relief="sunken", command=self.Track_THE_location)
        self.trackingbutton.place(x=200, y=200)
        
        self.countryname = Label(App, fg="white", font=("Times", 20), bg="#3f5efb")
        self.countryname.place(x=100, y=280) 
        
        self.countryname2 = Label(App, fg="white", font=("Times", 20), bg="#3f5efb")    
        self.countryname2.place(x=300, y=280)
               
    def Track_THE_location(self):    
        phone_number = self.mobile_number.get()
        if phone_number:
            try:
                tracked = phonenumbers.parse(phone_number, "US")
                if not phonenumbers.is_valid_number(tracked):
                    self.countryname.config(text="Invalid US phone number")
                    self.countryname2.config(text="")
                    return

                carrier_name = carrier.name_for_number(tracked, "en")
                location = geocoder.description_for_number(tracked, "en")

                self.countryname.config(text=carrier_name if carrier_name else "Unknown carrier")
                self.countryname2.config(text=location if location else "Unknown location")

            except phonenumbers.NumberParseException:
                self.countryname.config(text="Invalid phone number format")
                self.countryname2.config(text="")

PhoneTracking = Tk()
MyApp = Track(PhoneTracking)

PhoneTracking.mainloop()



    
    
        
            
            
                
                

            

            
        
