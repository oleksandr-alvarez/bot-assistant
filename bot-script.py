# import the necessary packages
from collections import namedtuple
Contact = namedtuple('Contact', ['name', 'phone'])

# list of global functions used in multiple functions
global_dict = dict()
flag = True # flags is responsible for continuing the while loop. If flag is set to False, the loop ends

def input_error(func):
    def check_error(*args):
        try: 
            out = func(*args)
            return out
        except KeyError:
            name = [*args]
            return f"I haven't found {name[0].capitalize()} in the phonebook. Please enter a valid name."
        except TypeError:
            return 'Please enter a phone number after the name.'    
    return check_error

def parse_input(input):
    input = input.split()
    return input[0], input[1:]

@input_error
def get_handler(command):
    try:
        assert command in ['hello', 'add', 'change', 'phone', 'show', 'good', 'close', 'exit']
        dct = {
        # 'ask_for_input' : ask_for_input,
        'hello' : hello,
        'add' : add_contact,
        'change' : change_contact,
        'phone' : phone_show,
        'show' : show_all,
        'good' : end_bot,
        'close' : end_bot,
        'exit' : end_bot
        }
        return dct[command]
    except AssertionError:
        return "Valid commands are: hello, add ..., change ..., phone ...,; show all; good bye, close, exit."

    
def hello():
    return 'How can I help you?'

@input_error
def add_contact(*name_phone):
    global global_dict
    
    contact = Contact(*name_phone)
    contact = Contact(contact.name.capitalize(), contact.phone)

    # check if the input name alredy exists in the phonebook
    if contact.name in global_dict.keys():
        return f"There is already {contact.name} in the phonebook. Please enter a different name."
    # check if the input phone number alredy exists in the phonebook
    elif contact.phone in global_dict.values():
        return f"Thre is already {contact.phone} in the phonebook. Please enter a different phone number."
    else:
        global_dict[contact.name] = contact.phone
        return f'{contact.name} has been added.'
    

@input_error
def change_contact(*existing_name_new_phone):
    global global_dict

    contact = Contact(*existing_name_new_phone)
    contact = Contact(contact.name.capitalize(), contact.phone)

    # check if the input phone number alredy exists in the phonebook
    if contact.phone in global_dict.values():
        return f"There is already {contact.phone} in the phonebook. It belongs to {[k for k, v in global_dict.items() if v == contact.phone][0]}."
    else:
        old_phone = global_dict[contact.name]
        # set the new phone number to the existing name
        global_dict[contact.name] = contact.phone
        return f"The phone number of {contact.name} has been updated.\n{contact.name}'s old number was {old_phone}.\n{contact.name}'s new phone number is {global_dict[contact.name]}."

@input_error
def phone_show(name):
    global global_dict

    name = name.capitalize()
    respective_phone = global_dict[name]
    print('-'*43)
    print("|{0:^20}|{1:^20}|".format(name, respective_phone))
    print('-'*43)
    

def show_all(*args):
    try:
        *n, = args
        assert len(n) == 0 or n == ['all']
        global global_dict
        print("The full phonebook is:")
        print("|{0:^20}|{1:^20}|".format('name', 'phone number'))
        print("-"*43)
        for k, v in global_dict.items():
            print("|{0:^20}|{1:^20}|".format(k, v))
    except AssertionError:
        return "Valid commands are: hello, add ..., change ..., phone ...,; show all; good bye, close, exit."

    

def end_bot():
    global flag
    flag = False

# main function
def main():
    
    print(
        'Hello! I am a bot-assistant.\nI accept the following commands: hello, add ..., change ..., phone ...; show all; good bye, close, exit.'
          )
    # actual_command = 'ask_for_input'
    # optional_args = None
    while flag:

        user_input = input('Please enter one of the valid commands: ').lower().strip()

        comm, data = parse_input(user_input)
        handler = get_handler(comm)
        if type(handler) is str:
            print(handler)
        else: 
            result = handler(*data)
            if result is not None:
                print(result)
            else:
                continue



if __name__ == '__main__':
    main()