from email.mime import base
import json
import os
from urllib import response
from address_contact_repository import AddressContactRepository
global address_contact
address_contact = None

addressContactRepository = AddressContactRepository()



def requirement_check(data):
    if data == "":
        print("This Field is Required")
        return False
    else:
        return True



def add_contact():
    print("\nAdd New Contact")
    while True:
        name = input("Name (Required): ")
        if requirement_check(name) == True:
            break
    while True:
        address = input("Address (Required): ")
        if requirement_check(address) == True:
            break
    contact = input("Enter Contact : ")
    email = input("Enter Email : ")
    new_entry = {
        "name":name,
        "address":address,
        "contact":contact,
        "email":email
    }
    addressContactRepository.add_new_address_contacts(new_entry)
    print("Successfully saved")



# def display_search_result(result):
#     index = 1
#     print("\033[1;32;40m** ALL CONTACTS **\n")
#     print("\033[1;33;40mID\t| NAME\t| ADDRESS\t| CONTACT\t| EMAIl")
#     for entry in result:
#         print("\033[1;37;40m{}\t| {}\t| {}\t| {}\t| {}".format(
#             index,
#             entry.get("name"),
#             entry.get("address"),
#             entry.get("contact"),
#             entry.get("email")
#             ))
#         index = index + 1

def display_search_result(result):

    max_length_name = len("Name")
    max_length_address = len("Address")
    max_length_contact = len("Contact")
    max_length_email = len("Email")
    max_length_index = len(str(len("No.")))
    ctr = 1
    if len(result) > 0:
        for item in result:
            if max_length_name < len(item.get('name')):
                max_length_name = len(item.get('name'))
            if max_length_address < len(item.get('address')):
                max_length_address = len(item.get('address'))
            if max_length_email < len(item.get('email')):
                max_length_email = len(item.get('email'))
            if max_length_contact < len(str(item.get('contact'))):
                max_length_contact = len(str(item.get('contact')))

        print("\033[1;33;40m ** DISPLAY CONTACT/S **\n \033[1;37;40m")
        print(
            "\033[1;32;40mNo.{}\t|Name{}\t|Email{}\t|Address{}\t|Contact\033[1;37;40m".format(
                add_space(max_length_index-len("No.")),
                add_space(max_length_name - len("Name")),
                add_space(max_length_email - len("Email")),
                add_space(max_length_address - len("Address"))
                ))
        for item in result:

            print("{} \t|{}\t|{}\t|{}\t|{}".format(
                str(ctr) + add_space(max_length_index - len(str(ctr))),
                item.get('name') + add_space(max_length_name -
                                             len(item.get('name'))),
                item.get('email') + add_space(max_length_email -
                                              len(item.get('email'))),
                item.get('address') + add_space(max_length_address -
                                                len(item.get('address'))),
                str(item.get('contact')) + add_space(max_length_contact - len(str(item.get('contact'))))))
            ctr += 1
    else:
        print("No results")

    # input("\n\033[1;34;40mPress enter to go back to main menu...\n\033[1;37;40m")


def add_space(num):
    return " " * (num)


def search_address_contact(operation):
    name = input("Enter Name : ")
    result = addressContactRepository.find_address_contact(name)
    record_for_edit = None
    
    if len(result) > 1:
        
        display_search_result(result)
        while True:
            try:
                id = int(input("\nEnter Account ID to {} [1-{}]: ".format(operation,len(result))))
                if id > len(result):
                    print("Invalid Selection, Please Try Again")
                else:
                    record_for_edit = result[id-1]
                    break
            except ValueError:
                print("Invalid input")

    elif len(result) == 1:
        display_search_result(result)
        record_for_edit = result[0]
    else:
        print("Account not found")

    return record_for_edit


def update_contact():
    print("\n**Update Account**\n")
    print("Search Account")
    display_edit_screen(search_address_contact("edit"))

def delete_contact():
    print("\n**Delete Account**\n")
    print("Search Account")
    result = search_address_contact("delete")
    if result != None:
        while True:
            response = input("Delete Account (Y/N)?")
            if response.lower() == "y":
                addressContactRepository.delete_address_contact(result)
                # print("record for delete -> {}".format(result))
                print("Successfully deleted. \n")
                break
            elif response.lower() == "n":
                input("\nUser cancelled, press enter key to quit")
                break
            else:
                print("Invalid Selection")
    # display_edit_screen()


def display_edit_screen(record_for_edit):
    if record_for_edit != None:
        clear_screen()
        get_user_input = lambda input, default : input if input != "" else default
        name = record_for_edit.get("name")
        address =  record_for_edit.get("address")
        contact =  record_for_edit.get("contact")
        email =  record_for_edit.get("email")
        print("** EDIT ADDRESS CONTACT **")
        name = get_user_input(input("New Name [{}]: ".format(name)),name)
        address = get_user_input(input("New Address [{}]: ".format(address)),address)
        while True:
            try:
                contact = int(get_user_input(input("New Contact [{}]: ".format(contact)),contact))
                break
            except ValueError:
                print("Invalid input")

        email = get_user_input(input("New Email [{}]: ".format(email)),email)

        record_for_edit["name"] = name
        record_for_edit["address"] = address
        record_for_edit["contact"] = contact
        record_for_edit["email"] = email

        addressContactRepository.update_address_contact(record_for_edit)
        print("Successfully Updated. \n")



def clear_screen():
    os.system("cls")

def transaction_selection():
    while True:
        selection = input("\033[1;34;40m \nGo back to main menu again? [Y/N]: \033[1;37;40m")
        if selection.lower() == "y":
            clear_screen()
            return True
        elif selection.lower() == "n":
            clear_screen()
            print("Thank you")
            return False


def display_menu():
    clear_screen()
    while True:
        print("\nAddress Book")
        print("\t1. Display Account")
        print("\t2. Add New Account")
        print("\t3. Update Account")
        print("\t4. Delete Account")
        selection = input("\nEnter Selection: ")

        if selection == "1":
            clear_screen()
            display_search_result(addressContactRepository.get_address_contacts().get("details"))
            if transaction_selection() == False:
                break
        elif selection == "2":
            clear_screen()
            add_contact()
            if transaction_selection() == False:
                break
        elif selection == "3":
            clear_screen()
            update_contact()
            if transaction_selection() == False:
                break
        elif selection == "4":
            clear_screen()
            delete_contact()
            if transaction_selection() == False:
                break
        else:
            print("Enter valid input")

display_menu()    
