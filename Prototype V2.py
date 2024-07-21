from tkinter import *

# Quit subroutine
def quit():
    main_window.destroy()

# Print details of all the customers
def print_customer_details():
    if len(customer_details) <= 0:
        return  # Exit the function if the list is empty to avoid printing the headers without any list items
    else:
        # Clear previous entries
        for widget in main_window.grid_slaves():
            if int(widget.grid_info()["row"]) > 8:  # Checks if the widget is in a row larger than 8, which is where customer details are displayed.
                widget.grid_forget()  # Remove the widget from the grid by forgetting it

        # Create the column headings
        Label(main_window, font=("Helvetica 10 bold"), text="Receipt No.").grid(column=0, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Customer Name").grid(column=1, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Item Hired").grid(column=2, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Amount Hired").grid(column=3, row=8, padx=5, pady=5)

        # Add each item in the list into its own row
        for index, details in enumerate(customer_details):
            list_row = index + 9
            Label(main_window, text=index + 1).grid(column=0, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[0]).grid(column=1, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[1]).grid(column=2, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[2]).grid(column=3, row=list_row, padx=5, pady=5)

# Check the inputs are all valid
def check_inputs():
    input_check = 0
    Label(main_window, text="                    ").grid(column=2, row=1)
    Label(main_window, text="                    ").grid(column=2, row=2)
    Label(main_window, text="                    ").grid(column=2, row=3)
    Label(main_window, text="                                       ").grid(column=2, row=4)

    # Check that name is not blank, set error text if blank
    if len(customer_name.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=2)
        input_check = 1

    # Check the item hired is not blank, set error text if blank
    if len(item_hired.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=3)
        input_check = 1

    # Check that the amount hired is not blank and above 0, set error text if blank or 0 and below
    if len(amount_hired.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=4)
        input_check = 1
    elif amount_hired.get().isdigit():
        if int(amount_hired.get()) <= 0 or int(amount_hired.get()) > 500:
            Label(main_window, fg="red", text="Above 0 or 500 max").grid(column=2, row=4)
            input_check = 1

    if input_check == 0:
        append_receipt()

# Add the next customer to the list
def append_receipt():
    # Append each item to its own area of the list
    customer_details.append([customer_name.get(), item_hired.get(), amount_hired.get()])
    # Clear the boxes
    customer_name.delete(0, 'end')
    item_hired.delete(0, 'end')
    amount_hired.delete(0, 'end')
    counters['total_entries'] += 1
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=1)

# Delete a receipt from the list
def delete_receipt():
    # Find which row is to be deleted and delete it
    index = int(delete_receipt_num.get()) - 1
    if 0 <= index < len(customer_details):  # Make sure that the index being deleted exists
        del customer_details[index]
        counters['total_entries'] -= 1
        Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=1)
        delete_receipt_num.delete(0, 'end')
        if len(customer_details) <= 0: #Check if the list is empty so that if it is, the headers and list items will be deleted rather than just the list items
            # Clear previous entries and headers
            for widget in main_window.grid_slaves():
                if int(widget.grid_info()["row"]) > 7:  # Checks if the widget is in a row larger than 7, which is where list headers and customer details are displayed
                    widget.grid_forget()  # Remove the widget from the grid by forgetting it
        else:
            print_customer_details()

# Add the background image
def setup_bg(canvas):
    # Add image file
    global bg  # Keep a reference to the image object
    bg = PhotoImage(file="Images/Concept-Background-Trials.png")

    # Show image using label
    canvas.create_image(0, 0, anchor=NW, image=bg)

# Create the buttons and labels
def setup_buttons():
    # Button Image Setup
    main_window.button_image_1 = PhotoImage(file="Images/Delete_Icon.png")

    # Create all the empty and default labels, buttons, and entry boxes. Put them in the correct grid location
    Label(main_window, text="Receipt Number").grid(column=0, row=1, sticky=E, padx=5, pady=5)
    Label(main_window, text="Customer Name").grid(column=0, row=2, sticky=E, padx=5, pady=5)
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=1)
    Button(main_window, text="Quit", font=("Arial 9 bold"), command=quit, bg="crimson", fg="white", width=12).grid(column=3, row=1, sticky=EW, padx=5, pady=5)
    Button(main_window, text="Append Details", command=check_inputs, width=16).grid(column=1, row=5, sticky=EW, padx=5, pady=5)
    Button(main_window, text="Print Details", command=print_customer_details, width=16).grid(column=1, row=6, sticky=EW, padx=5, pady=5)
    Label(main_window, text="Item Hired").grid(column=0, row=3, sticky=E, padx=5, pady=5)
    Label(main_window, text="Amount Hired").grid(column=0, row=4, sticky=E, padx=5, pady=5)
    Label(main_window, text="Receipt No.").grid(column=3, row=3, sticky=EW, padx=5, pady=5)

    # Create a frame for the image button
    img_frame = Frame(main_window)
    img_frame.grid(column=3, row=5, sticky=EW, padx=5, pady=5)
    Img_Button = Button(img_frame, text="Delete Receipt", command=delete_receipt, width=80, image=main_window.button_image_1)
    Img_Button.pack()

    # Set column width globally for columns 0-3
    main_window.columnconfigure(0, weight=0, minsize=150)
    main_window.columnconfigure(1, weight=0, minsize=150)
    main_window.columnconfigure(2, weight=0, minsize=150)
    main_window.columnconfigure(3, weight=0, minsize=150)

# Start the program running
def main():
    # Create a canvas for the background image
    canvas = Canvas(main_window, width=600, height=76)
    canvas.grid(row=0, column=0, columnspan=4, sticky=EW, pady=(0,20))

    # Add the background image
    setup_bg(canvas)

    # Start the GUI
    setup_buttons()
    main_window.mainloop()

# Create empty list for customer details and empty variable for entries in the list
counters = {'total_entries': 1, 'name_count': 0}
customer_details = []
main_window = Tk()
main_window.title("Julie's Party Hire Store")
customer_name = Entry(main_window, width=23)
customer_name.grid(column=1, row=2)
item_hired = Entry(main_window, width=23)
item_hired.grid(column=1, row=3)
amount_hired = Entry(main_window, width=23)
amount_hired.grid(column=1, row=4)
delete_receipt_num = Entry(main_window, width=23)
delete_receipt_num.grid(column=3, row=4, padx=5, pady=5)
main()
