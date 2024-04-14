from global_vars import *
from SessionDatabase import SessionDatabase
from helpers import *

def main():
    Database = SessionDatabase()

    #Check if there are already versions databases
    existing_databases = get_existing_databases() 

    #Open or create a database for the session
    if existing_databases:
        print_existing_databases(existing_databases)
        if ask_to_open_existing_database():
            database_name = ask_which_database_name_to_open(existing_databases)
            Database.load_existing_database(database_name, existing_databases)
    if not Database.database_name: #executed when user answers no to ask_to_open_database or when there are no existing databases
        while True: #User must chose a unique name. TODO: ask user if he wants to overwrite
            new_database_name = ask_new_database_name()
            if new_database_name in existing_databases.keys():
                print('\n There already exists a database with this name!, please use a unique name!')
                continue
            else:
                break 
        Database.create_new_database(new_database_name)

    #Ask the user what kind of action he wants to perform
    while True:
        ask_for_action() #Prints all available actions to the screen and asks user for input on what action he wants to perform.
        user_input = get_action_user_input() #generates the prompt with (including autocompleter functionality)
        valid_action_user_input = check_for_valid_action_user_input(user_input) #function returns False if not valid
        if valid_action_user_input and valid_action_user_input != 'quit': 
            Database.handle_action(valid_action_user_input)
        elif valid_action_user_input == 'quit':
            break
        else:
            print('input not recognized, please try again!')

    print('Closing application...') #Hits when valid_action_user_input == 'quit'
    Database.save_database()

    print(Database.database)


if __name__ == '__main__':
    main()

 