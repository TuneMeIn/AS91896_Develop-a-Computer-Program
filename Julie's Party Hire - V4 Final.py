# Date Created: 19/08/2024
# Author: Jack Compton
# Purpose: GUI application for Julie's party hire store to keep track of currently hired items.

import os
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random


# Function for quitting the program.
def quit_program():
    main_window.destroy()


# Function for clearing specified widgets (column, row).
def clear_widget(column, row):
    # Find all widgets in the specified row and column.
    for widget in main_canvas.grid_slaves(column=column, row=row):
        widget.destroy()      # Destroy the widgets occupying the specified space.


# Function for loading the "customer_details" list from the JSON file.
def load_customer_details():
        global data_loaded, customer_details

        if not os.path.exists("customer_receipts.json"):
            with open("customer_receipts.json", "w") as file:  # Create a new JSON file with an empty list if the file doesn't already exist.
                json.dump([], file)         # Write an empty list to the new JSON file.
            customer_details = []           # Initialise customer_details as an empty list.
            data_loaded = True              # Set the "data_loaded" variable to True, so that the program doesn't reload data before printing.
            counter["entry_number"] = 1     # Set the initial entry number.
        try:
            with open("customer_receipts.json", "r") as file:  # Open the JSON file in read mode ("r").
                customer_details.clear              # Clear the list to prevent duplicate entries.
                customer_details = json.load(file)  # Load the details from the JSON file into the "customer_details" list.
                data_loaded = True                  # Set the "data_loaded" variable to True, so that the program doesn't reload data before printing.
                counter["entry_number"] = len(customer_details) + 1  # Update the entry number so the user knows what number of entry they will be submitting.
        except json.JSONDecodeError:  # Error control for instances such as the JSON file having invalid data, having incorrect formatting, or being corrupted.
            response = messagebox.askyesno("File Error", "Failed to decode JSON data. The file may be corrupted or improperly formatted. Do you want to replace it?")
            if response == True:
                try:
                        with open("customer_receipts.json", "w") as file:  # Open the "customer_receipts.json" file in write mode ("w").
                            json.dump([], file)    # Overwrite the JSON file with an empty list.
                        with open("customer_receipts.json", "r") as file:  # Open the JSON file in read mode ("r").
                            customer_details.clear              # Clear the list to prevent duplicate entries.
                            customer_details = json.load(file)  # Load the details from the JSON file into the "customer_details" list.
                            data_loaded = True                  # Set the "data_loaded" variable to True, so that the program doesn't reload data before printing.
                            counter["entry_number"] = len(customer_details) + 1  # Update the entry number so the user knows what number of entry they will be submitting.
                        messagebox.showinfo("File Replaced", "The JSON file has been successfully replaced with an empty list.")
                        
                except IOError as io_error:  # Error control for instances such as the file being inaccessible or lacking the permission to read/write it.
                    messagebox.showerror("File Error", f"An error occurred while replacing the file: {io_error}")


# Function for saving the customer details to the JSON file.
def save_customer_details():
    global data_loaded
    try:
        with open("customer_receipts.json", "w") as file:   # Open the "customer_receipts.json" file in write mode ("w"). If it doesn't exist, a new file will be created.
            json.dump(customer_details, file, indent=4)     # Dump the entries from the "customer_details" list into the JSON file.
        data_loaded = False  # Set the "data_loaded" variable to false, so that the program will reload data from JSON file when printing.
    except IOError:
        messagebox.showerror("File Error", "Failed to write to 'customer_receipts.json'. Check file permissions or disk space.")
        quit_program()


# Function for handling the treeview items being selected.
def on_item_selected(event):
    global delkey_binded
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]                          # Set the "item_id" variable to the selected item's id.
        receipt_number = tree.item(item_id, "values")[1]    # Make the "receipt_number" equal to the receipt number of the entry selected.
        delete_receipt_num.delete(0, "end")                 # Remove the value in the "delete_receipt_num" entry box (from the beginning (0) to the end).
        delete_receipt_num.insert(0, receipt_number)        # Update the "delete_receipt_num" entry box with the receipt number.
        tree.bind("<Delete>", delete_receipt)               # Bind the "del" key to the "delete_receipt" function so that the selected receipt can be deleted.
        delkey_binded = True                                # Set "delkey_binded" variable/flag to True so program will later unbind the "del" key once the receipt is deleted.


