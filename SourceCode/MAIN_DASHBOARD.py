"""" Imports:
            1. ADMIN Package.
            2. VOTER Package
            3. PARTY_LEADER
            4. REGISTRATION"""


class Dashboard:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        from VOTER import Voter
        from REGISTRATION import Registration
        from PARTY_LEADER import PartyLeader
        from ADMIN import Admin
        while True:
            print("\n\n\t\t\t   Main Menu")
            print("\t\t\t---------------")
            print("\n\t\t1. Register Yourself")
            print("\t\t2. Login as Voter")
            print("\t\t3. Login as Party Leader")
            print("\t\t4. Login as Admin")
            print("\t\t5. View Results")
            print("\t\t6. Exit")

            choice = input("\n\tEnter your choice: ")

            if choice == "1":
                Registration.register_voter()
            elif choice == "2":
                Voter.login_as_voter(Registration)
            elif choice == "3":
                PartyLeader.login_as_party_leader(Registration)
            elif choice == "4":
                Admin.login_as_admin()
            elif choice == "5":
                if Admin.results_declared:
                    Voter.view_results()
                else:
                    print("\n\tResults not declared yet by Admin.")
            elif choice == "6":
                break
            else:
                print("\n\t\tInvalid choice. Please try again.")