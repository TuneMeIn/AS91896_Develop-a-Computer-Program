import os
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

# Quit function
def quit():
    main_window.destroy()


# Function to update the receipt numbers in the combo box
def update_receipt_combo():
    # Clear the current list of receipt numbers in the combo box
    delete_receipt_num["values"] = []
    
    # Add the current receipt numbers from customer_details to the receipt deletion combo box
    receipt_numbers = [str(customer[0]) for customer in customer_details]
    delete_receipt_num["values"] = receipt_numbers

    # Reset the selected value to an empty string
    delete_receipt_num.set("")


# Load customer details from .json file and update the receipt deletion combo box with the existing receipt numbers
def load_customer_details():
        global data_loaded, customer_details
        with open("customer_receipts.json", "r") as file:  # Open the .json file for reading (r) in binary mode (b)
            if os.path.getsize("customer_receipts.json") <= 18:  # Check that the .json file isn't below or equal to 18 bytes, indicating that it has no complete list data
                return
            else:
                customer_details.clear  # Clear the list to prevent duplicate entries
                customer_details = json.load(file)  # Load the details from the .json file into the "customer_details" list
                data_loaded = True  # Set the "data_loaded" variable to True, so program doesn't reload data before printing
                counter["entry_number"] = len(customer_details) + 1
                update_receipt_combo()  # Update the combo box with current receipt numbers


# Save customer details to .json file
def save_customer_details():
    global data_loaded
    with open("customer_receipts.json", "w") as file:
        json.dump(customer_details, file, indent=4)  # Dump the entries from the "customer_details" list into the .json file
    data_loaded = False  # Set the data_loaded variable to false, so program will reload data from .json file when printing


