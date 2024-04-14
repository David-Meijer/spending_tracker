#Simple completer class

#from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def return_simple_completer(word_list):
    SimpleCompleter = WordCompleter(word_list, ignore_case=True)
    return SimpleCompleter



