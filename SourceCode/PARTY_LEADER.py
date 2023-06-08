"""" Imports:
            1. REGISTRATION Package
            2. VOTER Package """


class PartyLeader:
    party_leaders_list = {}  # To store Party Leaders details
    candidates_dictionary = {}  # Dictionary to store candidates by district
    parties_dictionary = {}  # Dictionary to store all Parties Details
    candidates_by_party_dictionary = {}  # Dictionary to store candidates id that are related to specific party

    def __init__(self):
        pass

    @staticmethod
    def party_leader_menu(cnic_number):
        from VOTER import Voter
        from REGISTRATION import Registration
        try:
            while True:
                print("\n\n\t\t\t   Party Leader Menu   ")
                print("\t\t\t-----------------------")
                print("\n\t\t1. Update Personal Details")
                print("\t\t2. Add Candidates")
                print("\t\t3. Remove Candidates")
                print("\t\t4. View Party Candidates")
                print("\t\t5. Go Back")

                choice = input("\n\n\tEnter your choice: ")

                party_name = PartyLeader.party_leaders_list[cnic_number]["party_name"]
                if choice == "1":
                    PartyLeader.update_personal_details(cnic_number, Registration)
                elif choice == "2":
                    candidate_voter_id = input("\n\t\tCandidate's voter ID: ")
                    PartyLeader.add_candidate(candidate_voter_id, Voter.voters_dictionary, cnic_number, Registration)
                elif choice == "3":
                    PartyLeader.remove_candidate(PartyLeader.candidates_dictionary, Voter.voters_dictionary, party_name)
                elif choice == "4":
                    PartyLeader.view_candidates(party_name)
                    input("\n\tPress any key to go back: ")
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")
        except ValueError:
            return

    @staticmethod
    def login_as_party_leader(Registration):
        try:
            break_loop = True
            while break_loop:
                print("\n\n\t\t\t   Login as Party Leader")
                print("\t\t\t---------------------------")
                cnic_number = input("CNIC Number: ")
                user_password = input("Password: ")
                party_name = input("Party Name: ")
                if cnic_number in Registration.user_credentials:
                    if party_name in PartyLeader.party_leaders_list[cnic_number]['party_name']:
                        if Registration.user_credentials[cnic_number] == user_password:
                            PartyLeader.party_leader_menu(cnic_number)
                            break
                        else:
                            print("\n\t\tInvalid Password.")
                            user_choice = input("\t\tPress 'l' for logout or 't' for try again.").lower()
                            if user_choice == "l":
                                break_loop = False
                    else:
                        print("\n\t\tParty not registered yet. ")
                        user_registration_choice = input("\n\t\t Do You want to register new party? (YES/NO").lower()
                        if user_registration_choice == "yes":
                            Registration.request_party_registration(cnic_number, PartyLeader.party_leaders_list[cnic_number]["full_name"])
                        user_choice = input("\t\tPress 'l' for logout or 't' for try again.").lower()
                        if user_choice == "l":
                            break_loop = False
                else:
                    print("\n\n\t\tInvalid CNIC.")
                    user_choice = input("\t\tPress 'l' for logout or 't' for try again.").lower()
                    if user_choice == "l":
                        break_loop = False
        except ValueError:
            return

    @staticmethod
    def view_candidates(party_name):
        import pandas as pd
        from tabulate import tabulate
        print("\n\n\t\t   Party Candidates List")
        print("\t\t---------------------------\n")
        if not PartyLeader.candidates_dictionary:
            print("\n\t No Candidate exist yet.")
            return
        else:
            PartyLeader.fill_candidates_by_party_dictionary()
            candidates_in_a_party_list = PartyLeader.candidates_by_party_dictionary[party_name]
            specific_party_candidates = {}
            for candidates in candidates_in_a_party_list:
                specific_party_candidates[candidates] = PartyLeader.candidates_dictionary[candidates]
            df = pd.DataFrame(specific_party_candidates)
            print(tabulate(df.T, headers="keys"))

    @staticmethod
    def fill_candidates_by_party_dictionary():
        for key, value in PartyLeader.candidates_dictionary.items():
            party = value.get("party_name")
            if party:
                if party in PartyLeader.candidates_by_party_dictionary:
                    PartyLeader.candidates_by_party_dictionary[party].append(key)
                else:
                    PartyLeader.candidates_by_party_dictionary[party] = [key]

    @staticmethod
    def update_personal_details(cnic_number, Registration):
        from VOTER import Voter
        print("\n\n\t\t   Update Personal Details")
        print("\t\t-----------------------------")
        while True:
            print("\n\tWhat do you want to update?")
            print("\t\t1. Phone Number")
            print("\t\t2. Email Address")
            print("\t\t3. Password")
            print("\t\t4. Go Back")
            user_choice = input("\n\tEnter your choice: ")
            print()

            try:
                if user_choice == "1":
                    update_phone_number = Registration.set_phone_number()
                    PartyLeader.party_leaders_list[cnic_number]["phone_number"] = update_phone_number
                    Voter.voters_dictionary[cnic_number]["phone_number"] = update_phone_number
                    print("\n\t\tPhone Number updated successfully!")
                elif user_choice == "2":
                    update_Email = Registration.set_Email()
                    PartyLeader.party_leaders_list[cnic_number]["Email"] = update_Email
                    Voter.voters_dictionary[cnic_number]["Email"] = update_Email
                    print("\n\t\tEmail updated successfully!")
                elif user_choice == "3":
                    print("\n Enter new Credentials.")
                    update_password = Registration.set_password()
                    Registration.user_credentials[cnic_number] = update_password
                    print("\n\t\tPassword updated successfully!")
                elif user_choice == "4":
                    break
                else:
                    print("\n\tEnter Invalid choice. Try again.")
            except ValueError:
                return

    @staticmethod
    def add_candidate(candidate_voter_id, voters_list, leader_cnic_number, Registration):
        try:
            while True:
                if candidate_voter_id in voters_list:
                    if candidate_voter_id in PartyLeader.candidates_dictionary:
                        print("\n\t\tCandidate already in the candidates list.")
                        input("\n\tPress any key to go back: ")
                        break
                    else:
                        # Copy all candidates details from voter dict to candidates dict
                        PartyLeader.candidates_dictionary[candidate_voter_id] = voters_list[candidate_voter_id]
                        # Update voter dict against candidate cnic number
                        voters_list[candidate_voter_id]["party_name"] = PartyLeader.party_leaders_list[leader_cnic_number]["party_name"]
                        print("\n\t\tCandidate added Successfully.\n")
                        input("\n\tPress any key to go back: ")
                        break
                else:
                    print("\n\t\tCandidate is not register as voter. \n\tRegister First.")
                    user_choice = input("\n\tDo you want to register?(Yes/No)").lower()
                    if user_choice == "yes":
                        Registration.register_voter()
                        break
                    else:
                        break
        except ValueError:
            return

    @staticmethod
    def remove_candidate(candidates, voters_dictionary, party_name):
        PartyLeader.view_candidates(party_name)
        while True:
            candidate_id = input("\n\tEnter Candidate Id to remove or 'e' to go back: ")
            try:
                if candidate_id in candidates:
                    del PartyLeader.candidates_dictionary[candidate_id]
                    voters_dictionary[candidate_id]["party_name"] = ""
                    PartyLeader.candidates_by_party_dictionary[party_name].remove(candidate_id)
                    print("\n\tCandidate Removed.")
                    break
                elif candidate_id == 'e':
                    break
                else:
                    print("\n\t\tInvalid Candidate ID.\n")
            except ValueError:
                return