# Print details of all the customers
def print_customer_details():
    global printed_data, lis_customer_details
    if not data_loaded:
        load_customer_details()  # Reload the "customer_details" list from the .json file if not up-to-date, so there are no conflicting items
    if len(customer_details) <= 0:
        return  # Exit the function if the "customer_details" list is empty (<= 0) to avoid printing the headers without any list items
    else:
        # Set width for columns 0-5 (6 total) in the main window
        main_window.columnconfigure(0, weight=0, minsize=150)
        main_window.columnconfigure(1, weight=0, minsize=150)
        main_window.columnconfigure(2, weight=0, minsize=150)
        main_window.columnconfigure(3, weight=0, minsize=150)
        main_window.columnconfigure(4, weight=0, minsize=150)
        main_window.columnconfigure(5, weight=0, minsize=150)

        # Clear previous entries
        for widget in main_window.grid_slaves():
            if int(widget.grid_info()["row"]) > 8:  # Check if the widget is in a row larger than 8, which is where customer details are displayed.
                widget.grid_forget()  # Remove the widget from the grid by forgetting it

        # Create the column headings
        Label(main_window, font=("Helvetica 10 bold"), text="Entry", bg=main_window_bg_color, fg="white").grid(column=0, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Receipt No.", bg=main_window_bg_color, fg="white").grid(column=1, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="First Name", bg=main_window_bg_color, fg="white").grid(column=2, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Last Name", bg=main_window_bg_color, fg="white").grid(column=3, row=8, padx=5, pady=5)        
        Label(main_window, font=("Helvetica 10 bold"), text="Item Hired", bg=main_window_bg_color, fg="white").grid(column=4, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Amount Hired", bg=main_window_bg_color, fg="white").grid(column=5, row=8, padx=5, pady=5)

        # Add each item in the list into its own row
        for index, details in enumerate(customer_details):
            list_row = index + 9
            custom_firstname = details[1]
            custom_lastname = details[2]

            # Truncate the first name if "formatted_firstname" exceeds 15 characters by slicing the string (sequence[start:stop:step])
            if len(details[1]) >= 15:
                custom_firstname = (details[1])[:12] + "..."
            
            # Truncate the last name if "formatted_lastname" exceeds 15 characters by slicing the string (sequence[start:stop:step])
            if len(details[2]) >= 15:
                custom_lastname = (details[2])[:12] + "..."
            
            Label(main_window, text=index + 1, bg=main_window_bg_color, fg="white").grid(column=0, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[0], bg=main_window_bg_color, fg="white").grid(column=1, row=list_row, padx=5, pady=5)
            Label(main_window, text=custom_firstname, bg=main_window_bg_color, fg="white").grid(column=2, row=list_row, padx=5, pady=5)
            Label(main_window, text=custom_lastname, bg=main_window_bg_color, fg="white").grid(column=3, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[3], bg=main_window_bg_color, fg="white").grid(column=4, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[4], bg=main_window_bg_color, fg="white").grid(column=5, row=list_row, padx=5, pady=5)


# Check the inputs are all valid
def validate_inputs():
    error_detected_check = 0
    error_messages = []  # List to store error messages

    # Clear any previous error messages
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=2, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=3, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=4, sticky=E)
    Label(main_window, text="                                       ", bg=main_window_bg_color).grid(column=2, row=4, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=5, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=5, sticky=E)

    # Check if the "first_name" entry is blank
    if first_name.get().strip() == "":
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("First Name is required and cannot be left blank")
        first_name.delete(0, "end")  # Clear the first_name entry box
        error_detected_check = 1

    # Check if the "first_name" entry is above 50 characters long
    elif len(first_name.get().strip()) > 50:
        Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("First Name cannot be longer than 50 characters")
        first_name.delete(0, "end")  # Clear the first_name entry box
        error_detected_check = 1        

    # Check if the "first_name" entry only contains digits
    elif first_name.get().isdigit():
        Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=2, sticky=W)
        error_messages.append("First Name cannot only contain numbers.\n     - Please include at least one letter")
        first_name.delete(0, "end")  # Clear the first_name entry box
        error_detected_check = 1

    # Check if "first_name" contains a combination of letters and numbers as well as at least one letter.
    else:
        if not (first_name.get().replace(" ", "").isalnum() and any(char.isalpha() for char in first_name.get())):
            Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=2, sticky=W)
            error_messages.append("First Name can only include letters or letters with numbers.\n     - No symbols or non-alphanumeric characters.")
            first_name.delete(0, "end")  # Clear the first_name entry box
            error_detected_check = 1

    # Check if the "last_name" entry is blank
    if last_name.get().strip() == "":
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=3, sticky=W)
        error_messages.append("Last Name is required and cannot be left blank")
        last_name.delete(0, "end")  # Clear the last_name entry box
        error_detected_check = 1

    # Check if the "last_name" entry is above 50 characters long
    elif len(last_name.get().strip()) > 50:
        Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=3, sticky=W)
        error_messages.append("Last Name cannot be longer than 50 characters")
        last_name.delete(0, "end")  # Clear the last_name entry box
        error_detected_check = 1

    # Check if the "last_name" entry only contains digits
    elif last_name.get().isdigit():
        Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=3, sticky=W)
        error_messages.append("Last Name cannot only contain numbers.\n     - Please include at least one letter")
        last_name.delete(0, "end")  # Clear the last_name entry box
        error_detected_check = 1

    # Check if "last_name" contains a combination of letters and numbers as well as at least one letter.
    else:
        if not (last_name.get().replace(" ", "").isalnum() and any(char.isalpha() for char in last_name.get())):
            Label(main_window, text="Invalid Entry", bg=main_window_bg_color, fg="red").grid(column=2, row=3, sticky=W)
            error_messages.append("Last Name can only include letters or letters with numbers.\n     - No symbols or non-alphanumeric characters.")
            last_name.delete(0, "end")  # Clear the last_name entry box
            error_detected_check = 1

    # Check the item hired is not blank, set error text if blank
    if len(item_hired.get()) == 0:
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=4, sticky=W)
        error_messages.append("Item Hired is required")
        item_hired.delete(0, "end")
        error_detected_check = 1

    # Check that the amount hired is not blank and above 0, set error text if blank or 0 and below
    if len(amount_hired.get()) == 0:
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=5, sticky=W)
        error_messages.append("Amount Hired is required")
        amount_hired.delete(0, "end")
        error_detected_check = 1
    elif amount_hired.get().isdigit():
        if int(amount_hired.get()) <= 0 or int(amount_hired.get()) > 500:
            Label(main_window, text="Between 1-500", bg=main_window_bg_color, fg="red").grid(column=2, row=5, sticky=W)
            error_messages.append("Amount Hired must be between 1 and 500")
            amount_hired.delete(0, "end")
            error_detected_check = 1
    else:
        error_messages.append("Amount Hired must be a number")
        amount_hired.delete(0, "end")
        error_detected_check = 1

    # If there are any invalid inputs, show a message box with all errors
    if error_detected_check == 1:
        ordered_errors = [f"{i + 1}. {error_messages[i]}" for i in range(len(error_messages))]  # Create an ordered list version of the errors to display in the warning message box
        messagebox.showwarning("Invalid Entries", "\n".join(ordered_errors))
    else:
        submit_receipt()

