"""" Imports:
            1. ADMIN Package.
            2. VOTER Package
            3. PARTY_LEADER"""


class Registration:
    user_credentials = {}  # Dictionary to store user credentials

    def __init__(self):
        pass

    # To set Voter/Candidate/Part Leader Details
    @staticmethod
    def register_voter():
        try:
            print("\n\n\t\t\t   Voter Registration")
            print("\t\t\t------------------------")
            cnic_number = Registration.set_CNIC()
            full_name = Registration.set_name()
            gender = Registration.set_gender()
            date_of_birth = Registration.set_date_of_birth()
            phone_number = Registration.set_phone_number()
            Email = Registration.set_Email()
            district_name = Registration.set_district()
            user_password = Registration.set_password()

            while True:
                is_party_leader = input("\n\n\tAre you a party leader? Yes/No: ").lower()
                if is_party_leader == "yes":
                    # Sent party registration request to admin for approval
                    Registration.request_party_registration(cnic_number, full_name)
                    # Save all party leader details in party leaders Dictionary
                    Registration.save_party_leader_details(cnic_number, full_name, gender, date_of_birth, phone_number, Email, district_name)
                    # Save all party leader details as a voter in voters Dictionary
                    Registration.save_voter_details(cnic_number, full_name, gender, date_of_birth, phone_number, Email, district_name)
                    break
                elif is_party_leader == "no":
                    # Save all voter details in voters Dictionary
                    Registration.save_voter_details(cnic_number, full_name, gender, date_of_birth, phone_number, Email, district_name)
                    break
                else:
                    print("\n\t\tInvalid input.")

            # Save user password in user credentials list
            Registration.user_credentials[cnic_number] = user_password
            print("\tRegistration Completed Successfully!")
            input("\tPress any key to go back: ")
        except ValueError:
            return

    # Save voter details in voter dict
    @staticmethod
    def save_voter_details(cnic_number, full_name, gender, date_of_birth, phone_number, Email, district_name):
        from VOTER import Voter
        # Save all voter details in voters Dictionary
        Voter.voters_dictionary[cnic_number] = {"full_name": full_name, "gender": gender,
                                                "date_of_birth": date_of_birth, "phone_number": phone_number,
                                                "Email": Email, "district_name": district_name,
                                                "voted": False}

    # Save Party leader details in party leader dict
    @staticmethod
    def save_party_leader_details(cnic_number, full_name, gender, date_of_birth, phone_number, Email, district_name):
        from PARTY_LEADER import PartyLeader
        PartyLeader.party_leaders_list[cnic_number] = {"full_name": full_name, "gender": gender,
                                                       "date_of_birth": date_of_birth, "phone_number": phone_number,
                                                       "Email": Email, "district_name": district_name,
                                                       "voted": False, "party_name": ""}

    @staticmethod
    def request_party_registration(cnic_number, party_leader_name):
        from ADMIN import Admin
        request_id = cnic_number
        print("\n\tPlease register your party first.")
        print("\t\t   Party Registration")
        print("\t\t   ---------------------")
        party_name = input("\n\tParty name: ")
        party_motto = input("\tParty motto: ")
        part_symbol = input("\tParty symbol: ")
        Admin.party_approval_requests[request_id] = {
            "party_name": party_name,
            "party_symbol": part_symbol,
            "party_motto": party_motto,
            "party_leader": party_leader_name
        }
        print("\n\n\tParty registration request sent to admin for approval.")

    @staticmethod
    def set_CNIC():
        from VOTER import Voter
        while True:
            cnic_number = input('CNIC number (without dashes): ')
            if len(cnic_number) != 13:
                print("\n\tInvalid length of CNIC Number.!\n")
            elif not cnic_number.isnumeric():
                print("\n\tCNIC Number should be number.!\n")
            elif cnic_number in Voter.voters_dictionary:
                print("\n\tCNIC Already Registered.\n")
            else:
                return cnic_number

    @staticmethod
    def set_name():
        while True:
            full_name = input("Full Name: ").upper()
            if full_name.isalpha():
                return full_name
            else:
                print("\n\tName can only contain characters!\n")

    @staticmethod
    def set_gender():
        while True:
            gender = input("Gender(Male/Female/Other): ").lower()
            if gender == 'male' or gender == 'female' or gender == 'other':
                return gender
            else:
                print("\nPlease enter valid input!\n")

    @staticmethod
    def set_date_of_birth():
        from datetime import datetime
        while True:
            date_of_birth = input("Date of birth(YYYY-MM-DD): ")
            date_format = "%Y-%m-%d"
            is_valid_date = True
            try:
                birth_date = datetime.strptime(date_of_birth, date_format)
            except ValueError:
                is_valid_date = False

            if is_valid_date:
                today = datetime.today()
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                    return age
                if age < 18:
                    print("\nYou are not eligible to vote. Sorry!\n")
                    print("Bye!")
                    input("Press any key to go back to main menu: ")
                    from MAIN_DASHBOARD import Dashboard
                    Dashboard.main_menu()
                return date_of_birth
            else:
                print("\n\tThis is incorrect format. It should be YYYY-MM-DD\n")

    @staticmethod
    def set_phone_number():
        while True:
            phone_number = input("Phone Number(without dash like 03000000001): ")
            if len(phone_number) != 11:
                print("\n\tInvalid length of Phone no.!\n")
            elif phone_number.isnumeric():
                return phone_number
            else:
                print("\n\tPhone Number can only contain numbers!\n")

    @staticmethod
    def set_Email():
        while True:
            Email = input("Email address: ")
            if ('@' and '.' in Email) and (Email.index("@") < Email.index(".") and (Email.index(".") < len(Email) - 1)):
                return Email
            else:
                print("\n\tInvalid Email Id!\n")

    @staticmethod
    def set_district():
        while True:
            district_name = input("Enter District Name: ")
            if district_name == "":
                print("Please enter valid district name\n")
                continue
            return district_name

    @staticmethod
    def set_password():
        while True:
            password = input("Password: ")
            confirm_password = input("Confirm password: ")
            if confirm_password == password:
                return password
            else:
                print("\n\tPassword doesn't match! Enter again!\n")