# Function for printing all the customer receipts inside a Treeview widget.
def print_customer_details():
    global tree, remove_treeview, counter, customer_details, data_loaded

    # Clear the Treeview if it's already displayed.
    if remove_treeview == True:
        for widget in main_window.grid_slaves():
            if int(widget.grid_info()["row"]) > 7:  # Check if there are widgets in a row larger than 7, which is where the treeview is displayed.
                widget.grid_forget()                # Remove the treeview from the grid by forgetting it.
                remove_treeview = False             # Set "treeview_displayed" variable/flag to "False" so the treeview can be printed again next time the print function is run.

    else:
        if not data_loaded:
            load_customer_details()  # Reload the "customer_details" list from the JSON file if not up-to-date.

        try:
            if len(customer_details) <= 0:
                messagebox.showwarning("No Data Available", "There are no customer details to print. Please submit a customer receipt.")
                return  # Exit the function if the "customer_details" list is empty.

            else:
                for widget in main_window.grid_slaves():
                    if int(widget.grid_info()["row"]) > 7:  # Check if there are widgets in a row larger than 7, which is where the treeview is displayed.
                        widget.grid_forget()                # Remove the old treeview from the grid by forgetting it.

                # Create a frame to hold the Treeview and scrollbar.
                tree_frame = Frame(main_window)
                tree_frame.grid(column=0, row=9, columnspan=6, padx=20, pady=[0,20], sticky="nsew")

                treestyle = ttk.Style()
                treestyle.theme_use("default")

                # Configure the Treeview style for the field section.
                treestyle.configure("custom.Treeview",
                                    background=main_canvas_colour,          # Background colour of the treeview field entries.
                                    foreground="white",                     # Text colour of the treeview headings.
                                    fieldbackground=main_canvas_colour,     # Main background colour of the treeview field.
                                    font=("Segoe UI", 10))                  # Font style of the treeview field text.
                
                # Configure the Treeview style for the headings.
                treestyle.configure("custom.Treeview.Heading",
                                    background="#8183b2",           # Background colour of the treeview headings.
                                    foreground="white",             # Text colour of the treeview headings.
                                    font=("Segoe UI", 10,"bold"),   # Font style of the treeview heading text.
                                    relief="ridge")                 # Set the relief to "ridge" to give the header less of a button-look.

                # Change entry selection colour using ".map()" for dynamic styling of the "selected" state.
                treestyle.map("Treeview",
                            background=[("selected", "#9496c3")])  # Selection background colour of the treeview field entries.

                # Change the highlight colour for the headers when the mouse hovers over them.
                treestyle.map("custom.Treeview.Heading",
                            background=[("active", "#7678a3")],    # Background colour of the treeview headings when hovered over.
                            foreground=[("active", "white")])      # Text colour of the treeview headings when hovered over.


                # Create a Treeview widget to display the customer receipts.
                columns = ("Entry", "Receipt No.", "First Name", "Last Name", "Item Hired", "Amount Hired")
                tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="custom.Treeview", height=8)
                
                # Define the Treeview column headings.
                for col in columns:
                    tree.heading(col, text=col)
                
                # Set individual Treeview column widths.
                column_widths = {
                    "Entry": 50,
                    "Receipt No.": 100,
                    "First Name": 150,
                    "Last Name": 150,
                    "Item Hired": 150,
                    "Amount Hired": 100
                }

                # Configure the Treeview columns.
                for col in columns:
                    tree.column(col, anchor=W, width=column_widths[col])

                # Add each item in the list into the Treeview.
                for index, details in enumerate(customer_details):
                    custom_firstname = details[1]
                    custom_lastname = details[2]

                    # Truncate the first name if it exceeds 16 characters.
                    if len(details[1]) >= 16:
                        custom_firstname = details[1][:13] + "..."

                    # Truncate the last name if it exceeds 16 characters.
                    if len(details[2]) >= 16:
                        custom_lastname = details[2][:13] + "..."

                    tree.insert("", "end", values=(index + 1, details[0], custom_firstname, custom_lastname, details[3], details[4]))

                # Bind the treeview item selection event to the "on_item_selected" function.
                tree.bind("<<TreeviewSelect>>", on_item_selected)

                # Create a vertical scrollbar for the Treeview if the list is higher than 8 entries.
                if int(len(customer_details)) > 8:
                    scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)  
                    tree.configure(yscrollcommand=scrollbar.set)
                    scrollbar.pack(side=RIGHT, fill=Y)  # Position the scrollbar inside the frame by using ".pack()".

                # Position the Treeview inside the frame by using ".pack()".
                tree.pack(side=LEFT, fill=BOTH, expand=True)

                # Make sure the frame resizes properly by setting the weight to 1.
                tree_frame.grid_columnconfigure(0, weight=1)
                tree_frame.grid_rowconfigure(0, weight=1)

                remove_treeview = True  # Set "treeview_displayed" variable/flag to "True" so that pressing the print button next time will remove the treeview.

        except IndexError:
            for widget in main_window.grid_slaves():
                if int(widget.grid_info()["row"]) > 7:  # Check if there are widgets in a row larger than 7, which is where the treeview is displayed.
                    widget.grid_forget()                # Remove the treeview from the grid by forgetting it.
                    remove_treeview = False             # Set "treeview_displayed" variable/flag to "False" so the treeview can be printed again next time the print function is run.
            response = messagebox.askyesno("Replace JSON File", "Invalid JSON data: The JSON file may have been modified or improperly formatted. Do you want to replace it?")
            if response == True:
                try:
                    with open("customer_receipts.json", "w") as file:
                        json.dump([], file)         # Overwrite the JSON file with an empty list.
                        load_customer_details()     # Reload the "customer_details" list.
                        Label(main_canvas, text=counter["entry_number"], font=("Segoe UI", 10, "bold"), bg=main_canvas_colour, fg="white").grid(column=1, row=0, pady=[15,0])
                    messagebox.showinfo("File Replaced", "The JSON file has been successfully replaced with an empty list.")
                    
                except IOError as io_error:  # Error control for instances such as the file not existing or lacking the permission to read/write it.
                    messagebox.showerror("File Error", f"An error occurred while replacing the file: {io_error}")
                    