# Add the next customer to the list
def submit_receipt():
    # Generate a random 4-digit receipt number
    existing_receipt_numbers = [customer[0] for customer in customer_details]  # Get the existing receipt numbers
    while True:
        receipt_number = random.randint(1000, 9999)  # Generate a random number from 1000 to 9999 and put this value into the "receipt_number" variable
        if receipt_number not in existing_receipt_numbers:  # Check that the generated receipt number doesn't already exist
            break

    # Remove any leading and trailing spaces from the "first_name" and "last_name" entries.
    stripped_firstname = first_name.get().strip()
    stripped_lastname = last_name.get().strip()

    # Split the names into a list of seperate word strings if there are multiple words, so that they can be individually capitalised.
    fname_words = stripped_firstname.split()
    lname_words = stripped_lastname.split()

    # Capitalise the first letter of all words in the "first_name" and "last_name" entries while joining the listed words for both entries and adding a space between them.
    formatted_firstname = " ".join(fn_word.capitalize() for fn_word in fname_words)
    formatted_lastname = " ".join(ln_word.capitalize() for ln_word in lname_words)

    # Append each item to its own area of the list
    customer_details.append([receipt_number, formatted_firstname, formatted_lastname, item_hired.get(), amount_hired.get()])
    save_customer_details()  # Save data to .json file after appending

    # Clear the entry boxes
    first_name.delete(0, "end")
    last_name.delete(0, "end")
    item_hired.delete(0, "end")
    amount_hired.delete(0, "end")

    # Update the entry counter
    counter["entry_number"] += 1
    Label(main_window, text=counter["entry_number"], font=("Segoe UI", 10, "bold"), bg=main_window_bg_color, fg="white").grid(column=1, row=1)

    # Update the combo box with current receipt numbers
    update_receipt_combo()


# Delete a receipt from the list
def delete_receipt():
    global data_loaded

    # Check that the receipt deletion entry is not blank. Set error text and clear the other entry boxes' error messages if blank.
    if len(delete_receipt_num.get()) == 0:
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=2, sticky=W)
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=3, sticky=W)
        Label(main_window, text="                                       ", bg=main_window_bg_color).grid(column=2, row=4, sticky=W)
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=5, sticky=W)
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=5, sticky=E)   
    else:
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=5, sticky=E)

        # Convert the delete receipt number entry to an integer
        receipt_num_to_delete = int(delete_receipt_num.get())

        # Find the customer with the matching receipt number
        customer_found = False
        for i, customer in enumerate(customer_details):
            if customer[0] == receipt_num_to_delete:  # Compare with the receipt number
                del customer_details[i]
                customer_found = True
                data_loaded = False  # Set the data_loaded variable to false, so program will reload data from .json file when printing
                counter["entry_number"] -= 1
                Label(main_window, text=counter["entry_number"], font=("Segoe UI", 10, "bold"), bg=main_window_bg_color, fg="white").grid(column=1, row=1)
                delete_receipt_num.delete(0, "end")
                save_customer_details()
                update_receipt_combo()
                if len(customer_details) <= 0:
                    # Clear previous entries
                    for widget in main_window.grid_slaves():
                        if int(widget.grid_info()["row"]) > 7:  # Checks if the widget is in a row larger than 8, which is where customer details are displayed.
                            widget.grid_forget()  # Remove the widget from the grid by forgetting it
                else:
                    print_customer_details()
                break
        if not customer_found:
            Label(main_window, text="Receipt not found", bg=main_window_bg_color, fg="red").grid(column=2, row=5, sticky=E)


