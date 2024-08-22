# Date Created: 17/06/2024
# Author: Jack Compton
# Purpose: GUI application for Julie's party hire store to keep track of items that are currently hired

from tkinter import *

# Quit subroutine
def quit():
    main_window.destroy()

# Print details of all the customers
def print_customer_details():
    # Clear previous entries
    for widget in main_window.grid_slaves():
        if int(widget.grid_info()["row"]) > 7: # Checks if the widget is in a row larger than 7, which is where customer details are displayed.
            widget.grid_forget() # Remove the widget from the grid by forgetting it

    # Create the column headings
    Label(main_window, font=("Helvetica 10 bold"), text="Receipt No.").grid(column=0, row=7, padx=5, pady=5)
    Label(main_window, font=("Helvetica 10 bold"), text="Customer Name").grid(column=1, row=7, padx=5, pady=5)
    Label(main_window, font=("Helvetica 10 bold"), text="Item Hired").grid(column=2, row=7, padx=5, pady=5)
    Label(main_window, font=("Helvetica 10 bold"), text="Amount Hired").grid(column=3, row=7, padx=5, pady=5)
    
    # Add each item in the list into its own row
    for index, details in enumerate(customer_details):
        list_row = index + 8
        Label(main_window, text=index + 1).grid(column=0, row=list_row, padx=5, pady=5)
        Label(main_window, text=details[0]).grid(column=1, row=list_row, padx=5, pady=5)
        Label(main_window, text=details[1]).grid(column=2, row=list_row, padx=5, pady=5)
        Label(main_window, text=details[2]).grid(column=3, row=list_row, padx=5, pady=5)

# Check the inputs are all valid
def check_inputs():
    input_check = 0
    Label(main_window, text="                    ").grid(column=2, row=0)
    Label(main_window, text="                    ").grid(column=2, row=1)
    Label(main_window, text="                    ").grid(column=2, row=2)
    Label(main_window, text="                    ").grid(column=2, row=3)
    
    # Check that name is not blank, set error text if blank
    if len(customer_name.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=1)
        input_check = 1
    
    # Check the item hired is not blank, set error text if blank
    if len(item_hired.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=2)
        input_check = 1
    
    # Check that the amount hired is not blank and above 0, set error text if blank or 0 and below
    if len(amount_hired.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=3)
        input_check = 1
    elif amount_hired.get().isdigit():
        if int(amount_hired.get()) <= 0 or int(amount_hired.get()) > 500:
            Label(main_window, fg="red", text="Above 0 or 500 max").grid(column=2, row=3)
            input_check = 1

    if input_check == 0:
        append_name()

# Add the next customer to the list
def append_name():
    # Append each item to its own area of the list
    customer_details.append([customer_name.get(), item_hired.get(), amount_hired.get()])
    # Clear the boxes
    customer_name.delete(0, 'end')
    item_hired.delete(0, 'end')
    amount_hired.delete(0, 'end')
    counters['total_entries'] += 1
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=0)

# Delete a receipt from the list
def delete_receipt():
    # Find which row is to be deleted and delete it
    index = int(delete_receipt_num.get()) - 1
    if 0 <= index < len(customer_details):  # Make sure that the index being deleted exists
        del customer_details[index]
        counters['total_entries'] -= 1
        Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=0)
        delete_receipt_num.delete(0, 'end')
        # Print all the items in the list
        print_customer_details()

# Create the buttons and labels
def setup_buttons():

    # Button Image Setup
    main_window.button_image_1 = PhotoImage(file="Images\Delete_Icon.png")

    # Create all the empty and default labels, buttons, and entry boxes. Put them in the correct grid location
    Label(main_window, text="Receipt Number").grid(column=0, row=0, sticky=E, padx=5, pady=5)
    Label(main_window, text="Customer Name").grid(column=0, row=1, sticky=E, padx=5, pady=5)
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=0)
    Button(main_window, text="Quit", font=("Arial 9 bold"), command=quit, bg="crimson", fg="white", width=12).grid(column=3, row=0, sticky=EW, padx=5, pady=5)
    Button(main_window, text="Append Details", command=check_inputs, width=16).grid(column=1, row=4, sticky=EW, padx=5, pady=5)
    Button(main_window, text="Print Details", command=print_customer_details, width=16).grid(column=1, row=5, sticky=EW, padx=5, pady=5)
    Label(main_window, text="Item Hired").grid(column=0, row=2, sticky=E, padx=5, pady=5)
    Label(main_window, text="Amount Hired").grid(column=0, row=3, sticky=E, padx=5, pady=5)
    Label(main_window, text="Receipt No.").grid(column=3, row=2, sticky=EW, padx=5, pady=5)
    
    # Create a frame for the image button
    img_frame = Frame(main_window)
    img_frame.grid(column=3, row=4, sticky=EW, padx=5, pady=5)
    Img_Button = Button(img_frame, text="Delete Receipt", command=delete_receipt, width=60, image=main_window.button_image_1)
    Img_Button.pack()

    Label(main_window, text="               ").grid(column=2, row=0)

    # Set column width globally for columns 0-3
    main_window.columnconfigure(0, weight=0, minsize=120)
    main_window.columnconfigure(1, weight=0, minsize=120)
    main_window.columnconfigure(2, weight=0, minsize=120)
    main_window.columnconfigure(3, weight=0, minsize=120)

# Start the program running
def main():
    # Start the GUI
    setup_buttons()
    main_window.mainloop()

# Create empty list for customer details and empty variable for entries in the list
counters = {'total_entries': 1, 'name_count': 0}
customer_details = []
main_window = Tk()
main_window.title("Julie's Party Hire Store")
customer_name = Entry(main_window)
customer_name.grid(column=1, row=1)
item_hired = Entry(main_window)
item_hired.grid(column=1, row=2)
amount_hired = Entry(main_window, width=20)
amount_hired.grid(column=1, row=3)
delete_receipt_num = Entry(main_window, width=18)
delete_receipt_num.grid(column=3, row=3, padx=5, pady=5)
main()
