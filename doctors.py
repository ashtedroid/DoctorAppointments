'''
Class object to hold the data
'''
from random import randint

class DoctorData(object):
    """Holds all data and provides fucntions for the REST requests"""
    def __init__(self):
        '''
        Adding sample doctors
        '''
        self.doctors = dict() # Key: Doc_ID Value: Doctor()
        self.add_doctor('John', 'Doe')
        self.add_doctor('Jane', 'Doe')

    def add_doctor(self, first_name, last_name):
        doc_id = randint(1, 9999)
        self.doctors[doc_id] = Doctor(first_name, last_name)

    def get_doctors(self):
        #print self.doctors
        return [{doc[0]: {"first_name": doc[1].first_name, "last_name":doc[1].last_name}} for doc in self.doctors.items()]

    def add_appointment(self, json_data):
        '''
        Assuming a valid doctor and a date is already selected in the GUI before requesting a new appointment.

        '''
        doctor = self.doctors[int(json_data['doc_id'])]
        date = json_data['date']
        time = json_data['time']
        apt_id = randint(1, 9999)
        apt_data = [json_data["patient_first_name"],
                    json_data["patient_last_name"],
                    json_data["date"],
                    json_data["time"],
                    json_data["kind"]]
        return doctor.add_appointment(date, time, apt_id, apt_data)

    def get_appointments(self, doc_id, date):
        '''
        Assuming a valid doctor and a date is already selected in the GUI before requesting a new appointment.

        '''
        if doc_id not in self.doctors:
            return []
        doctor = self.doctors[int(doc_id)]
        appointments = doctor.get_appointments(date)
        return [ {str(appointment[0]):str(appointment[1])} for appointment in appointments.items()]

    def del_appointment(self, doc_id, date, apt_id):
        '''
        Assuming a valid doctor, date and an appointment is already selected in the GUI before requesting a new appointment.
        '''
        if doc_id not in self.doctors:
            return "No such doctor."
        doctor = self.doctors[int(doc_id)]
        return doctor.del_appointment(date, apt_id)
         

class Doctor(object):
    """Data structure to hold doctor data"""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.dates = dict() # Key: Date Value: DateInfo()

    def add_appointment(self, date, time, apt_id, apt_data):
        '''
        Retrieve Date Info for the particular date for the doctor and add appointment 
        '''
        # If New date
        if date not in self.dates:
            self.dates[date] = DateInfo()
        date_info = self.dates[date]
        return date_info.add_appointment(time, apt_id, apt_data)

    def get_appointments(self, date):
        if date not in self.dates:
            return {}
        return self.dates[date].get_appointments()

    def del_appointment(self, date, apt_id):
        if date not in self.dates:
            return "No such date."
        date_info = self.dates[date]
        return date_info.del_appointment(apt_id)
        

class DateInfo(object):
    """docstring for DateInfo"""
    def __init__(self):
        self.appointments = dict() # Key: Appointment_ID Value: Appointment()
        self.booked = dict() # Key: Time Value: True

    def __str__(self):
        return str([str(appointment) for appointment in self.appointments.items()]) + str(self.booked.items())

    def add_appointment(self, time, apt_id, apt_data):
        if time not in self.booked:
            self.booked[time] = True
            self.appointments[int(apt_id)] = Appointment(*apt_data)
            return "Appointment booked."
        else:
            return "Appointment not successful. The slot is already booked."
    def get_appointments(self):
        return self.appointments

    def del_appointment(self, apt_id):
        if apt_id not in self.appointments:
            return "No such appointment to delete."
        apt_time = self.appointments[int(apt_id)].time
        del self.appointments[int(apt_id)]
        del self.booked[apt_time]
        return "Appointment deleted."

class Appointment(object):
    """docstring for Appointment"""
    def __init__(self, patient_first_name, patient_last_name, date, time, kind):
        self.patient_first_name = patient_first_name
        self.patient_last_name = patient_last_name
        self.date = date
        self.time = time
        self.kind = kind
    
    def __str__(self):
        return str(self.__dict__)