# Function for checking if there are any invalid entries inside the entry boxes.
def validate_customer_details():
    details_error_detected = False
    error_messages = []  # List to store error messages so that they can be joined into the warning message box after error control is completed.
    entry_clear = []     # List to store entry box variable names so that the box can be cleared.

    # Clear any previous error messages by using the "clear_widget(column, row)" function.
    clear_widget(2, 1)
    clear_widget(2, 2)
    clear_widget(2, 3)
    clear_widget(2, 4)

    # First Name error control.
    # Check if the "first_name" entry is blank.
    if first_name.get().strip() == "":
        Label(main_canvas, text="Required", bg=main_canvas_colour, fg="red").grid(column=2, row=1, sticky=W)
        error_messages.append("First Name is required and cannot be left blank.")
        details_error_detected = True

    # Check if the "first_name" entry is above 50 characters long.
    elif len(first_name.get().strip().replace(" ", "")) > 50:
        Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=1, sticky=W)
        error_messages.append("First Name cannot be longer than 50 characters.")
        entry_clear.append(first_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
        details_error_detected = True        

    # Check if the "first_name" entry only contains digits.
    elif first_name.get().strip().replace(" ", "").isdigit():
        Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=1, sticky=W)
        error_messages.append("First Name cannot only contain numbers.\n     - Please include at least one letter.")
        entry_clear.append(first_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
        details_error_detected = True

    # Check if "first_name" entry contains a combination of letters and numbers, as well as at least one letter.
    else:
        if not (first_name.get().strip().replace(" ", "").isalnum() and any(char.isalpha() for char in first_name.get())):
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=1, sticky=W)
            error_messages.append("First Name can only include letters or letters with numbers.\n     - No symbols or non-alphanumeric characters.")
            entry_clear.append(first_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True

    # Last Name error control.
    # Check if the "last_name" entry is blank.
    if last_name.get().strip() == "":
        Label(main_canvas, text="Required", bg=main_canvas_colour, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("Last Name is required and cannot be left blank.")
        details_error_detected = True

    # Check if the "last_name" entry is above 50 characters long.
    elif len(last_name.get().strip().replace(" ", "")) > 50:
        Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("Last Name cannot be longer than 50 characters.")
        entry_clear.append(last_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
        details_error_detected = True

    # Check if the "last_name" entry only contains digits.
    elif last_name.get().strip().replace(" ", "").isdigit():
        Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("Last Name cannot only contain numbers.\n     - Please include at least one letter.")
        entry_clear.append(last_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
        details_error_detected = True

    # Check if "last_name" contains a combination of letters and numbers, as well as at least one letter.
    else:
        if not (last_name.get().strip().replace(" ", "").isalnum() and any(char.isalpha() for char in last_name.get())):
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=2, sticky=W)
            error_messages.append("Last Name can only include letters or letters with numbers.\n     - No symbols or non-alphanumeric characters.")
            entry_clear.append(last_name)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True

    # Item Hired error control.
    # Check if the "item_hired" entry is blank.
    if len(item_hired.get()) == 0:
        Label(main_canvas, text="Required", bg=main_canvas_colour, fg="red").grid(column=2, row=3, sticky=W)
        error_messages.append("Item Hired is required and cannot be left blank.")
        details_error_detected = True

    # Amount Hired error control.
    # Check if the "amount_hired" entry is blank.
    if amount_hired.get().strip() == "":
        Label(main_canvas, text="Required", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
        error_messages.append("Amount Hired is required and cannot be left blank.")
        details_error_detected = True

    # Check if the "amount_hired" entry contains any alphabetic characters.
    elif any(char.isalpha() for char in amount_hired.get().strip().replace(" ", "")):
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
            error_messages.append("Amount Hired must only include numbers, no letters.")
            entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True
    
    # Check if the "amount_hired" entry is a negative number (starting with a minus sign) and has at least one numeric value after it.
    elif amount_hired.get().strip().replace(" ", "").startswith("-") and any(char.isnumeric() for char in amount_hired.get()):
            Label(main_canvas, text="Between 1-500", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
            error_messages.append("Amount Hired must be a positive number between 1 and 500.")
            entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True

    # Check if the "amount_hired" entry only contains digits and if so, whether the value is below/equal to zero or above 500.
    elif amount_hired.get().strip().replace(" ", "").isdigit():
        if int(amount_hired.get().replace(" ", "")) <= 0 or int(amount_hired.get().replace(" ", "")) > 500:
            Label(main_canvas, text="Between 1-500", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
            error_messages.append("Amount Hired must be between 1 and 500.")
            entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True
    else:
        try:
            # Check if the "amount_hired" entry is a decimal number.
            amount_float = float(amount_hired.get().strip().replace(" ", ""))   # Convert "amount_hired" to a float and store the value in "amount_float".
            amount_int = int(amount_float)                                      # Convert "amount_float" to an integer and store the value in "amount_int".

            # Check if the float and integer are not equal, meaning the entry would be a decimal. Otherwise check if ".0" is in the entry, also suggesting a decimal.
            if amount_float != amount_int or ".0" in amount_hired.get() and amount_float == amount_int: 
                Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
                error_messages.append("Amount Hired cannot be a decimal.\n     - Must be an integer between 1 and 500.")
                entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
                details_error_detected = True
            
            # Check if the "amount_hired" entry doesn't only consist of digits.
            elif not amount_hired.get().strip().replace(" ", "").isdigit():
                Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
                error_messages.append("Amount Hired must only include numbers.\n     - Cannot include symbols or non-numeric characters.")
                entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
                details_error_detected = True

        except ValueError:
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=W)
            error_messages.append("Amount Hired must only include numbers.\n     - Cannot include symbols or non-numeric characters.")
            entry_clear.append(amount_hired)  # Allow the entry to be cleared after closing the warning box by placing it in a list till the end of the function.
            details_error_detected = True

    # If there are any invalid inputs, show a message box with all errors.
    if details_error_detected == True:
        ordered_errors = [f"{i + 1}. {error_messages[i]}" for i in range(len(error_messages))]  # Create an ordered list version of the errors to display in the warning message box.
        messagebox.showwarning("Invalid Entries", "\n".join(ordered_errors))
        
        # Clear any invalid entries inside the entry boxes after the user closes the message box.
        for entry in entry_clear:
            entry.delete(0, "end")  # Remove the invalid entries from their entry boxes (from the beginning (0) to the end).
    else:
        submit_receipt()


# Function for adding the next customer to the list.
def submit_receipt():
    global remove_treeview

    existing_receipt_numbers = [customer[0] for customer in customer_details]  # Get the existing receipt numbers.

    # Check if the maximum number of unique receipt numbers has been reached.
    if len(existing_receipt_numbers) >= 9000:  # 9000 possible unique 4-digit receipt numbers from 1000 to 9999.
        messagebox.showwarning("Maximum Entries Reached", "No more unique receipt numbers can be generated. Please delete old entries to add new ones.")
        return  # Exit the function if no more receipt numbers can be generated.

    while True:
        receipt_number = random.randint(1000, 9999)  # Generate a random number from 1000 to 9999 and put this value into the "receipt_number" variable.
        if receipt_number not in existing_receipt_numbers:  # Check that the generated receipt number doesn't already exist.
            break

    # Remove any leading and trailing spaces from the "amount_hired", "first_name", and "last_name" entries, as well as any spaces in between characters in "amount_hired".
    stripped_amounthired = amount_hired.get().strip().replace(" ", "")
    stripped_firstname = first_name.get().strip()
    stripped_lastname = last_name.get().strip()

    # Split the names into a list of separate word strings if there are multiple words, so that they can be individually capitalised.
    fname_words = stripped_firstname.split()
    lname_words = stripped_lastname.split()

    # Capitalise the first letter of all words in the "first_name" and "last_name" entries while joining the listed words for both entries and adding a space between them.
    formatted_firstname = " ".join(fname_word.capitalize() for fname_word in fname_words)
    formatted_lastname = " ".join(lname_word.capitalize() for lname_word in lname_words)

    # Create a temporary new entry list.
    new_entry = [receipt_number, formatted_firstname, formatted_lastname, item_hired.get(), stripped_amounthired]

    # Check if the new entry matches any existing entry and replace the latest matching entry with the updated entry if the user chooses to do so.
    receipt_replaced = False
    for i in reversed(range(len(customer_details))):  # Use "reversed" so that the newest receipt for the customer can be updated.
        customer = customer_details[i]
        if (customer[1] == formatted_firstname and customer[2] == formatted_lastname and customer[3] == item_hired.get()):
            # Ask user if they want to update the existing receipt. The message box returns True if the answer is "Yes" and False otherwise.
            response = messagebox.askyesno("Update Existing Receipt", "A receipt with the same customer full name and item already exists. Do you want to update the latest existing receipt?")
            if response == True:
                # Replace the old entry with the new one, using [start:stop] slicing technique.
                customer_details[i][4:5] = new_entry[4:5]  # Update just the amount hired (4th item in list).
                receipt_replaced = True
                new_entry = []              # Clear the new entry list so it can be used again.
                save_customer_details()     # Save the "customer_details" list data to the JSON file after appending by using the "save_customer_details()" function.
                break
            else:
                break

    if receipt_replaced == False:
        # If no match was found, add the new entry.
        customer_details.append(new_entry)
        new_entry = []
        save_customer_details()  # Save the "customer_details" list data to the JSON file after appending.

    # Clear the input boxes.
    first_name.delete(0, "end")
    last_name.delete(0, "end")
    item_hired.set("")
    amount_hired.delete(0, "end")

    # Update the entry counter.
    if receipt_replaced == False:
        counter["entry_number"] += 1  # Update the entry number so the user knows what number of entry they will be submitting.
        Label(main_canvas, text=counter["entry_number"], font=("Segoe UI", 10, "bold"), bg=main_canvas_colour, fg="white").grid(column=1, row=0, pady=[15,0])

    # Print customer details only if they are already printed, so that the printed list can be updated.
    for widget in main_window.grid_slaves():
        grid = widget.grid_info()
        if "row" in grid and int(grid["row"]) > 7:  # Check if there are widgets in a row larger than 7, which is where the treeview is displayed.
            remove_treeview = False                 # Set "treeview_displayed" variable/flag to "False" so the treeview can be updated if already printed rather than removing it.
            print_customer_details()                # Print the customer list again to update the treeview with the latest entries.


# Function for checking that the entry inside the receipt deletion entry box is valid.
def validate_receipt_deletion():
    receipt_error_detected = False

    # Clear any previous error messages by using the "clear_widget(column, row)" function.
    clear_widget(2, 1)
    clear_widget(2, 2)
    clear_widget(2, 3)
    clear_widget(2, 4)

    # Check if the "delete_receipt_num" entry is blank.
    if delete_receipt_num.get().strip() == "":
        Label(main_canvas, text="Required", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
        messagebox.showwarning("Invalid Entry", "Receipt Number is required and cannot be left blank.")
        delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
        receipt_error_detected = True

    # Check if the "delete_receipt_num" entry contains any alphabetic characters and doesn't only consist of digits.
    elif any(char.isalpha() for char in delete_receipt_num.get().strip().replace(" ", "")) and not delete_receipt_num.get().strip().replace(" ", "").isdigit():
        Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
        messagebox.showwarning("Invalid Entry", "Receipt Number must only include numbers.\nPlease don't use letters or symbols/non-numeric characters.")
        delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
        receipt_error_detected = True

    # Check if the "delete_receipt_num" entry is a negative number (starting with a minus sign) and has at least one numeric value after it.
    elif delete_receipt_num.get().strip().replace(" ", "").startswith("-") and any(char.isnumeric() for char in delete_receipt_num.get()):
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
            messagebox.showwarning("Invalid Entry", "Receipt Number can only be a positive number.")
            delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
            receipt_error_detected = True

    # Check if the "delete_receipt_num" entry only contains digits and if so, whether the total number of digits is not equal to 4.
    elif delete_receipt_num.get().strip().replace(" ", "").isdigit():
        if not len(delete_receipt_num.get().strip().replace(" ", "")) == 4:
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
            messagebox.showwarning("Invalid Entry", "Receipt Number must only be 4 digits long.")
            delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
            receipt_error_detected = True

    else:
        try:
            # Check if the "delete_receipt_num" entry is a decimal number.
            receipt_num_float = float(delete_receipt_num.get().strip().replace(" ", ""))  # Convert "delete_receipt_num" to a float and store the value in "receipt_num_float".
            receipt_num_int = int(receipt_num_float)                                      # Convert "receipt_num_float" to an integer and store the value in "receipt_num_int".

            # Check if the float and integer are not equal, meaning the input would be a decimal. Otherwise check if ".0" is in the entry, also suggesting a decimal.
            if receipt_num_float != receipt_num_int or ".0" in delete_receipt_num.get() and receipt_num_float == receipt_num_int: 
                Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
                messagebox.showwarning("Invalid Entry", "Receipt Number cannot be a decimal and must\nbe an existing receipt number/integer.")
                delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
                receipt_error_detected = True
            
            # Check if the "delete_receipt_num" entry doesn't only consist of digits.
            elif not delete_receipt_num.get().strip().replace(" ", "").isdigit():
                Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
                messagebox.showwarning("Invalid Entry", "Receipt Number must only include numbers.\nPlease don't use symbols/non-numeric characters.")
                delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
                receipt_error_detected = True 

        except ValueError:
            Label(main_canvas, text="Invalid Entry", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)
            messagebox.showwarning("Invalid Entry", "Receipt Number must only include numbers.\nPlease don't use symbols/non-numeric characters.")
            delete_receipt_num.delete(0, "end")  # Clear the delete_receipt_num entry box.
            receipt_error_detected = True

    # If there is an invalid input, exit the function (error message is already displayed).
    if receipt_error_detected == True:
        return
    else:
        delete_receipt()


# Function for deleting a receipt from the list.
def delete_receipt(event=None):
    global data_loaded, remove_treeview, delkey_binded

    # Remove any leading, in-between, and trailing spaces from the "delete_receipt_num" variable entry.
    stripped_receiptnum = int(delete_receipt_num.get().strip().replace(" ", ""))

    # Enumerate through the customer entries in the "customer_details" list to find the matching receipt number.
    # "i" represents the index of the current customer entry in the "customer_details" list, and "customer" is the current customer entry.
    customer_found = False
    for i, customer in enumerate(customer_details):
        if customer[0] == stripped_receiptnum:  # Check if the receipt number stored in the first element "[0]" of each "customer" list entry matches the stripped user-entered receipt number.
            del customer_details[i]             # If a match is found, delete the customer at index "i" from "customer_details".
            customer_found = True
            if delkey_binded == True:       # If "delkey_binded" variable/flag is True, unbind the "del" key so that it doesn't work when no treeview item is selected.
                tree.unbind("<Delete>")
            delkey_binded = False           # Set "delkey_binded" variable/flag to False so program won't try to unbind the "del" key if it hasn't been binded already.
            data_loaded = False             # Set the "data_loaded" variable to false, so that the program will reload data from JSON file when printing.
            counter["entry_number"] -= 1    # Update the entry number so the user knows what number of entry they will be submitting.
            Label(main_canvas, text=counter["entry_number"], font=("Segoe UI", 10, "bold"), bg=main_canvas_colour, fg="white").grid(column=1, row=0, pady=[15,0])
            delete_receipt_num.delete(0, "end")             # Remove the value in the "delete_receipt_num" entry box (from the beginning (0) to the end).
            save_customer_details()                         # Update the JSON file with the latest customer list.         
            if len(customer_details) <= 0:                  # Check if the "customer_details" list is empty so that the printed list can be removed after.
                for widget in main_window.grid_slaves():
                    if int(widget.grid_info()["row"]) > 7:  # Check if there are widgets in a row larger than 7, which is where the treeview is displayed.
                        widget.grid_forget()                # Remove the treeview from the grid by forgetting it.
                        remove_treeview = False             # Set "remove_treeview" variable/flag to "False" so the treeview can be printed again next time the print function is run.
            else:
                remove_treeview = False     # Set "remove_treeview" variable/flag to "False" so the treeview can be updated if already printed rather than removing it.
                print_customer_details()    # Print the customer list again to update the treeview with the latest entries.

    # Display an error label if the customer receipt entered wasn't found in the list of existing customer receipts.
    if not customer_found:
        Label(main_canvas, text="Receipt not found", bg=main_canvas_colour, fg="red").grid(column=2, row=4, sticky=E)

# Function for adding the banner image to the canvas.
def setup_banner(canvas):
    global banner  # Keep a reference to the image object so that it appears.
    banner = PhotoImage(file="Images/Banner_V2.png")    # Add the banner image file directory.
    canvas.create_image(0, 0, anchor=NW, image=banner)  # Add the image to the canvas.


# Function for setting up the UI elements consisting of images, labels, entry boxes, combo boxes, spin boxes, and buttons.
def setup_elements():
    global main_canvas, main_canvas_colour, canvas_image, first_name, last_name, item_hired, amount_hired, delete_receipt_num, left_image, right_image

    # Create a canvas for the main entry section.
    main_canvas_colour = "#a7acd0"  # Set the colour of the main canvas so that other elements can use it.
    main_canvas = Canvas(main_window, bg=main_window_bg, bd=0, highlightthickness=0)
    main_canvas.grid(row=1, column=1, columnspan=4, rowspan=7, pady=[0, 20])

    # Add the image as a background for the main canvas.
    canvas_image = PhotoImage(file="Images/Main_Canvas_Image.png")  # Add the canvas image file directory.
    main_canvas.create_image(0, 0, anchor=NW, image=canvas_image)  # Add the image to the canvas.

    # Set width for columns 0-3 (4 total) in the main canvas.
    main_canvas.columnconfigure(0, weight=0, minsize=150)
    main_canvas.columnconfigure(1, weight=0, minsize=150)
    main_canvas.columnconfigure(2, weight=0, minsize=150)
    main_canvas.columnconfigure(3, weight=0, minsize=150)

    # Create the left-side canvas.
    left_canvas = Canvas(main_window, bg="#B4B9DE", width=150, height=278, bd=0, highlightthickness=0)
    left_canvas.grid(row=1, column=0, rowspan=7, sticky=NSEW)

    # Create the right-side sanvas.
    right_canvas = Canvas(main_window, bg="#B4B9DE", width=150, height=278, bd=0, highlightthickness=0)
    right_canvas.grid(row=1, column=5, rowspan=7, sticky=NSEW)

    # Add the image to the left-side canvas.
    left_image = PhotoImage(file="Images/Balloons.png")
    left_canvas.create_image(0, 0, anchor=NW, image=left_image)

    # Add the image to the left-side canvas.
    right_image = PhotoImage(file="Images/Balloons.png")
    right_canvas.create_image(0, 0, anchor=NW, image=right_image)    

    # Create the labels to be placed next to their relevant entry boxes.
    Label(main_canvas, text="Entry Number", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=0, sticky=E, padx=5, pady=[15,0])
    Label(main_canvas, text=counter["entry_number"], bg=main_canvas_colour, fg="white", font=("Segoe UI", 10, "bold")).grid(column=1, row=0, pady=[15,0])
    Label(main_canvas, text="First Name", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=1, sticky=E, padx=5, pady=5)
    Label(main_canvas, text="Last Name", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=2, sticky=E, padx=5, pady=5)
    Label(main_canvas, text="Item Hired", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=3, sticky=E, padx=5, pady=5)
    Label(main_canvas, text="Amount Hired", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=4, sticky=E, padx=5, pady=5)
    Label(main_canvas, text="Receipt No.", bg=main_canvas_colour, font=("Segoe UI", 10, "bold"), fg="white").grid(column=3, row=3, sticky=EW, padx=[5,15])

    # Create a style for the Combobox and Spinbox.
    combostyle = ttk.Style()
    spinboxstyle = ttk.Style()
    combostyle.theme_use("default")    # Make the program use the default theme that supports custom styling for the Combobox.
    spinboxstyle.theme_use("default")  # Make the program use the default theme that supports custom styling for the Spinbox.

    # Configure the custom Combobox style
    combostyle.configure("custom.TCombobox",
                        fieldbackground="#979BBA",  # Background colour of the entry field.
                        background="#8183b2",       # Background colour of the dropdown arrow.
                        foreground="white",         # Text colour in the entry field.
                        arrowcolor="white",         # Dropdown arrow colour.
                        selectbackground="#faf1c0",     # Text selection background colour.
                        selectforeground="black",       # Text colour while selected.
                        selectborderwidth=0,            # Text selection border width.
                        insertwidth=2,              # Text cursor width.
                        insertcolor="white")        # Text cursor colour.

    # Map the custom style for the readonly combobox state.
    combostyle.map("custom.TCombobox",
                fieldbackground=[("readonly", "#979BBA")],      # Background colour for readonly state.
                background=[("readonly", "#8183b2")],           # Background colour of the dropdown arrow for readonly state.
                selectbackground=[("readonly", "#979BBA")],     # Make readonly selection colour same as background so it doesn't appear selected.
                selectforeground=[("readonly", "white")])       # Make the text white for the readonly selected text.

    # Configure the custom Spinbox style
    spinboxstyle.configure("custom.TSpinbox",
                        fieldbackground="#979BBA",  # Background colour of the entry field.
                        background="#8183b2",       # Background colour of the dropdown arrow.
                        foreground="white",         # Text colour in the entry field.
                        arrowcolor="white",         # Dropdown arrow colour.
                        selectbackground="#faf1c0",     # Text selection background colour.
                        selectforeground="black",       # Text colour while selected.
                        selectborderwidth=0,            # Text selection border width.
                        insertwidth=2,              # Typing cursor width.
                        insertcolor="white")        # Typing cursor colour.

    # Setup entry boxes, comboboxes and spinboxes.
    first_name = Entry(main_canvas, bg="#979BBA", fg="white", selectbackground="#facbe9", selectforeground="black", insertwidth=2)
    first_name.grid(column=1, row=1, padx=5, sticky=EW)
    first_name.config(insertbackground="white")
    last_name = Entry(main_canvas, bg="#979BBA", fg="white", selectbackground="#c2eaf3", selectforeground="black", insertwidth=2)
    last_name.grid(column=1, row=2, padx=5, sticky=EW)
    last_name.config(insertbackground="white")
    item_hired = ttk.Combobox(main_canvas, values = item_list, style="custom.TCombobox", state="readonly")
    item_hired.grid(column=1, row=3, padx=5, sticky=EW)
    amount_hired = ttk.Spinbox(main_canvas, from_=1, to=500, style="custom.TSpinbox")
    amount_hired.grid(column=1, row=4, padx=5, sticky=EW)
    delete_receipt_num = Entry(main_canvas, bg="#979BBA", fg="white", selectbackground="#faf1c0", selectforeground="black", insertwidth=2)
    delete_receipt_num.grid(column=3, row=4, padx=[5,15], sticky=EW)
    delete_receipt_num.config(insertbackground="white")

    # Specify the images to use for each button in normal and clicked states.
    main_canvas.btn_img1_normal = PhotoImage(file="Images/Buttons/Exit.png")
    main_canvas.btn_img1_clicked = PhotoImage(file="Images/Buttons/Exit_Clicked.png")
    main_canvas.btn_img2_normal = PhotoImage(file="Images/Buttons/Delete.png")
    main_canvas.btn_img2_clicked = PhotoImage(file="Images/Buttons/Delete_Clicked.png")
    main_canvas.btn_img3_normal = PhotoImage(file="Images/Buttons/Submit.png")
    main_canvas.btn_img3_clicked = PhotoImage(file="Images/Buttons/Submit_Clicked.png")
    main_canvas.btn_img4_normal = PhotoImage(file="Images/Buttons/Print.png")
    main_canvas.btn_img4_clicked = PhotoImage(file="Images/Buttons/Print_Clicked.png")

    # Create frames for each image button to be packed into.
    img_frame1 = Frame(main_canvas, width=23, bg=main_canvas_colour)
    img_frame1.grid(column=3, row=0, sticky=EW, padx=[5,15], pady=[15,5])
    img_frame2 = Frame(main_canvas, width=23, bg=main_canvas_colour)
    img_frame2.grid(column=3, row=5, sticky=EW, padx=[5,15], pady=5)
    img_frame3 = Frame(main_canvas, width=23, bg=main_canvas_colour)
    img_frame3.grid(column=1, row=5, sticky=EW, pady=5)
    img_frame4 = Frame(main_canvas, width=23, bg=main_canvas_colour)
    img_frame4.grid(column=1, row=6, sticky=EW, pady=[5,15])

    def on_button_press(button, clicked_img):  # Define the "on_button_press" function to handle button presses for the clicked button image to appear.
        button.config(image=clicked_img)
        button.image = clicked_img
        button._is_pressed = True

    def on_button_release(button, normal_img):  # Define the "on_button_release" function to handle button releases for the normal button image to appear.
        button.config(image=normal_img)
        button.image = normal_img
        button._is_pressed = False

    def on_button_enter(button, clicked_img, normal_img):   # Define the "on_button_enter" function to handle the mouse entering the button while clicked for the clicked button image to appear.
        if getattr(button, "_is_pressed", True):            # Check if the button is being pressed/held down.
            button.config(image=clicked_img)
            button.image = clicked_img
        else:
            button.config(image=normal_img)
            button.image = normal_img

    def on_button_leave(button, normal_img):        # Define the "on_button_leave" function to handle the mouse leaving the button while clicked for the normal button image to appear.
        if getattr(button, "_is_pressed", True):    # Check if the button is being pressed/held down.
            button.config(image=normal_img)
            button.image = normal_img

    def handle_button_click(action):
        # Execute the action associated with the button.
        action()

    # Create the image buttons.
    # Exit Program Button.
    img_button1 = Button(img_frame1, command=lambda: handle_button_click(quit_program), width=140, image=main_canvas.btn_img1_normal,
                        bg=main_canvas_colour, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_canvas_colour, activeforeground=main_canvas_colour)
    img_button1.image = main_canvas.btn_img1_normal  # Store the image reference to prevent garbage collection from causing it to disappear.
    img_button1.bind("<Button-1>", lambda e: on_button_press(img_button1, main_canvas.btn_img1_clicked))                            # Bind button press to left mouse click event to change image to the clicked version.
    img_button1.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button1, main_canvas.btn_img1_normal))                    # Bind button release to left click release event to revert the image.
    img_button1.bind("<Enter>", lambda e: on_button_enter(img_button1, main_canvas.btn_img1_clicked, main_canvas.btn_img1_normal))  # Bind the mouse enter event while clicked to change image to clicked version.
    img_button1.bind("<Leave>", lambda e: on_button_leave(img_button1, main_canvas.btn_img1_normal))                                # Bind the mouse leave event while clicked to revert the image.
    img_button1.pack()                  # Pack the Exit button into its frame/container.
    img_button1._is_pressed = False     # Set the initial pressed state variable to "False" so that it isn't automatically set to "True" and doesn't cause the button image to be a clicked state when hovered over.

    # Delete Receipt Button.
    img_button2 = Button(img_frame2, command=lambda: handle_button_click(validate_receipt_deletion), width=140, image=main_canvas.btn_img2_normal,
                        bg=main_canvas_colour, fg="white", font=("Helvetica 10 bold"), borderwidth=0, compound="center", relief="flat",
                        activebackground=main_canvas_colour, activeforeground=main_canvas_colour)
    img_button2.image = main_canvas.btn_img2_normal  # Store the image reference to prevent garbage collection from causing it to disappear.
    img_button2.bind("<Button-1>", lambda e: on_button_press(img_button2, main_canvas.btn_img2_clicked))                            # Bind button press to left mouse click event to change image to the clicked version.
    img_button2.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button2, main_canvas.btn_img2_normal))                    # Bind button release to left click release event to revert the image.
    img_button2.bind("<Enter>", lambda e: on_button_enter(img_button2, main_canvas.btn_img2_clicked, main_canvas.btn_img2_normal))  # Bind the mouse enter event while clicked to change image to clicked version.
    img_button2.bind("<Leave>", lambda e: on_button_leave(img_button2, main_canvas.btn_img2_normal))                                # Bind the mouse leave event while clicked to revert the image.
    img_button2.pack()                  # Pack the Delete Receipt button into its frame/container.
    img_button2._is_pressed = False     # Set the initial pressed state variable to "False" so that it isn't automatically set to "True" and doesn't cause the button image to be a clicked state when hovered over.

    # Submit Details Button.
    img_button3 = Button(img_frame3, command=lambda: handle_button_click(validate_customer_details), width=140, image=main_canvas.btn_img3_normal,
                        bg=main_canvas_colour, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_canvas_colour, activeforeground=main_canvas_colour)
    img_button3.image = main_canvas.btn_img3_normal  # Store the image reference to prevent garbage collection from causing it to disappear.
    img_button3.bind("<Button-1>", lambda e: on_button_press(img_button3, main_canvas.btn_img3_clicked))                            # Bind button press to left mouse click event to change image to the clicked version.
    img_button3.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button3, main_canvas.btn_img3_normal))                    # Bind button release to left click release event to revert the image.
    img_button3.bind("<Enter>", lambda e: on_button_enter(img_button3, main_canvas.btn_img3_clicked, main_canvas.btn_img3_normal))  # Bind the mouse enter event while clicked to change image to clicked version.
    img_button3.bind("<Leave>", lambda e: on_button_leave(img_button3, main_canvas.btn_img3_normal))                                # Bind the mouse leave event while clicked to revert the image.
    img_button3.pack()                  # Pack the Submit Details button into its frame/container.
    img_button3._is_pressed = False     # Set the initial pressed state variable to "False" so that it isn't automatically set to "True" and doesn't cause the button image to be a clicked state when hovered over.

    # Print Details Button.
    img_button4 = Button(img_frame4, command=lambda: handle_button_click(print_customer_details), width=140, image=main_canvas.btn_img4_normal,
                        bg=main_canvas_colour, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_canvas_colour, activeforeground=main_canvas_colour)
    img_button4.image = main_canvas.btn_img4_normal  # Store the image reference to prevent garbage collection from causing it to disappear.
    img_button4.bind("<Button-1>", lambda e: on_button_press(img_button4, main_canvas.btn_img4_clicked))                            # Bind button press to left mouse click event to change image to the clicked version.
    img_button4.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button4, main_canvas.btn_img4_normal))                    # Bind button release to left click release event to revert the image.
    img_button4.bind("<Enter>", lambda e: on_button_enter(img_button4, main_canvas.btn_img4_clicked, main_canvas.btn_img4_normal))  # Bind the mouse enter event while clicked to change image to clicked version.
    img_button4.bind("<Leave>", lambda e: on_button_leave(img_button4, main_canvas.btn_img4_normal))                                # Bind the mouse leave event while clicked to revert the image.
    img_button4.pack()                  # Pack the Print Details button into its frame/container.
    img_button4._is_pressed = False     # Set the initial pressed state variable to "False" so that it isn't automatically set to "True" and doesn't cause the button image to be a clicked state when hovered over.


