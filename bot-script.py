# import the necessary packages
from collections import namedtuple
Contact = namedtuple('Contact', ['name', 'phone'])

# list of global functions used in multiple functions
global_dict = dict()
flag = True # flags is responsible for continuing the while loop. If flag is set to False, the loop ends

# decorator that briefly checks the input string.
def initial_screening(func):
    def inner(*args):   
        written_command = func().split()
        num_of_words = len(written_command)
        if written_command[0] not in ['hello', 'add', 'change', 'phone', 'show', 'good', 'close', 'exit']:
            command_reminder()
            return None
        elif written_command[0] in ['add', 'change']:
            try:
                assert num_of_words == 3
                return written_command
            except:
                print('Please include name and phone number by separating them with space.')
                return None
        elif written_command[0] in ['phone']:
            try:
                assert num_of_words == 2
            except:
                print("Please separate 'phone' command and the phone number with space.")
                return None
        return written_command   
    return inner

# decorator that handles errors insided the executed function
def input_error(func):
    def check_error(*args):
        try:
            func(*args)
        except KeyError as ke:
            name = [*args]
            print(f"I haven't found {name[0][0].capitalize()} in the phonebook. Please enter a valid name.")
        finally:
            return ['ask_for_input']
    
    return check_error

# function that routes the written command (by the user) to the correct function
def route_command(command, *args):
    dct = {
        'ask_for_input' : ask_for_input,
        'hello' : hello,
        'add' : add_contact,
        'change' : change_contact,
        'phone' : phone_show,
        'show' : show_all,
        'good' : end_bot,
        'close' : end_bot,
        'exit' : end_bot
    }
    return dct.get(command)

# if user inputs the wrong command, then this function will remind all possible commands
def command_reminder():
    print(
        "Valid commands are: hello, add ..., change ..., phone ...,; show all; good bye, close, exit."
    )
# function that greets the user and lists all possible commands
def initial_greeting():
    print(
        'Hello! I am a bot-assistant.\nI accept the following commands: hello, add ..., change ..., phone ...; show all; good bye, close, exit.'
          )

# function that asks user to input some command. It's checked by the decorator
@initial_screening
def ask_for_input(*args):
    return input('Please enter one of the valid commands: ').lower()

# below are functions that correspond to each command
@initial_screening
def hello(*args):
    return input('How can I help you? ').lower()

@input_error
def add_contact(name_phone):
    global global_dict
    
    contact = Contact(*name_phone)
    contact = Contact(contact.name.capitalize(), contact.phone)

    # check if the input name alredy exists in the phonebook
    if contact.name in global_dict.keys():
        print(f"There is already {contact.name} in the phonebook. Please enter a different name.")
        return
    # check if the input phone number alredy exists in the phonebook
    elif contact.phone in global_dict.values():
        print(f"Thre is already {contact.phone} in the phonebook. Please enter a different phone number.")
    else:
        global_dict[contact.name] = contact.phone
        print(f'{contact.name} has been added.')
    

@input_error
def change_contact(existing_name_new_phone):
    global global_dict

    contact = Contact(*existing_name_new_phone)
    contact = Contact(contact.name.capitalize(), contact.phone)

    # check if the input phone number alredy exists in the phonebook
    if contact.phone in global_dict.values():
        print(f"There is already {contact.phone} in the phonebook. It belongs to {[k for k, v in global_dict.items() if v == contact.phone][0]}.")
    else:
        old_phone = global_dict[contact.name]
        # set the new phone number to the existing name
        global_dict[contact.name] = contact.phone
        print(f"The phone number of {contact.name} has been updated.\n{contact.name}'s old number was {old_phone}.\n{contact.name}'s new phone number is {global_dict[contact.name]}.")

@input_error
def phone_show(name):
    global global_dict

    name = name[0].capitalize()
    respective_phone = global_dict[name]
    print('-'*43)
    print("|{0:^20}|{1:^20}|".format(name, respective_phone))
    print('-'*43)
    

def show_all(*args):
    global global_dict
    print("The full phonebook is:")
    print("|{0:^20}|{1:^20}|".format('name', 'phone number'))
    print("-"*43)
    for k, v in global_dict.items():
        print("|{0:^20}|{1:^20}|".format(k, v))
    return ['ask_for_input']

def end_bot(*args):
    global flag
    flag = False

# main function
def main():
    
    initial_greeting()
    actual_command = 'ask_for_input'
    optional_args = None
    while flag:

        out = route_command(actual_command)(optional_args)

        if out is None:
            continue
        else:
            actual_command = out[0]
            try:
                optional_args = out[1:]
            except:
                None

if __name__ == '__main__':
    main()