#Version of budget app
APP_VERSION = '1.0'

#Path where version database csv's are stored
DATABASE_PATH = './Database'

DATABASE_EXTENSION = '.csv'

#Version database prefix to find csv's stored by budgetapp
DATABASE_PREFIX = 'BudgetApp_DATABASE_'

VALID_CATEGORIZED_DATABASE_ACTION_INPUTS  = {
    'add': ['a', 'add'],
    'delete_row': ['dr', 'delete row'],
    'quit': ['q', 'quit'],
    'save': ['sv', 'save']
}

VALID_DATABASE_ACTION_INPUTS = [v for category in VALID_CATEGORIZED_DATABASE_ACTION_INPUTS.values() for v in category]

