# Date Created: 21/07/2024
# Author: Jack Compton
# Purpose: GUI application for Julie's party hire store to keep track of items that are currently hired

import os
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Quit function
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
        Label(main_window, font=("Helvetica 10 bold"), text="Receipt No.", bg=main_window_bg_color, fg="white").grid(column=0, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Customer Name", bg=main_window_bg_color, fg="white").grid(column=1, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Item Hired", bg=main_window_bg_color, fg="white").grid(column=2, row=8, padx=5, pady=5)
        Label(main_window, font=("Helvetica 10 bold"), text="Amount Hired", bg=main_window_bg_color, fg="white").grid(column=3, row=8, padx=5, pady=5)

        # Add each item in the list into its own row
        for index, details in enumerate(customer_details):
            list_row = index + 9
            Label(main_window, text=index + 1, bg=main_window_bg_color, fg="white").grid(column=0, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[0], bg=main_window_bg_color, fg="white").grid(column=1, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[1], bg=main_window_bg_color, fg="white").grid(column=2, row=list_row, padx=5, pady=5)
            Label(main_window, text=details[2], bg=main_window_bg_color, fg="white").grid(column=3, row=list_row, padx=5, pady=5)

# Check the inputs are all valid
def validate_inputs():
    input_check = 0
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=2, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=3, sticky=W)
    Label(main_window, text="                                       ", bg=main_window_bg_color).grid(column=2, row=4, sticky=W)
    Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=4, sticky=E)

    # Check that name is not blank, set error text if blank
    if len(customer_name.get()) == 0:
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=2, sticky=W)
        input_check = 1

    # Check the item hired is not blank, set error text if blank
    if len(item_hired.get()) == 0:
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=3, sticky=W)
        input_check = 1

    # Check that the amount hired is not blank and above 0, set error text if blank or 0 and below
    if len(amount_hired.get()) == 0:
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=4, sticky=W)
        input_check = 1
    elif amount_hired.get().isdigit():
        if int(amount_hired.get()) <= 0 or int(amount_hired.get()) > 500:
            Label(main_window, text="Between 0-500", bg=main_window_bg_color, fg="red").grid(column=2, row=4, sticky=W)
            input_check = 1

    if input_check == 0:
        append_receipt()


# Add the next customer to the list
def append_receipt():
    # Append each item to its own area of the list
    customer_details.append([customer_name.get(), item_hired.get(), amount_hired.get()])
    # Clear the boxes
    customer_name.delete(0, "end")
    item_hired.delete(0, "end")
    amount_hired.delete(0, "end")
    counter["total_entries"] += 1
    Label(main_window, text=counter["total_entries"], font=("Segoe UI", 10, "bold"), bg=main_window_bg_color, fg="white").grid(column=1, row=1)

# Delete a receipt from the list
def delete_receipt():
    # Check that name is not blank, set error text if blank
    if len(delete_receipt_num.get()) == 0:
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=2, sticky=W)
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=3, sticky=W)
        Label(main_window, text="                                       ", bg=main_window_bg_color).grid(column=2, row=4, sticky=W)
        Label(main_window, text="Required", bg=main_window_bg_color, fg="red").grid(column=2, row=4, sticky=E)   
    else:
        Label(main_window, text="                                ", bg=main_window_bg_color).grid(column=2, row=4, sticky=E)
        # Find which row is to be deleted and delete it
        index = int(delete_receipt_num.get()) - 1
        if 0 <= index < len(customer_details):  # Make sure that the index being deleted exists
            del customer_details[index]
            counter["total_entries"] -= 1
            Label(main_window, text=counter["total_entries"], font=("Segoe UI", 10, "bold"), bg=main_window_bg_color, fg="white").grid(column=1, row=1)
            delete_receipt_num.delete(0, "end")
            if len(customer_details) <= 0:
                # Clear previous entries
                for widget in main_window.grid_slaves():
                    if int(widget.grid_info()["row"]) > 7:  # Checks if the widget is in a row larger than 8, which is where customer details are displayed.
                        widget.grid_forget()  # Remove the widget from the grid by forgetting it
            else:
                print_customer_details()

# Add the banner image
def setup_bg(canvas):
    # Add image file
    global bg  # Keep a global reference to the background image ("bg" object)
    bg = PhotoImage(file="Images/Banner.png")

    # Show image using canvas
    canvas.create_image(0, 0, anchor=NW, image=bg)

