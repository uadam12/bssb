import string
import random

class Image:
    url = 'applicant.jpg'

class PersonalInformation:
    guardian_name = 'Adam Imam'
    gender = 'Male'
    date_of_birth = '5 May 2000'
    phone_number = '+2349018319720'
    nin = '12345678909'
    bvn = '12345678909'
    place_of_birth = 'Maiduguri'
    lga = 'Maiduguri'
    residential_address = 'Wulari Tashan Kurma opposite police barracks'

class User:
    first_name = 'Usman'
    last_name = 'Adam Imam'
    email = 'uadam12@gmail.com'
    picture = Image()
    personal_info = PersonalInformation()

class Application:
    scholarship = '2020/2021 Scholarship'
    application_id = 'BSSB'+''.join(
        random.choices(
            string.digits, k = 16
        )
    )
    applied_on = '30 June 2023'
    applicant = User()
    # Academic
    institution = 'College of Business and Management Studies Konduga'
    program = 'Undergraduate'
    course_of_study = 'Computer Engineering'
    level = 'Part 3'
    id_number = '2024/2023/AGT/SHM/12345'
    admission_year = '2020'
    graduation_year = '2025'
    
    # Account
    account_bank = 'Guarantee Trust Bank'
    account_name = 'Imam Usman Adam'
    account_number = '0501136346'

    schools_attended = [
        ('School Name', 'Qualification Obtained', 'From Date', 'To Date'),
        ('Kamsulem Junior Day Secondary School', 'JSCE', '2013', '2015'),
        ('Government Colledge Maiduguri Borno State', 'SSCE', '2016', '2029')
    ]
    
    referee_name = 'Adam Imam'
    referee_phone_number = '09012345678'
    referee_occupation = 'Trader'
    
    @property
    def declerations(self):
        return [
            f"I <b><u>{self.applicant.first_name}</u></b> hereby declare that the information provided above is to the best of my knowledge and belief accurate in every details.",
            'If given this scholarship, I will also comply strictly with the Rules and Regulations of the Borno State Scholarship Board.'
        ]
application = Application()