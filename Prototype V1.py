#import tkinter so we can make a GUI
from tkinter import *

#quit subroutine
def quit():
    main_window.destroy()

#print details of all the camps
def print_customer_details():
    name_count = 0
    # Create the column headings
    Label(main_window, font=("Helvetica 10 bold"), text="Receipt Number").grid(column=0, row=7)
    Label(main_window, font=("Helvetica 10 bold"), text="Customer Name").grid(column=1, row=7)
    Label(main_window, font=("Helvetica 10 bold"), text="Item Hired").grid(column=2, row=7)
    Label(main_window, font=("Helvetica 10 bold"), text="Amount Hired").grid(column=3, row=7)
    
    # Add each item in the list into its own row
    while name_count < counters['total_entries']:
        if name_count < len(customer_details):
            Label(main_window, text=name_count).grid(column=0, row=name_count + 8)
            Label(main_window, text=(customer_details[name_count][0])).grid(column=1, row=name_count + 8)
            Label(main_window, text=(customer_details[name_count][1])).grid(column=2, row=name_count + 8)
            Label(main_window, text=(customer_details[name_count][2])).grid(column=3, row=name_count + 8)
            Label(main_window, text=(customer_details[name_count][3])).grid(column=4, row=name_count + 8)
        name_count += 1
        counters['name_count'] = name_count

# Check the inputs are all valid
def check_inputs():
    input_check = 0
    Label(main_window, text="               ").grid(column=2, row=0)
    Label(main_window, text="               ").grid(column=2, row=1)
    Label(main_window, text="               ").grid(column=2, row=2)
    Label(main_window, text="               ").grid(column=2, row=3)
    
    # Check that name is not blank, set error text if blank
    if len(entry_name.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=0)
        input_check = 1
    
    # Check the item hired is not blank and between 5 and 10, set error text if blank
    if entry_item.get().isdigit():
        if int(entry_item.get()) < 5 or int(entry_item.get()) > 10:
            Label(main_window, fg="red", text="5-10 only").grid(column=2, row=2)
            input_check = 1
    else:
        Label(main_window, fg="red", text="5-10 only").grid(column=2, row=2)
        input_check = 1
    
    # Check that weather is not blank, set error text if blank
    if len(entry_weather.get()) == 0:
        Label(main_window, fg="red", text="Required").grid(column=2, row=3)
        input_check = 1
    
    if input_check == 0:
        append_name()

# Add the next customer to the list
def append_name():
    # Append each item to its own area of the list
    customer_details.append([entry_name.get(), entry_item.get(), entry_weather.get(), counters['total_entries']])
    # Clear the boxes
    entry_name.delete(0, 'end')
    entry_item.delete(0, 'end')
    entry_weather.delete(0, 'end')
    counters['total_entries'] += 1
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=1)

# Delete a row from the list
def delete_row():
    # Find which row is to be deleted and delete it
    index = int(delete_item.get())
    if 0 <= index < len(customer_details):
        del customer_details[index]
        counters['total_entries'] -= 1
        delete_item.delete(0, 'end')
        # Clear the last item displayed on the GUI
        Label(main_window, text="       ").grid(column=0, row=index + 8)
        Label(main_window, text="       ").grid(column=1, row=index + 8)
        Label(main_window, text="       ").grid(column=2, row=index + 8)
        Label(main_window, text="       ").grid(column=3, row=index + 8)
        Label(main_window, text="       ").grid(column=4, row=index + 8)
        # Print all the items in the list
        print_customer_details()

# Create the buttons and labels
def setup_buttons():
    # Create all the empty and default labels, buttons, and entry boxes. Put them in the correct grid location
    Label(main_window, text="Customer Name").grid(column=0, row=0, sticky=E)
    Label(main_window, text="Receipt Number").grid(column=0, row=1, sticky=E)
    Label(main_window, text=counters['total_entries'], font=("Helvetica 10 bold")).grid(column=1, row=1)
    Button(main_window, text="Quit", font=("Arial 9 bold"), command=quit, bg="crimson", fg="white", width=10).grid(column=4, row=0, sticky=E)
    Button(main_window, text="Append Details", command=check_inputs).grid(column=3, row=1)
    Button(main_window, text="Print Details", command=print_customer_details, width=10).grid(column=4, row=1, sticky=E)
    Label(main_window, text="Item Hired").grid(column=0, row=2, sticky=E)
    Label(main_window, text="Amount Hired").grid(column=0, row=3, sticky=E)
    Label(main_window, text="Row #").grid(column=3, row=2, sticky=E)
    Button(main_window, text="Delete Row", command=delete_row, width=10).grid(column=4, row=3, sticky=E)
    Label(main_window, text="               ").grid(column=2, row=0)

# Start the program running
def main():
    # Start the GUI
    setup_buttons()
    main_window.mainloop()

# Create empty list for customer details and empty variable for entries in the list
counters = {'total_entries': 0, 'name_count': 0}
customer_details = []
main_window = Tk()
entry_name = Entry(main_window)
entry_name.grid(column=1, row=0)
entry_item = Entry(main_window)
entry_item.grid(column=1, row=2)
entry_weather = Entry(main_window)
entry_weather.grid(column=1, row=3)
delete_item = Entry(main_window)
delete_item.grid(column=3, row=3)
main()