# Create the buttons and labels
def setup_elements():

    # Specify the images to use for each button in normal and clicked states
    main_window.btn_img1_normal = PhotoImage(file="Images/Buttons/Exit.png")
    main_window.btn_img1_clicked = PhotoImage(file="Images/Buttons/Exit_Clicked.png")
    main_window.btn_img2_normal = PhotoImage(file="Images/Buttons/Delete.png")
    main_window.btn_img2_clicked = PhotoImage(file="Images/Buttons/Delete_Clicked.png")
    main_window.btn_img3_normal = PhotoImage(file="Images/Buttons/Append.png")
    main_window.btn_img3_clicked = PhotoImage(file="Images/Buttons/Append_Clicked.png")
    main_window.btn_img4_normal = PhotoImage(file="Images/Buttons/Print.png")
    main_window.btn_img4_clicked = PhotoImage(file="Images/Buttons/Print_Clicked.png")

    # Create the labels
    Label(main_window, text="Receipt Number", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=1, sticky=E, padx=5, pady=5)
    Label(main_window, text="Customer Name", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=2, sticky=E, padx=5, pady=5)
    Label(main_window, text=counter["total_entries"], bg=main_window_bg_color, fg="white", font=("Segoe UI", 10, "bold")).grid(column=1, row=1)
    Label(main_window, text="Item Hired", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=3, sticky=E, padx=5, pady=5)
    Label(main_window, text="Amount Hired", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=0, row=4, sticky=E, padx=5, pady=5)
    Label(main_window, text="Receipt No.", bg=main_window_bg_color, font=("Segoe UI", 10, "bold"), fg="white").grid(column=3, row=3, sticky=EW, padx=5, pady=5)

    # Create a frame for the image buttons
    img_frame1 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame1.grid(column=3, row=1, sticky=EW, pady=5)
    img_frame2 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame2.grid(column=3, row=5, sticky=EW, pady=5)
    img_frame3 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame3.grid(column=1, row=5, sticky=EW, pady=5)
    img_frame4 = Frame(main_window, width=23, bg=main_window_bg_color)
    img_frame4.grid(column=1, row=6, sticky=EW, pady=5)

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
    #Exit Program Button
    img_button1 = Button(img_frame1, command=lambda: handle_button_click(main_window.quit), width=140, image=main_window.btn_img1_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button1.image = main_window.btn_img1_normal  # Store the image reference
    img_button1.bind("<Button-1>", lambda e: on_button_press(img_button1, main_window.btn_img1_clicked))  # Bind button press
    img_button1.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button1, main_window.btn_img1_normal))  # Bind button release
    img_button1.bind("<Enter>", lambda e: on_button_enter(img_button1, main_window.btn_img1_clicked, main_window.btn_img1_normal))  # Handle mouse enter
    img_button1.bind("<Leave>", lambda e: on_button_leave(img_button1, main_window.btn_img1_normal))  # Handle mouse leave
    img_button1.pack(fill="x")

    #Delete Receipt Button
    img_button2 = Button(img_frame2, command=lambda: handle_button_click(delete_receipt), width=140, image=main_window.btn_img2_normal,
                        bg=main_window_bg_color, fg="white", font=("Helvetica 10 bold"), borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button2.image = main_window.btn_img2_normal  # Store the image reference
    img_button2.bind("<Button-1>", lambda e: on_button_press(img_button2, main_window.btn_img2_clicked))  # Bind button press
    img_button2.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button2, main_window.btn_img2_normal))  # Bind button release
    img_button2.bind("<Enter>", lambda e: on_button_enter(img_button2, main_window.btn_img2_clicked, main_window.btn_img2_normal))  # Handle mouse enter
    img_button2.bind("<Leave>", lambda e: on_button_leave(img_button2, main_window.btn_img2_normal))  # Handle mouse leave
    img_button2.pack(fill="x")

    #Append Details Button
    img_button3 = Button(img_frame3, command=lambda: handle_button_click(validate_inputs), width=140, image=main_window.btn_img3_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button3.image = main_window.btn_img3_normal  # Store the image reference
    img_button3.bind("<Button-1>", lambda e: on_button_press(img_button3, main_window.btn_img3_clicked))  # Bind button press
    img_button3.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button3, main_window.btn_img3_normal))  # Bind button release
    img_button3.bind("<Enter>", lambda e: on_button_enter(img_button3, main_window.btn_img3_clicked, main_window.btn_img3_normal))  # Handle mouse enter
    img_button3.bind("<Leave>", lambda e: on_button_leave(img_button3, main_window.btn_img3_normal))  # Handle mouse leave
    img_button3.pack(fill="x")

    #Print Details Button
    img_button4 = Button(img_frame4, command=lambda: handle_button_click(print_customer_details), width=140, image=main_window.btn_img4_normal,
                        bg=main_window_bg_color, fg="white", borderwidth=0, compound="center", relief="flat",
                        activebackground=main_window_bg_color, activeforeground=main_window_bg_color)
    img_button4.image = main_window.btn_img4_normal  # Store the image reference
    img_button4.bind("<Button-1>", lambda e: on_button_press(img_button4, main_window.btn_img4_clicked))  # Bind button press
    img_button4.bind("<ButtonRelease-1>", lambda e: on_button_release(img_button4, main_window.btn_img4_normal))  # Bind button release
    img_button4.bind("<Enter>", lambda e: on_button_enter(img_button4, main_window.btn_img4_clicked, main_window.btn_img4_normal))  # Handle mouse enter
    img_button4.bind("<Leave>", lambda e: on_button_leave(img_button4, main_window.btn_img4_normal))  # Handle mouse leave
    img_button4.pack(fill="x")

    # Set width for columns 0-3 in the main window
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
    setup_elements()
    main_window.mainloop()

#Initialise the main window
main_window = Tk()
main_window.title("Julie's Party Hire Store")
main_window.iconphoto(False, PhotoImage(file="Images/Pgm_Icon.png"))  # Set the title bar icon
main_window.resizable(False, False)  # Set the resizable property for height and width to False
main_window_bg_color = "#B4B9DE"  # Set the background color of the main window
main_window.configure(bg=main_window_bg_color)

#Initialise total entries counter 
counter = {"total_entries": 1}
customer_details = []  # Create empty list for customer details and empty variable for entries in the list

#Setup entry boxes
customer_name = Entry(main_window, width=23, bg="#979BBA", fg="white")
customer_name.grid(column=1, row=2)
customer_name.config(insertbackground="white")
item_hired = Entry(main_window, width=23, bg="#979BBA", fg="white")
item_hired.grid(column=1, row=3)
item_hired.config(insertbackground="white")
amount_hired = Entry(main_window, width=23, bg="#979BBA", fg="white")
amount_hired.grid(column=1, row=4)
amount_hired.config(insertbackground="white")
delete_receipt_num = Entry(main_window, width=23, bg="#979BBA", fg="white")
delete_receipt_num.grid(column=3, row=4, padx=5, pady=5)
delete_receipt_num.config(insertbackground="white")

#Run the main function
main()