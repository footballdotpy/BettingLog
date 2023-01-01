import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Treeview
from tkinter import Scrollbar, messagebox
import datetime

def add_data():
    try:
        # Get the values of the dropdown menus
        value1 = dropdown1.get()
        value2 = entry_text.get()
        value3 = entry_text_stake.get()
        value4 = dropdown3.get()
        value5 = dropdown5.get()

        # Get the current date
        value6 = datetime.datetime.now().strftime("%Y-%m-%d")

        # Open the CSV file in append mode
        with open('bettinglog.csv', 'a', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)
            # Write the values to a new row in the CSV file
            writer.writerow([value6, value1, value2, value3, value4, value5])

            # Show a message box indicating that the bet has been added to the log
            messagebox.showinfo("Betting Log", "Bet added to log")

    except Exception as e:
        # Print an error message if an exception is raised
        messagebox.showerror("Betting Log", "Error adding to log")
        # Print an error message if an exception is raised
        print(f'Error writing to file: {e}')


def clear_data():
    # Set the values of the dropdown menus to an empty string
    dropdown1.set('')
    dropdown3.set('')
    dropdown5.set('')
    # Set the values of the text entry fields to an empty string
    entry_text.set('')
    entry_text_stake.set('')


# Create the main window
window = tk.Tk()
window.title("Betting Log")
window.geometry("1000x750")

# Create the labels and dropdown menus
label1 = tk.Label(window, text="Bookmaker:")
label1.pack()
dropdown1 = tk.ttk.Combobox(window, width=20, values=['SkyBet', 'Betfair SB', 'Betfair Exchange', 'BetVictor', 'Coral'
    , 'Betway', 'Unibet'])
dropdown1.pack()

label2 = tk.Label(window, text="Selection:")
label2.pack()

entry_text = tk.StringVar()
text_input = tk.Entry(window, width=50, textvariable=entry_text)
text_input.pack()

label3 = tk.Label(window, text="Stake:")
label3.pack()
entry_text_stake = tk.StringVar()
text_input_stake = tk.Entry(window, width=20, textvariable=entry_text_stake)
text_input_stake.pack()

label4 = tk.Label(window, text="Odds:")
label4.pack()
dropdown3 = tk.ttk.Combobox(window, width=20, values=[1.45, 1.5, 1.53, 1.57, 1.62, 1.66, 1.72, 1.8, 1.83, 1.91, 2, 2.1,
                                                      2.2, 2.25, 2.38, 2.4, 2.5, 2.55, 2.6, 2.63, 2.75, 2.8, 2.88, 3, 3.2,
                                                      3.25, 3.4, 3.5, 3.6, 3.75, 4, 4.33, 4.5, 5, 5.5,
                                                      6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 11, 12, 13, 14, 15, 16, 17,
                                                      19, 21, 26, 34, 101])
dropdown3.pack()

label5 = tk.Label(window, text="Result:")
label5.pack()
dropdown5 = tk.ttk.Combobox(window, width=20, values=['Win', 'Lose', 'Push'])
dropdown5.pack()

# Create the "Add" button and bind the add_data function to the button's command event
add_button = tk.Button(window, text="Add", command=add_data)
add_button.place(x=100, y=100, height=50, width=100)

# Create the "Clear" button and bind the clear_data function to the button's command event
clear_button = tk.Button(window, text="Clear", command=clear_data)
clear_button.place(x=800, y=100, height=50, width=100)

# Create the Treeview widget and Scrollbar widget


tree = Treeview(window,
                columns=("Date","Bookmaker", "Selection", "Stake", "Odds", "Result", "Profit/Loss"))

scrollbar = Scrollbar(window)

# Configure the treeview widget to use the scrollbar
tree.configure(yscrollcommand=scrollbar.set)

# Pack the Scrollbar and Treeview widgets
scrollbar.pack(side="right", fill="y")

# Configure the scrollbar to control the treeview widget
scrollbar.configure(command=tree.yview)


# Set the column headings and supress the first column it shows empty as default
tree.column("#0", width=0, stretch=False)
tree.column("Date", width=80, anchor="ne")
tree.column("Bookmaker", width=125, anchor="ne")
tree.column("Selection", width=200, anchor="w")
tree.column("Stake", width=110, anchor="w")
tree.column("Odds", width=110, anchor="w")
tree.column("Result", width=110, anchor="w")
tree.column("Profit/Loss", width=130, anchor="w")
tree.heading("Date", text="Date")
tree.heading("Bookmaker", text="Bookmaker")
tree.heading("Selection", text="Selection")
tree.heading("Stake", text="Stake")
tree.heading("Odds", text="Odds")
tree.heading("Result", text="Result")
tree.heading("Profit/Loss", text="Profit/Loss")

# Open the CSV file and read the rows

with open('bettinglog.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the first row (column names)
    next(reader)
    # Iterate over the rows in the CSV file
    for i, row in enumerate(reader):
        # Calculate the profit or loss based on the result
        if row[5] == 'Win':
            profit_loss = float(row[3]) * float(row[4]) - float(row[3])
        elif row[5] == 'Lose':
            profit_loss = -float(row[3])
        else:
            profit_loss = 0
        # Insert the row and the profit/loss into the Treeview
        tree.insert("", "end", values=row[:6] + [profit_loss])

# Place the Treeview widget
tree.place(x=100, y=250)


def refresh_treeview():
    # Open the CSV file and read the data

    # Clear the existing data from the Treeview
    for i in tree.get_children():
        tree.delete(i)

    with open('bettinglog.csv', 'r', newline='') as csvfile:

        reader = csv.reader(csvfile)

        next(reader)

        # Iterate over the rows in the CSV file
        for i, row in enumerate(reader):
            # Calculate the profit or loss based on the result
            if row[5] == 'Win':
                profit_loss = float(row[3]) * float(row[4]) - float(row[3])
            elif row[5] == 'Lose':
                profit_loss = -float(row[3])
            else:
                profit_loss = 0
            # Insert the row and the profit/loss into the Treeview
            tree.insert("", "end", values=row[:6] + [profit_loss])


# Create the "Refresh" button and bind the refresh_treeview function to the button's command event
refresh_button = tk.Button(window, text="Refresh", command=refresh_treeview)
refresh_button.place(x=100, y=500, height=50, width=100)

# Run the main loop
window.mainloop()