# Add the banner image
def setup_bg(canvas):
    # Add image file
    global bg  # Keep a reference to the image object
    bg = PhotoImage(file="Images/Banner.png")

    # Show image using label
    canvas.create_image(0, 0, anchor=NW, image=bg)


# Create the buttons and labels
def setup_elements():

    # Specify the images to use for each button in normal and clicked states
    main_window.btn_img1_normal = PhotoImage(file="Images/Buttons/Exit.png")
    main_window.btn_img1_clicked = PhotoImage(file="Images/Buttons/Exit_Clicked.png")
    main_window.btn_img2_normal = PhotoImage(file="Images/Buttons/Delete.png")
    main_window.btn_img2_clicked = PhotoImage(file="Images/Buttons/Delete_Clicked.png")
    main_window.btn_img3_normal = PhotoImage(file="Images/Buttons/Submit.png")
    main_window.btn_img3_clicked = PhotoImage(file="Images/Buttons/Submit_Clicked.png")
    main_window.btn_img4_normal = PhotoImage(file="Images/Buttons/Print.png")
    main_window.btn_img4_clicked = PhotoImage(file="Images/Buttons/Print_Clicked.png")

    # Create the labels
    Label(main_window, text="Entry Number", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=1, sticky=E, padx=5, pady=5)    
    Label(main_window, text="First Name", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=2, sticky=E, padx=5, pady=5)
    Label(main_window, text="Last Name", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=3, sticky=E, padx=5, pady=5)
    Label(main_window, text=counter["entry_number"], bg=main_window_bg_color, fg="white", font=("Segoe UI", 10, "bold")).grid(column=1, row=1)
    Label(main_window, text="Item Hired", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=4, sticky=E, padx=5, pady=5)
    Label(main_window, text="Amount Hired", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=5, sticky=E, padx=5, pady=5)
    Label(main_window, text="Receipt No.", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=3, row=4, sticky=EW, padx=5, pady=5)

    # Create a frame for the image buttons
    img_frame1 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame1.grid(column=3, row=1, sticky=EW, pady=5)
    img_frame2 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame2.grid(column=3, row=6, sticky=EW, pady=5)
    img_frame3 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame3.grid(column=1, row=6, sticky=EW, pady=5)
    img_frame4 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame4.grid(column=1, row=7, sticky=EW, pady=[5,15])

    def on_button_press(button, clicked_img):
        button.config(image=clicked_img)
        button.image = clicked_img
        button._is_pressed = True

    def on_button_release(button, normal_img):
        button.config(image=normal_img)
        button.image = normal_img
        button._is_pressed = False

    def on_button_enter(button, clicked_img, normal_img):
        if getattr(button, "_is_pressed", False):  # Check if the button is pressed
            button.config(image=clicked_img)
            button.image = clicked_img
        else:
            button.config(image=normal_img)
            button.image = normal_img

    def on_button_leave(button, normal_img):
        if getattr(button, "_is_pressed", False):  # Check if the button is pressed
            button.config(image=normal_img)
            button.image = normal_img

    def handle_button_click(action):
        # Execute the action associated with the button
        action()

    # Create the image buttons
    # Exit Program Button
    img_button1 = Button(img_frame1, command=lambda: handle_button_click(main_window.quit), width=140, image=main_window.btn_img1_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button1.image = main_window.btn_img1_normal  # Store the image reference to prevent garbage collection from causing it to disappear
    img_button1.bind("<Button-1>", lambda e: on_button_press(img_button1, main_window.btn_img1_clicked))  # Bind button press to left mouse click event to change image to the clicked version
    img_button1.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button1, main_window.btn_img1_normal))  # Bind button release to left click release event to revert the image
    img_button1.bind("<Enter>", lambda e: on_button_enter(img_button1, main_window.btn_img1_clicked, main_window.btn_img1_normal))  # Bind the mouse enter event while clicked to change image to clicked version
    img_button1.bind("<Leave>", lambda e: on_button_leave(img_button1, main_window.btn_img1_normal))  # Bind the mouse leave event while clicked to revert the image
    img_button1.pack(fill="x")  # Pack the exit button to fill the horizontal space of its container

    # Delete Receipt Button
    img_button2 = Button(img_frame2, command=lambda: handle_button_click(delete_receipt), width=140, image=main_window.btn_img2_normal,
                        bg=main_window_bg_color, fg="white", font=("Helvetica 10 bold"), borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button2.image = main_window.btn_img2_normal  # Store the image reference to prevent garbage collection from causing it to disappear
    img_button2.bind("<Button-1>", lambda e: on_button_press(img_button2, main_window.btn_img2_clicked))  # Bind button press to left mouse click event to change image to the clicked version
    img_button2.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button2, main_window.btn_img2_normal))  # Bind button release to left click release event to revert the image
    img_button2.bind("<Enter>", lambda e: on_button_enter(img_button2, main_window.btn_img2_clicked, main_window.btn_img2_normal))  # Bind the mouse enter event while clicked to change image to clicked version
    img_button2.bind("<Leave>", lambda e: on_button_leave(img_button2, main_window.btn_img2_normal))  # Bind the mouse leave event while clicked to revert the image
    img_button2.pack(fill="x")  # Pack the delete button to fill the horizontal space of its container

    # Submit Details Button
    img_button3 = Button(img_frame3, command=lambda: handle_button_click(validate_inputs), width=140, image=main_window.btn_img3_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button3.image = main_window.btn_img3_normal  # Store the image reference to prevent garbage collection from causing it to disappear
    img_button3.bind("<Button-1>", lambda e: on_button_press(img_button3, main_window.btn_img3_clicked))  # Bind button press to left mouse click event to change image to the clicked version
    img_button3.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button3, main_window.btn_img3_normal))  # Bind button release to left click release event to revert the image
    img_button3.bind("<Enter>", lambda e: on_button_enter(img_button3, main_window.btn_img3_clicked, main_window.btn_img3_normal))  # Bind the mouse enter event while clicked to change image to clicked version
    img_button3.bind("<Leave>", lambda e: on_button_leave(img_button3, main_window.btn_img3_normal))  # Bind the mouse leave event while clicked to revert the image
    img_button3.pack(fill="x")  # Pack the submit button to fill the horizontal space of its container

    # Print Details Button
    img_button4 = Button(img_frame4, command=lambda: handle_button_click(print_customer_details), width=140, image=main_window.btn_img4_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button4.image = main_window.btn_img4_normal  # Store the image reference to prevent garbage collection from causing it to disappear
    img_button4.bind("<Button-1>", lambda e: on_button_press(img_button4, main_window.btn_img4_clicked))  # Bind button press to left mouse click event to change image to the clicked version
    img_button4.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button4, main_window.btn_img4_normal))  # Bind button release to left click release event to revert the image
    img_button4.bind("<Enter>", lambda e: on_button_enter(img_button4, main_window.btn_img4_clicked, main_window.btn_img4_normal))  # Bind the mouse enter event while clicked to change image to clicked version
    img_button4.bind("<Leave>", lambda e: on_button_leave(img_button4, main_window.btn_img4_normal))  # Bind the mouse leave event while clicked to revert the image
    img_button4.pack(fill="x")  # Pack the print button to fill the horizontal space of its container

    # Set width for columns 0-3 (4 total) in the main window
    main_window.columnconfigure(0, weight=0, minsize=150)
    main_window.columnconfigure(1, weight=0, minsize=150)
    main_window.columnconfigure(2, weight=0, minsize=150)
    main_window.columnconfigure(3, weight=0, minsize=150)

