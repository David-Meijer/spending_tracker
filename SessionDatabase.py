import polars as pl
from datetime import datetime, date
from global_vars import *

#TODO: implement readline module: https://docs.python.org/3/library/readline.html, https://pymotw.com/2/readline/

class SessionDatabase:
    def __init__(self):
        self.database_name = None #In order to save it with the same database name at the end of the session
        self.database = None #Opened database, polars dataframe.
        self.category_tree = None #Dict that hold all categories and subcategories in tree-form
        self.unique_categories = None #set of category
        self.unique_subcategories_1 = None #set of subcategory_1
        self.unique_subcategories_2 = None #set of subcategory_2
        self.next_database_index = None #In order to keep track of the index. Is equal to the amount of rows as we begin with index = 0
        self.database_schema = {
                'index': pl.Int64, #TODO: right now in the delete, people can also give up negative index numbers.
                'amount': pl.Float64,
                'category': pl.Utf8,
                'subcategory_1': pl.Utf8,
                'subcategory_2': pl.Utf8,
                'expenditure_date': pl.Date,
                'entry_date': pl.Datetime

            }


    def load_existing_database(self, existing_database_name, existing_databases):
        self.database_name = existing_database_name
        self.database = pl.read_csv(existing_databases[existing_database_name], schema=self.database_schema)
        print(f'opened database: {existing_database_name} \n')
        #Only run when there are rows in the database
        if len(self.database) > 0:
            self.next_database_index = (self.database.select(pl.max('index')).item() + 1) #https://docs.pola.rs/py-polars/html/reference/expressions/api/polars.max.html
            print(f'counted {self.next_database_index} rows! \n') #begins at zero so the next index is equal to the amount of rows
            print('populating category tree..\n')
            self.fill_category_tree()
            print('looking up all unique categories..\n')
            self.fill_unique_categories()
        #Only run when the database is empty
        else:
            self.next_database_index = int(0)

    def create_new_database(self, new_database_name):
        self.database_name = new_database_name
        self.next_database_index = int(0)
        self.database = pl.DataFrame(schema = self.database_schema)
        print(f'created database: {new_database_name}')

    def fill_category_tree(self):
        #Initial load
        self.category_tree = self.database.select('category', 'subcategory_1', 'subcategory_2').unique()

    def fill_unique_categories(self):
        self.unique_categories = self.category_tree.select('category').unique()
        print('unique categories loaded!')
        self.unique_subcategories_1 = self.category_tree.select('subcategory_1').unique()
        self.unique_subcategories_2 = self.category_tree.select('subcategory_2').unique()
        print('unique subcategories loaded! \n')

    #TODO:Implement
    def update_category(self):
        #if category is added, add to tree.
        return

    def handle_action(self, action):
        if action == 'add':
            self.add_expenditure()
        elif action == 'show':
            #possibly implement ask_for_last_nr_of_rows_to_show()
            print(self.database)
        elif action == 'delete_row':
            self.delete_row()
        elif action == 'save':
            self.save_database()
        else: 
            raise ValueError (f'Action: {action} recognized as valid action input but no handler has been build. Update valid actions in the configuration or build action handler')

    def add_expenditure(self):
        #TODO: implement typechecking
        index = self.next_database_index
        category, subcategory_1, subcategory_2 = self.ask_for_expenditure_categories()
        amount = self.ask_for_expenditure_amount()
        expenditure_date = self.ask_for_expenditure_date()

        #Fill new database row with given inputs
        new_database_row = pl.DataFrame(
            {
            'index': [index],
            'amount': [amount],
            'category': [category],
            'subcategory_1': [subcategory_1],
            'subcategory_2': [subcategory_2],
            'expenditure_date': [expenditure_date],
            'entry_date': [datetime.now()]
            }

        )
        self.database = pl.concat([self.database, new_database_row])
        self.next_database_index += 1

        #self.fill_category_tree()

    def ask_for_expenditure_categories(self):
        partial_question = 'please name the '
        category =  str(input(partial_question + 'category: '))
        subcategory_1 = str(input(partial_question + 'subcategory_1: '))
        subcategory_2 = str(input(partial_question + 'subcategory_2: '))
        return category, subcategory_1, subcategory_2

    def ask_for_expenditure_amount(self):
        partial_question = 'please name the '
        return float(input(partial_question + 'amount: '))

    def ask_for_expenditure_date(self):
        partial_question = 'please name the '
        date_of_expenditure = str(input(partial_question + 'date of expenditure (dd-mm-yyyy) (PRESS ENTER TO USE TODAY\'S DATE): '))
        if date_of_expenditure == '':
            #get datetime.now and take only the day-month-year
            date_of_expenditure = date.today() 
        else:
            #first cast string to datetime with strptime, then make it a date type.
            date_of_expenditure = datetime.strptime(date_of_expenditure, '%d-%m-%Y').date()
        return date_of_expenditure
            

    def delete_row(self):
        last_nr_of_rows_to_show = self.ask_for_last_nr_of_rows_to_show()
        print(self.database.slice(last_nr_of_rows_to_show, None))
        index_of_row_to_delete = self.ask_for_index_of_row_to_delete()
        if index_of_row_to_delete != 'abandon':
            print('\n You are about to delete the following row:')
            print(self.database.slice(index_of_row_to_delete, length=1))
            #Ask if user really wants to delete the row
            if self.ask_for_confirmation():
                #If so, delete
                self.delete_row_at_index(index_of_row_to_delete)
                self.rebase_database_index()

    def ask_for_last_nr_of_rows_to_show(self):
        print('Please enter a number corresponding to the amount of last rows you want to see.')
        print('You can press enter or 0 to show all rows.')
        last_nr_of_rows_to_show = input('Number of rows (press enter or 0 to show all rows): ')

        if last_nr_of_rows_to_show == '':  #before casting to integer type, check for enter
            return 0
        try: #Cast to integer
            last_nr_of_rows_to_show = int(last_nr_of_rows_to_show) 
        except: #when the input is not of integer type, ask user to try again
            print('\n ERROR: The given input is not a number! Please try again.')
            last_nr_of_rows_to_show = self.ask_for_last_nr_of_rows_to_show() #recursively ask user to give a valid input
        else:
            last_nr_of_rows_to_show *= -1 #make negative to make the offset to represent the last number of rows
        
        return last_nr_of_rows_to_show

    def ask_for_index_of_row_to_delete(self):
        print('Please type the index of the row you want to delete. Press ENTER to abandon and not delete any row.')
        index_of_row_to_delete = input('Index of row to delete (press ENTER to abandon): ')

        if index_of_row_to_delete == '':  #before casting to integer type, check for enter
            return 'abandon'
        try: #Cast to integer
            index_of_row_to_delete = int(index_of_row_to_delete)
        except: #when the input is not of integer type, ask user to try again
            print('\n ERROR: The given input is not a (postitive) number! Please try again.')
            index_of_row_to_delete = self.ask_for_index_of_row_to_delete() #recursively ask user to give a valid input

        return index_of_row_to_delete

    def delete_row_at_index(self, index_of_row_to_delete):
        try:
            self.database.row(index_of_row_to_delete)
        except:
            Print(f'error retrieving the to be deleted row at index {index_of_row_to_delete}, please try again')
            #Note that recalling self.delete_function can only be done if this function is also triggered from the delete_row function.
            self.delete_row() #try again. Non existing or false index given by user.
        else:
            #Remove row by creating two dataframen and stacking them again, not selecting the row at the index to be deleted
            self.database = self.database[:index_of_row_to_delete].vstack(self.database[index_of_row_to_delete+1:])

    def rebase_database_index(self):
        #Function will recalculate index column (e.g. use when rows have been deleted)
        #First remove index column and create a new one
        self.database = (
            self.database
                .drop('index')
                .select(
                #Select new index column, then select all others
                pl.int_range(pl.len(), dtype=pl.Int64).alias('index'),
                pl.all()
            )
        )
        #Reset next database index based on newly calculated column.
        self.next_database_index = self.database.select(pl.max('index')).item() + 1

    def ask_for_confirmation(self):
        if input('please enter y/yes to confirm, anything else to abandon: ') in ['y', 'yes']:
            return True
        else:
            return False

    def save_database(self):
        file_path = (f'{DATABASE_PATH}/{DATABASE_PREFIX}{self.database_name}{DATABASE_EXTENSION}')
        if DATABASE_EXTENSION == '.csv':
            self.database.write_csv(file=file_path)

        else:
            print(f'Configurated database extension: {DATABASE_EXTENSION} is not supported for saving!')
            print('Backing up in .csv')
            file_path = (f'{DATABASE_PATH}/{DATABASE_PREFIX}{self.database_name}.csv')
            self.database.write_csv(file=file_path)

        print(f'saved database: {self.database_name}, path = {file_path}')