# Main function for starting the program.
def main(): 
    banner_canvas = Canvas(main_window, bg="#B4B9DE", width=917, height=232, bd=0, highlightthickness=0)  # Create a canvas for the banner image.
    banner_canvas.grid(row=0, column=0, columnspan=6, sticky=EW, pady=(2,20))
    setup_banner(banner_canvas)  # Call the setup_banner function to add the banner image.

    # Start the primary GUI functions.
    load_customer_details()
    setup_elements()

    main_window.mainloop()


#Initialise the main window.
main_window = Tk()
main_window.title("Julie's Party Hire Store")  # Set the title of the window.
main_window.iconphoto(False, PhotoImage(file="Images/Pgm_Icon.png"))  # Set the title bar icon.
main_window.resizable(False, False)         # Set the resizable property for height and width to False.
main_window_bg = "#B4B9DE"                  # Set the background colour of the main window.
main_window.configure(bg=main_window_bg)    # Configure the main window to use the background colour (value) of the "main_window_bg variable".

# Set width for columns 0-5 (6 total) in the main window.
main_window.columnconfigure(0, weight=0, minsize=150)
main_window.columnconfigure(1, weight=0, minsize=150)
main_window.columnconfigure(2, weight=0, minsize=150)
main_window.columnconfigure(3, weight=0, minsize=150)
main_window.columnconfigure(4, weight=0, minsize=150)
main_window.columnconfigure(5, weight=0, minsize=150)

# Initialise global lists and variables.
counter = {"entry_number": 1}   # Initialise the entry number counter at 1.
customer_details = []           # Create empty list for customer details so that the entered details can be stored inside.
item_list = ["Knives", "Forks", "Spoons", "Paper Plates", "Paper Bowls", "Paper Cups", "Balloons", "Party Hats"]  # Create a list of all the available items for hire.
data_loaded = False         # Initialise a flag to track whether the JSON file data has been loaded, setting it to False so that the program will reload data from the file when printing.
remove_treeview = False     # Initialise a flag to track whether the Treeview is displayed so that the print button can alternate between printing and removing the treeview.
delkey_binded = False       # Initialise a flag to track if the "del" key is binded to the "delete_receipt" function so that it only binds when a treeview item is selected.

# Run the main function.
main()