# Start the program
def main():
    # Create a canvas for the background image
    canvas = Canvas(main_window, width=600, height=76, bg="#B4B9DE", bd=0, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=4, sticky=EW, pady=(2,20), padx=2)

    # Add the background image
    setup_bg(canvas)

    # Start the GUI
    load_customer_details()
    setup_elements()
    main_window.mainloop()


#Initialise the main window
main_window = Tk()
main_window.title("Julie's Party Hire Store")
main_window.iconphoto(False, PhotoImage(file="Images/Pgm_Icon.png"))  # Set the title bar icon
main_window.resizable(False, False)  # Set the resizable property for height and width to False 
main_window_bg_color = "#B4B9DE"  # Set the background color of the main window
main_window.configure(bg=main_window_bg_color)

# Create a style for the Combobox
combostyle = ttk.Style()
spinboxstyle = ttk.Style()
combostyle.theme_use("default")  # Make the program use a theme that supports custom styling
spinboxstyle.theme_use("default")

# Configure the custom combobox style
combostyle.configure("custom.TCombobox",
                     fieldbackground="#979BBA",  # Background colour of the entry field
                     background="#8183b2",      # Background colour of the dropdown arrow
                     foreground="white",        # Text colour in the entry field
                     arrowcolor="white",
                     selectbackground="#faf1c0",  # Selection background colour
                     selectforeground="black",  # Text colour while selected
                     selectborderwidth=0,   # Selection border width
                     insertwidth=2,  # Text cursor width
                     insertcolor="white")  # Text cursor colour     

