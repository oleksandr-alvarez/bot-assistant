# list of global functions used in multiple functions
address_book = {}
flag = True # flags is responsible for continuing the while loop. If flag is set to False, the loop ends




def input_error(func):
    def check_error(*args, **kwargs):
        try: 
            return func(*args, **kwargs)
        except KeyError:
            return f"I haven't found this name in the phonebook. Please enter a valid name."
        except TypeError:
            return 'Please enter a phone number after the name.'    
    return check_error

def parse_input(input):
    input = input.split()
    return input[0], input[1:]

@input_error
def get_handler(command):
    if command in command_list:
        return command_list[command]
    return f"Valid commands are: {', '.join(command_list.keys())}."

    
def hello():
    return 'How can I help you?'

@input_error
def add_contact(name, phone):
    
    name = name.capitalize()

    # check if the input name alredy exists in the phonebook
    if name in address_book:
        return f"There is already {name} in the phonebook. Please enter a different name."
    # check if the input phone number alredy exists in the phonebook
    elif phone in address_book.values():
        return f"There is already {phone} in the phonebook. Please enter a different phone number."
    else:
        address_book[name] = phone
        return f'{name} has been added.'
    

@input_error
def change_contact(existing_name, new_phone):

    existing_name = existing_name.capitalize()

    # check if the input phone number alredy exists in the phonebook
    if new_phone in address_book.values():
        return f"There is already {new_phone} in the phonebook. It belongs to {[k for k, v in address_book.items() if v == new_phone][0]}."
    else:
        old_phone = address_book[existing_name]
        # set the new phone number to the existing name
        address_book[existing_name] = new_phone
        return f"The phone number of {existing_name} has been updated.\n{existing_name}'s old number was {old_phone}.\n{existing_name}'s new phone number is {address_book[existing_name]}."

@input_error
def phone_show(name):

    name = name.capitalize()
    respective_phone = address_book[name]
    print('-'*43)
    print("|{0:^20}|{1:^20}|".format(name, respective_phone))
    print('-'*43)
    

def show_all(*args):
    *extra_args, = args
    if len(extra_args) == 0 or extra_args == ['all']:

        print("The full phonebook is:")
        print("|{0:^20}|{1:^20}|".format('name', 'phone number'))
        print("-"*43)
        for k, v in address_book.items():
            print("|{0:^20}|{1:^20}|".format(k, v))
    else:
        return f"Valid commands are: {', '.join(command_list.keys())}."

    

def end_bot():
    global flag
    flag = False

command_list = {
    'hello' : hello,
    'add' : add_contact,
    'change' : change_contact,
    'phone' : phone_show,
    'show' : show_all,
    'goodbye' : end_bot,
    'close' : end_bot,
    'exit' : end_bot
    }

# main function
def main():
    
    print(
        f"Hello! I am a bot-assistant.\nI accept the following commands: hello, add ..., change ..., phone ...; show all; good bye, close, exit."
          )

    while flag:

        user_input = input('Please enter one of the valid commands: ').lower().strip()

        comm, data = parse_input(user_input)
        handler = get_handler(comm)
        if isinstance(handler, str):
            print(handler)
        else: 
            result = handler(*data)
            if result :
                print(result)



if __name__ == '__main__':
    main()