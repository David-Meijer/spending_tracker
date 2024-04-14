#import polars as pl
import glob
import os

from global_vars import *
from prompt_toolkit import prompt
#from prompt_toolkit.completion import WordCompleter
from completer import return_simple_completer #customized WordCompleter

def get_existing_databases() -> dict:
    database_files = {}
    for file in os.listdir(DATABASE_PATH):
        if file.startswith(DATABASE_PREFIX) and file.endswith(DATABASE_EXTENSION):
            #clean with string slicing, stripping prefix and extension
            clean_database_name = file[len(DATABASE_PREFIX):-len(DATABASE_EXTENSION)] 
            #use cleaned database name as key and store full file path as value
            database_files[clean_database_name] = DATABASE_PATH + '/' + file 
    return database_files

def print_dictionary_keys(dictionary):
     for key in dictionary.keys():
        print('\t', key)

def print_existing_databases(databases):
    print('Existing databases:')
    print_dictionary_keys(databases)

def ask_to_open_existing_database():
    while True:
        user_input = input("\n Do you want to open one of the existing databases to open (see available databases above) \n press 'y' or 'n': ").lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please try again.")

def ask_which_database_name_to_open(existing_databases):
    while True:
        user_input = input('\n Enter the name of the database you wish to open: ')
        if user_input in existing_databases.keys():
            return user_input #returns the database name, this is without prefix and extension
        else:
            print("Invalid input. Please try again.")

def ask_new_database_name():
    new_database_name = input('Please give a name for your new database: ')
    #check if version name already exists. if so, ask to overwrite. else, call self again
    return new_database_name

def ask_for_action():
    print()
    print('What action do you want to perform?\n Press a/add to add a new expenditure.\n Press dr/"delete row" to delete a row.\n Press q/quit to quit.\n')
    
#def checks_on_startup():
#    os.makedirs(os.path.dirname(f'.{DATABASE_PATH}'), exist_ok=True)

def get_action_user_input():
    SimpleCompleter = return_simple_completer(VALID_DATABASE_ACTION_INPUTS) #TODO: Make this a global class
    action_user_input = prompt('Input: ', completer=SimpleCompleter)
    return action_user_input

def check_for_valid_action_user_input(action_user_input):
    if action_user_input in VALID_DATABASE_ACTION_INPUTS:
        for category in VALID_CATEGORIZED_DATABASE_ACTION_INPUTS:
            #Match input on valid inputs to bind a category. This way multiple inputs ca be given for a single category for example a, add = 'add' category.
            if action_user_input in VALID_CATEGORIZED_DATABASE_ACTION_INPUTS[category]:
                return category 
    else:
        return False
                