# Map the custom style for the readonly combobox state
combostyle.map("custom.TCombobox",
               fieldbackground=[("readonly", "#979BBA")],  # Background colour for readonly state
               background=[("readonly", "#8183b2")],  # Background colour of the dropdown arrow for readonly state
               selectbackground=[("readonly", "#979BBA")],  # Make readonly selection colour same as background so it doesn't appear selected
               selectforeground=[("readonly", "white")])  # Make the text white for the readonly selected text

spinboxstyle.configure("custom.TSpinbox",
                    fieldbackground="#979BBA",  # Background colour of the entry field
                    background="#8183b2",      # Background colour of the dropdown arrow
                    foreground="white",        # Text colour in the entry field
                    arrowcolor="white",
                    selectbackground="#faf1c0",  # Selection background colour
                    selectforeground="black",  # Text colour while selected
                    selectborderwidth=0,   # Selection border width
                    insertwidth=2,  # Text cursor width
                    insertcolor="white")  # Text cursor colour  

#Initialise global lists and variables
counter = {"entry_number": 1}
customer_details = []  # Create empty list for customer details and empty variable for entries in the list
del_list = []  # Create empty list for the receipt numbers to be stored inside
item_list = ["Knives", "Forks", "Spoons", "Paper Plates", "Paper Bowls", "Paper Cups", "Balloons", "Party Hats"]  # Create a list of all the available items for hire
data_loaded = False  # Set the data_loaded variable to false, so program will reload data from .json file when printing

#Setup entry boxes
first_name = Entry(main_window, bg="#979BBA", fg="white", selectbackground="#facbe9", selectforeground="black", insertwidth=2)
first_name.grid(column=1, row=2, padx=5, sticky=EW)
first_name.config(insertbackground="white")
last_name = Entry(main_window, bg="#979BBA", fg="white", selectbackground="#c2eaf3", selectforeground="black", insertwidth=2)
last_name.grid(column=1, row=3, padx=5, sticky=EW)
last_name.config(insertbackground="white")
item_hired = ttk.Combobox(main_window, values = item_list, style="custom.TCombobox", state="readonly")
item_hired.grid(column=1, row=4, padx=5, sticky=EW)
amount_hired = ttk.Spinbox(main_window, from_=1, to=500, style="custom.TSpinbox")
amount_hired.grid(column=1, row=5, padx=5, sticky=EW)
delete_receipt_num = ttk.Combobox(main_window, values=del_list, style="custom.TCombobox")
delete_receipt_num.grid(column=3, row=5, padx=5, sticky=EW)

#Run the main function
main()