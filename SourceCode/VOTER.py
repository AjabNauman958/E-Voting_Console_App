"""" Imports:
            1. ADMIN Package.
            2. REGISTRATION Package
            3. PARTY_LEADER"""

class Voter:
    voter_cnic = ""
    voters_dictionary = {}  # To store Voters details
    districts_dictionary = {}  # To store candidates id's that are in specific district

    def __init__(self):
        pass

    @staticmethod
    def voter_menu(cnic_number):
        from PARTY_LEADER import PartyLeader
        from REGISTRATION import Registration
        from ADMIN import Admin
        try:
            Voter.voter_cnic = cnic_number
            while True:
                print("\n\n\t\t\t   Voter Menu")
                print("\t\t\t----------------")
                print("\n\t\t1. Cast Vote")
                print("\t\t2. Update Personal Details")
                print("\t\t3. View Results")
                print("\t\t4. Go Back")

                choice = input("\n\tEnter your choice: ")

                user_district = Voter.voters_dictionary[cnic_number]["district_name"]
                if choice == "1":
                    Voter.cast_vote(user_district, cnic_number, PartyLeader, Admin)
                elif choice == "2":
                    Voter.update_personal_details(cnic_number, Registration)
                elif choice == "3":
                    Voter.view_results()
                elif choice == "4":
                    break
                else:
                    print("\n\tInvalid choice. Please try again.")
        except ValueError:
            return

    # Login through correct cnic and password
    @staticmethod
    def login_as_voter(Registration):
        try:
            break_loop = True
            while break_loop:
                print("\n\n\t\t\t   Login as Voter")
                print("\t\t\t--------------------")
                cnic_number = input("\n\t\tCNIC Number(Without dashes: ")
                user_password = input("\t\tPassword: ")
                if cnic_number in Voter.voters_dictionary:
                    if Registration.user_credentials[cnic_number] == user_password:
                        Voter.voter_menu(cnic_number)
                        break_loop = False
                else:
                    print("\n\n\t\tInvalid credentials.")
                    user_choice = input("\n\t\tPress 'l' for logout or 't' for try again.").lower()
                    if user_choice == "l":
                        break_loop = False
        except ValueError:
            return

    # Fill Candidates District Dictionary which store district wise candidates id's
    @staticmethod
    def fill_district_dictionary(PartyLeader):
        for key, value in PartyLeader.candidates_dictionary.items():
            district = value.get("district_name")
            if district:
                if district in Voter.districts_dictionary:
                    Voter.districts_dictionary[district].append(key)
                else:
                    Voter.districts_dictionary[district] = [key]

    # cast vote through voter cnic.
    @staticmethod
    def cast_vote(user_district, cnic_number, PartyLeader, Admin):
        import pandas as pd
        from tabulate import tabulate
        try:
            if Admin.voting_started:
                if Voter.voters_dictionary[cnic_number]["voted"]:
                    input("You already voted. Press any key to go back: ")
                    return
                # All District wise candidates
                Voter.fill_district_dictionary(PartyLeader)
                if user_district not in Voter.districts_dictionary:
                    input("\n\tNo candidate in your district.\n\tPress any key to go back: ")
                    return
                # Extract voter district candidates id's as a list
                candidates_in_user_district = Voter.districts_dictionary[user_district]
                if not candidates_in_user_district:
                    print("\n\tNo candidates available in your district.")
                else:
                    candidates_in_user_district_details = {}
                    # Extract candidates details of voter district
                    candidates_in_user_district_details = Voter.fill_voter_district_candidates(candidates_in_user_district_details, candidates_in_user_district, PartyLeader)
                    # Display candidates details
                    df = pd.DataFrame(candidates_in_user_district_details)
                    print(tabulate(df.T, headers="keys"))
                    print()
                    while True:
                        candidate_id = input("\n\tEnter the candidate ID to cast your vote: ")
                        # Update results based on candidate id in user_district_dictionary
                        is_vote_casted = Voter.update_resullts_dictionary(cnic_number, candidate_id, candidates_in_user_district_details, Admin, PartyLeader)
                        if is_vote_casted:
                            print("\n\tVote cast successfully!")
                            break
                        else:
                            print("\n\tInvalid candidate ID.")
            else:
                print("\n\t\tVoting not started yet.")
            input("\n\tPress any key to go back: ")
        except ValueError:
            return

    # Update results dic based on candidate id
    @staticmethod
    def update_resullts_dictionary(cnic_number, candidate_id, candidates_in_user_district_details, Admin, PartyLeader):
        if candidate_id in candidates_in_user_district_details:
            Admin.all_results_dictionary[candidate_id] = {
                "Candidate_Name": PartyLeader.candidates_dictionary[candidate_id]["full_name"],
                "Candidate_Party": PartyLeader.candidates_dictionary[candidate_id]["party_name"],
                "Candidate_District": PartyLeader.candidates_dictionary[candidate_id]["district_name"],
                "Candidate_Votes": 0
                }
            Admin.all_results_dictionary[candidate_id]["Candidate_Votes"] += 1
            Voter.voters_dictionary[cnic_number]["voted"] = True
            return True
        else:
            return False

    # All details of voter district candidates
    @staticmethod
    def fill_voter_district_candidates(candidates_in_user_district_details, candidates_in_user_district, PartyLeader):
        for candidates in candidates_in_user_district:
            candidates_in_user_district_details[candidates] = {"Name": PartyLeader.candidates_dictionary[candidates]["full_name"],
                                                               "Party Name": PartyLeader.candidates_dictionary[candidates]["party_name"],
                                                               "Party Symbol": PartyLeader.parties_dictionary[PartyLeader.candidates_dictionary[candidates]["party_name"]]["party_symbol"]
                                                               }
        return candidates_in_user_district_details
    
    @staticmethod
    def update_personal_details(cnic_number, Registration):
        print("\n\n\t\t   Update Personal Details")
        print("\t\t-----------------------------")
        while True:
            print("\n\tWhat do you want to update?")
            print("\n\t\t1. Phone Number")
            print("\t\t2. Email Address")
            print("\t\t3. Password")
            print("\t\t4. Go Back")
            user_choice = input("\n\tEnter your choice: ")
            print()

            try:
                if user_choice == "1":
                    update_phone_number = Registration.set_phone_number()
                    Voter.voters_dictionary[cnic_number]["phone_number"] = update_phone_number
                    print("\n\t\tPhone Number updated successfully!")
                elif user_choice == "2":
                    Update_Email = Registration.set_Email()
                    Voter.voters_dictionary[cnic_number]["Email"] = Update_Email
                    print("\n\t\tEmail updated successfully!")
                elif user_choice == "3":
                    print("\n Enter new Credentials.")
                    update_password = Registration.set_password()
                    Registration.user_credentials[cnic_number] = update_password
                    print("\n\t\tPassword updated successfully!")
                elif user_choice == "4":
                    break
                else:
                    print("\n\t\tEnter Invalid choice. Try again.")
            except ValueError:
                Voter.voter_menu(cnic_number)
        print("\n\t\tPersonal details updated successfully!")

    # Display all district results
    @staticmethod
    def view_results():
        import pandas as pd
        from tabulate import tabulate
        from ADMIN import Admin
        print("\n\n\t\t   Election Results ")
        print("\t\t----------------------")
        if not Admin.all_results_dictionary:
            print("\n\tNo Results available.")
        else:
            try:
                df = pd.DataFrame(Admin.all_results_dictionary)
                print(tabulate(df.T, headers="keys"))
            except ValueError:
                return
