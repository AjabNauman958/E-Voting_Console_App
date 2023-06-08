"""" Imports:
            1. VOTER Package
            2. PARTY_LEADER"""
import pandas as pd
from tabulate import tabulate


class Admin:
    voting_started = False
    results_declared = False
    party_approval_requests = {}  # To store part registration requests details
    all_results_dictionary = {}  # Dictionary to store results by district

    def __init__(self):
        pass

    @staticmethod
    def admin_menu():
        from PARTY_LEADER import PartyLeader
        from VOTER import Voter
        try:
            while True:
                print("\n\n\t\t   Admin Menu")
                print("\t\t----------------")
                print("\n\t\t1. Approve Party Registration Requests")
                print("\t\t2. Start Voting")
                print("\t\t3. End Voting")
                print("\t\t4. Declare Results")
                print("\t\t5. View Voters List")
                print("\t\t6. View Party Leaders List")
                print("\t\t7. View Registered Parties List")
                print("\t\t8. View All Candidates List")
                print("\t\t9. View Results")
                print("\t\t10. Go Back")

                user_choice = input("\n\tEnter your choice: ")
                print()
                if user_choice == "10":
                    break
                Admin.action_on_user_choice(user_choice, PartyLeader, Voter)
        except ValueError:
            return

    @staticmethod
    def action_on_user_choice(user_choice, PartyLeader, Voter):
        if user_choice == "1":
            Admin.approve_party_registration_requests(PartyLeader)
        elif user_choice == "2":
            Admin.start_voting()
        elif user_choice == "3":
            Admin.end_voting()
        elif user_choice == "4":
            Admin.declare_results()
        elif user_choice == "5":
            Admin.view_voters_list(Voter)
        elif user_choice == "6":
            Admin.view_party_leaders_list(PartyLeader)
        elif user_choice == "7":
            Admin.view_parties_list(PartyLeader)
        elif user_choice == "8":
            Admin.all_candidates_list(PartyLeader)
        elif user_choice == "9":
            Admin.view_result(Voter)
        else:
            print("\n\t\tInvalid choice. Please try again.")

    @staticmethod
    def login_as_admin():
        try:
            break_loop = True
            while break_loop:
                print("\n\n\t\t\t   Login as Admin")
                print("\t\t\t--------------------")
                user_name = input("\n\t\tUser name: ")
                user_password = input("\t\tPassword: ")
                if user_name == "admin" and user_password == "1234":
                    Admin.admin_menu()
                    break_loop = False
                else:
                    print("\n\n\t\tInvalid credentials.")
                    user_choice = input("\t\tPress 'l' for logout or 't' for try again.").lower()
                    if user_choice == "l":
                        break_loop = False
        except ValueError:
            return

    @staticmethod
    def approve_party_registration_requests(PartyLeader):
        print("\n\n\t\t   Party Approval Requests")
        print("\t\t-----------------------------\n")
        if not Admin.party_approval_requests:
            print("\tNo party registration requests to approve.")
            input("\n\tPress any key to go back: ")
            return

        # Display all parties approval requests
        df = pd.DataFrame(Admin.party_approval_requests)
        print(tabulate(df.T, headers="keys"))

        while True:
            request_id = input("\n\n\tEnter the Request ID to approve or 'e' to exit: ")
            if request_id == 'e':
                return
            try:
                if request_id in Admin.party_approval_requests:
                    # Update Party Leader details that are related to recently approved party
                    party_name = Admin.party_approval_requests[request_id]["party_name"]
                    PartyLeader.party_leaders_list[request_id]["party_name"] = party_name
                    # Update parties_dictionary
                    Admin.add_parties_details(request_id, party_name, PartyLeader)
                    del Admin.party_approval_requests[request_id]
                    print("\tParty registration approved successfully.")
                    if not Admin.party_approval_requests:
                        input("Press any key to go back: ")
                        break
                    else:
                        user_choice = input("Do you want to approve more request? (Yes/No): ")
                        if not user_choice == "yes":
                            break
            except ValueError:
                return
            print("\n\tInvalid Request ID. Please try again.")

    # Fill parties details in parties dictionary
    @staticmethod
    def add_parties_details(request_id, party_name, PartyLeader):
        party_motto = Admin.party_approval_requests[request_id]["party_motto"]
        part_symbol = Admin.party_approval_requests[request_id]["party_symbol"]
        party_leader_name = Admin.party_approval_requests[request_id]["party_leader"]

        # Save Parties details
        PartyLeader.parties_dictionary[party_name] = {"party_symbol": part_symbol,
                                                      "party_motto": party_motto,
                                                      "party_leader": party_leader_name
                                                      }

    @staticmethod
    def start_voting():
        print("\n\n\t\t   Start Voting")
        print("\t\t------------------")
        if Admin.voting_started:
            print("\t\tVoting has already started.")
        else:
            Admin.voting_started = True
            print("\t\tVoting started.")
        input("Press any key to go back: ")

    @staticmethod
    def end_voting():
        print("\n\n\t\t   End Voting")
        print("\t\t------------------\n")
        if Admin.voting_started:
            Admin.voting_started = False
            print("\t\tVoting ended.")
        else:
            print("\t\tVoting has not started yet.")
        input("Press any key to go back: ")

    @staticmethod
    def view_voters_list(Voter):
        print("\n\n\t\t   Voters List")
        print("\t\t------------------\n")
        if not Voter.voters_dictionary:
            print("\tNo voter registered yet.")
        else:
            # Print dictionary in table format
            df = pd.DataFrame(Voter.voters_dictionary)
            print(tabulate(df.T, headers="keys"))
        input("\n\tPress any key to go back: ")

    @staticmethod
    def view_party_leaders_list(PartyLeader):
        print("\n\n\t\t   Party Leaders List")
        print("\t\t-------------------------\n")
        if not PartyLeader.party_leaders_list:
            print("\tNo party leader registered yet.")
        else:
            df = pd.DataFrame(PartyLeader.party_leaders_list)
            print(tabulate(df.T, headers="keys"))
        input("\n\tPress any key to go back: ")

    @staticmethod
    def view_parties_list(PartyLeader):
        print("\n\n\t\t   Parties List")
        print("\t\t-------------------\n")
        if not PartyLeader.parties_dictionary:
            print("\tNo party registered yet.")
        else:
            df = pd.DataFrame(PartyLeader.parties_dictionary)
            print(tabulate(df.T, headers="keys"))
        input("\n\tPress any key to go back: ")

    @staticmethod
    def all_candidates_list(PartyLeader):
        print("\n\n\t\t   All Candidates List")
        print("\t\t-------------------\n")
        if not PartyLeader.candidates_dictionary:
            print("\tCandidates not registered yet.")
        else:
            df = pd.DataFrame(PartyLeader.candidates_dictionary)
            print(tabulate(df.T, headers="keys"))
        input("\n\tPress any key to go back: ")

    @staticmethod
    def declare_results():
        print("\n\n\t\t   Result Declaration")
        print("\t\t------------------------\n")
        if Admin.results_declared:
            print("\t\tResults has already declared.")
        else:
            Admin.results_declared = True
            print("\t\tResults declared.")
        input("\tPress any key to go back: ")

    @staticmethod
    def view_result(Voter):
        Voter.view_results()
