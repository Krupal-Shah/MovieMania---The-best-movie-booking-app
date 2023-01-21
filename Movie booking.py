#Movie Booking.
#By Krupal Shah

#Modules Used
import tkinter as tk
from tkinter import *
from tkinter import ttk
import re
import pyautogui as py
import mysql.connector as ms
import random

#MySQL Backend Connection
mycon = ms.connect(host="localhost", user="root" ,passwd="krupal", database="Booking")
mycursor = mycon.cursor()
if mycon.is_connected():
    print("connected")

query_1 = "create table if not exists table_one(booking_id int primary key, movie_name varchar(50), day varchar(10), time varchar(20), seats varchar(20), cost float)"
query_2 = "create table if not exists table_two(booking_id int primary key, customer_name varchar(50), email_id varchar(50), mobile_no int, cardholder_name varchar(50), cardholder_number varchar(25), expiry char(5), foreign key(booking_id) REFERENCES table_one(booking_id))"

mycursor.execute(query_1)
mycursor.execute(query_2)
mycon.commit()

#Mainpage
window = tk.Tk()
window.title("Movie Booking")
window.geometry('1350x800+0+0')
cruella = PhotoImage(file = "cruella.png").subsample(5,5)
F9 = PhotoImage(file = "F9.png").subsample(4,4)
free = PhotoImage(file = "free.png").subsample(1,1)
jungle = PhotoImage(file = "jungle cruise.png").subsample(5,5)
quiet = PhotoImage(file = "quiet place 2.png").subsample(1,1)
space = PhotoImage(file = "space jam.png").subsample(4,4)
color =  '#%02x%02x%02x' % (240, 240, 237)

window.configure(bg = color)

mainl = []
detail = []
l1=['BookingID','Movie', 'Day', 'Time', 'Seats', 'Total Cost']
l2 = ['Name', 'Email Address', 'Mobile Number']

#Create Booking ID
mycursor.execute('select booking_id from table_one')
record = mycursor.fetchall()
ids = ()
while True:
    bookingID = random.randint(1111111, 9999999)
    for row in record:
        ids += (row[0],)
    if  bookingID not  in ids:
        break    
print(bookingID)

mainl.append(bookingID)
detail.append(bookingID)

def mainpage():
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar, bg=color)
    my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion =  my_canvas.bbox('all')))
    second_frame = Frame(my_canvas, bg = color) 
    my_canvas.create_window((0,0), window=second_frame, anchor='nw')
    Label(second_frame, text= "Cinestar Cinemas", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 0, columnspan=4)
    Button(second_frame, text='Login', command= lambda : login()).grid(row=0, column = 4)
    Button(second_frame, text = 'Cruella', image = cruella, command = lambda a='Cruella': timings(a)).grid(row=1, column=0, padx = 1, pady = 1)
    Button(second_frame, text= 'Fast and Furious 9', image = F9,  command = lambda a='Fast and Furious 9': timings(a)).grid(row=1, column=1, padx = 1, pady = 1)
    Button(second_frame, text= 'Free Guy', image = free, command = lambda a = 'Free Guy': timings(a)).grid(row=1, column=2, padx = 1, pady = 1)
    Button(second_frame, text= 'Jungle Cruise', image = jungle, command = lambda a = 'Jungle Cruise': timings(a)).grid(row=3, column=0, padx = 1, pady = 1)
    Button(second_frame, text= 'A Quiet Place: Part II', image = quiet, command = lambda a = 'A Quiet Place: Part II': timings(a)).grid(row=3, column=1, padx = 1, pady = 1)
    Button(second_frame, text= 'Space Jam: A New Legacy', image = space, command = lambda a = 'Space Jam: A New Legacy': timings(a)).grid(row=3, column=2, padx = 1, pady = 1)
    Label(second_frame ,text="Cruella", bg = color, font=('Comic Sans MS', 14)).grid(row=2, column=0)
    Label(second_frame ,text="Fast and Furious 9", bg = color, font=('Comic Sans MS', 14)).grid(row=2, column=1)
    Label(second_frame ,text="Free Guy", bg = color, font=('Comic Sans MS', 14)).grid(row=2, column=2)
    Label(second_frame ,text="Jungle Cruise", bg = color, font=('Comic Sans MS', 14)).grid(row=4, column=0)
    Label(second_frame ,text="A Quiet Place: Part II", bg = color, font=('Comic Sans MS', 14)).grid(row=4, column=1)
    Label(second_frame ,text="Space Jam: A New Legacy", bg = color,font=('Comic Sans MS', 14)).grid(row=4, column=2)
        
#Day and Timings Page
def timings(x):
    mainl.append(x)
    window.destroy()
    timing=tk.Tk()
    timing.title("Timing")
    timing.configure(bg=color)
    timing.geometry('1350x800+0+0')
    day=['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
    time=['10:00am', '11:00am', '12:30pm', '1:25pm', '3:30pm', '4:20pm', '5:10pm', '5:50pm', '7:10pm', '8:00pm', '9:30pm', '10:45pm']
    i=0
    for d in range(0,6):
        Button(timing, text=day[d], width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda a=day[d]: mainl.append(a)).grid(row=0, column=d)
    Label(timing, text="  \n   ", bg=color, font=('Comic Sans MS', 14)).grid(row=1, column=0)
    
    for j in range(2,4):
        for k in range(0,6):
            Button(timing, text=time[i], width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda a=time[i]: seats(timing, a)).grid(row=j, column=k)
            i+=1
            
    Label(timing, text="  \n   ", bg=color, font=('Comic Sans MS', 14)).grid(row=7, column=0)
    Button(timing, text='Cancel', command=lambda: cancel(timing)).grid(row=9, column = 5)

#Seats Page
def seats(file, val):
    mainl.append(val)
    file.destroy()
    seat = tk.Tk()
    seat.title("Seats")
    seat.geometry('1350x800+0+0')
    seat.configure(bg=color)
    selected_seats = []
    Label(seat, text='Screen', font=('Times New Roman', 16)).grid(row=0, column=12, columnspan = 5, padx = 5, pady = 5)
    row = ['N', 'M', 'L','K','J','I','H','G','F','E','D','C','B','A']
    
    mycursor.execute('select seats from table_one where movie_name="{}" and day = "{}" and time = "{}"'.format(mainl[1], mainl[2], mainl[3]))
    rec = mycursor.fetchall()
        
    #Letters
    for letter in range (2,6):  
        Label(seat, text=row[letter-2], font=('Times New Roman', 12)).grid(row=letter, column=0)
        Label(seat, text=row[letter-2], font=('Times New Roman', 12)). grid(row=letter, column=35)
    Label(seat, text='  \n  ', font=('Times New Roman', 16)).grid(row=6, column=0)
    for letter in range (7, 13):
        Label(seat, text=row[letter-3], font=('Times New Roman', 12)).grid(row=letter, column=0)
        Label(seat, text=row[letter-3], font=('Times New Roman', 12)). grid(row=letter, column=35)
    Label(seat, text='  \n  ', font=('Times New Roman', 16)).grid(row=13, column=0)
    for letter in  range (14, 18):
        Label(seat, text=row[letter-4], font=('Times New Roman', 12)).grid(row=letter, column=0)
        Label(seat, text=row[letter-4], font=('Times New Roman', 12)). grid(row=letter, column=35)

    #First Stack
    for num in range(2,6):
        if num%2==0:
            for k in range(3,30,4):
                Checkbutton(seat, command=lambda r=row[num-2], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-2], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)
        else:
            for k in range(1,29,4):
                Checkbutton(seat, command=lambda r=row[num-2], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-2], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)
    Label(seat, text='  \n  ', font=('Times New Roman', 16)).grid(row=6, column=0)
    
    # Second Stack starting 6
    for num in range(7,13):
        if num%2==0:
            for k in range(3,30,4):
                Checkbutton(seat, command=lambda r=row[num-3], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-3], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)
        else:
            for k in range(1,29,4):
                Checkbutton(seat, command=lambda r=row[num-3], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-3], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)
    Label(seat, text='  \n  ', font=('Times New Roman', 16)).grid(row=13, column=0)
    
    # Last Stack
    for num in range(14,18):
        if num%2==0:
            for k in range(3,30,4):
                Checkbutton(seat, command=lambda r=row[num-4], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-4], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)  
        else:
            for k in range(1,29,4):
                Checkbutton(seat, command=lambda r=row[num-4], c=k: selected_seats.append([r,c])).grid(row=num, column=k)
                Checkbutton(seat, command=lambda r=row[num-4], c=k+1: selected_seats.append([r,c])).grid(row=num, column=k+1)
    if rec != []:
        check = rec[0][0]
        a = (check.split(','))
        seatl1 = []
        for i in a:
            x = i.strip("\(\) '")
            if x.isalpha() == True:
                seatl1.append(str(x))
            elif x.isalnum() == True:
                seatl1.append(int(x))
        for i in range(0, len(seatl1), 2):
            if seatl1[i] in ['N', 'M', 'L','K']:
                Checkbutton(seat, state = DISABLED).grid(row = (row.index(seatl1[i]))+2, column = seatl1[i+1])
            elif seatl1[i] in ['J','I','H','G','F','E']:
                Checkbutton(seat,  state = DISABLED).grid(row = (row.index(seatl1[i]))+3, column = seatl1[i+1])
            elif seatl1[i] in ['D','C','B','A']:
                Checkbutton(seat, state = DISABLED).grid(row = (row.index(seatl1[i]))+4, column = seatl1[i+1])
    
    Checkbutton(seat, text='', state = DISABLED).grid(row=19, column = 4)
    Label(seat, text='Booked').grid(row=19, column = 5)
    
    selected = Checkbutton(seat, text='')
    selected.grid(row=19, column = 8)
    selected.select()
    Label(seat, text='Selected').grid(row=19, column = 9, columnspan = 2)
    
    Checkbutton(seat, text='',).grid(row=19, column = 12)
    Label(seat, text='Empty').grid(row=19, column = 13, columnspan = 2)
    Button(seat, text='Next', command=lambda: proceed()).grid(row=19, column = 35)
    Button(seat, text='Cancel', command=lambda: cancel(seat)).grid(row=19, column = 34)
    
    def proceed():
        global cost
        cost=(len(selected_seats))*40
        mainl.append(tuple(tuple(x) for x in selected_seats))
        mainl.append(cost)
        seat.destroy()
        payment()
 
 #Payment Page

def payment():
    pay = Tk()
    pay.title("Payment Details")
    pay.geometry('1350x800+0+0')
    pay.configure(bg=color)
    Label(pay, text="PAYMENT", bg=color, font=('Comic Sans MS', 16)).grid(row=0, column = 6)
    Label(pay, text="Details", bg=color, font=('Comic Sans MS', 14)).grid(row=1, column = 0, columnspan = 1)
    for i in range(2,6):
        Label(pay, text=l1[i-1], bg=color, font=('Comic Sans MS', 12)).grid(row=i, sticky  = W)
        Label(pay, text=mainl[i-1], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 1, sticky = W)
    Label(pay, text=l1[-1], bg=color, font=('Comic Sans MS', 12)).grid(row=6, column=0, sticky = W)
    Label(pay, text='Dhs '+str(mainl[-1]), bg=color, font=('Comic Sans MS', 12)).grid(row=6, column = 1, sticky = W)
    
    def new_window():
        global cus_name, cus_email, cus_conemail,  cus_phone,  card_name, card_number, card_expiry
        cus_name = e1.get()
        cus_email = e2.get()
        cus_conemail  = e3.get()
        cus_phone = e4.get()
        card_name = e5.get()
        card_number = e6.get()
        card_expiry = e7.get()
        
        if cus_email != cus_conemail:
            tk.messagebox.showerror(title='Invalid Email', message = 'Please Enter same Email Address')
        elif not re.match("^[0-9 ]*$", cus_phone):
            tk.messagebox.showerror(title='Invalid Phone Number', message = 'Please Enter numbers only')
        elif not re.match("^[a-zA-Z ]*$", card_name):
            tk.messagebox.showerror(title='Invalid Name', message = 'Please enter proper name')
        elif not re.match("^[0-9 ]*$", card_number):
            tk.messagebox.showerror(title='Invalid card Number', message = 'Please Enter numbers only\nFormat: (1111 1111 1111 1111)')
        elif len(card_number) != 19 or card_number[4] !=' '  or card_number[9] !=' ' or card_number[14] !=' ':
            tk.messagebox.showerror(title='Invalid card Number', message = 'Please Enter numbers only\nFormat: (1111 1111 1111 1111)')            
        elif not re.match("^[0-9 /]*$", card_expiry):
            tk.messagebox.showerror(title='Invalid Expiry Date', message = 'Please Enter numbers only\nFormat: (MM/YY)')
        else:
            detail.append(cus_name)
            detail.append(cus_email)
            detail.append(cus_phone)
            detail.append(card_name)
            detail.append(card_number)
            detail.append(card_expiry)
            pay.destroy()
            confirmation()
            
    Label(pay, text='   \n    ', bg=color, font=('Comic Sans MS', 12)).grid(row=7, column = 1)
    Label(pay, text="First Name", bg=color, font=('Calibri', 13)).grid(row=8)
    Label(pay, text="Email", bg=color, font=('Calibri', 13)).grid(row=9)
    Label(pay, text='Confirm Email', bg=color, font=('Calibri', 13)).grid(row=10)
    Label(pay, text='Phone Number', bg=color, font=('Calibri', 13)).grid(row = 11)
    Label(pay, text='  \n  ', bg=color, font=('Times New Roman', 12)).grid(row=12, column=0)
    Label(pay, text='Cardholder Name', bg=color, font=('Calibri', 13)).grid(row = 13)
    Label(pay, text='Card  Number', bg=color, font=('Calibri', 13)).grid(row = 14)
    Label(pay, text='Card Expiry', bg=color, font=('Calibri', 13)).grid(row = 15)
    
    e1 = Entry(pay)
    e1.grid(row=8, column=1)
    
    e2 = Entry(pay)
    e2.grid(row=9, column=1)
    
    e3 = Entry(pay)
    e3.grid(row=10, column=1)

    e4 = Entry(pay)
    e4.grid(row=11, column=1)
    
    e5 = Entry(pay)
    e5.grid(row=13, column=1)

    e6 = Entry(pay)
    e6.grid(row=14, column=1)

    e7 = Entry(pay)
    e7.grid(row=15, column=1)
    
    Button(pay, text='Next', command=lambda: new_window()).grid(row=16, column = 10)
    Button(pay, text='Cancel', command=lambda: cancel(pay)).grid(row=16, column = 9)
    pay.mainloop()

#Confirmation Page
def confirmation():
    if len(mainl) == 6 and len(detail) == 7:
        a1, a2, a3, a4, a5, a6 = mainl
        d1,d2,d3,d4,d5,d6,d7 = detail
        record1 = 'insert into table_one values({},"{}","{}","{}","{}",{})'.format(a1, a2, a3, a4, a5, a6)
        record2 = "insert into table_two values({},'{}','{}',{},'{}','{}','{}')".format(d1,d2,d3,d4,d5,d6,d7)
        mycursor.execute(record1)
        mycursor.execute(record2)
        mycon.commit()
        confirm=tk.Tk()
        confirm.title("Booking Successful")
        confirm.geometry('1350x800+0+0')
        confirm.configure(bg=color)
        Label(confirm, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 3, columnspan=4)
        Label(confirm, text="Congratulations", bg=color, font=('Comic Sans MS', 16)).grid(row=1, column =4)
        Label(confirm, text="Your Ticket Booking was Sucessful!", bg=color, font=('Comic Sans MS', 14, "bold")).grid(row=2, column = 3, columnspan = 4)
        Label(confirm, text='  \n  ', bg=color, font=('Times New Roman', 12)).grid(row=3, column=0)
        Label(confirm, text='Booking ID', bg=color, font=('Times', 14, 'bold')).grid(row=4,  column=1, columnspan = 2)
        Label(confirm, text='Details', bg=color, font=('Times', 14, 'bold')).grid(row=4,  column=7, columnspan = 2)

        for i in range(5,10):
            Label(confirm, text=l1[i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 1, sticky = W)
            Label(confirm, text=mainl[i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 2)
        Label(confirm, text=l1[-1], bg=color, font=('Comic Sans MS', 12)).grid(row=10, column = 1)
        Label(confirm, text='AED  '+str(mainl[-1]), bg=color, font=('Comic Sans MS', 12)).grid(row=10, column = 2)

        for i in range(5,8):
            Label(confirm, text=l2[i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 7, sticky = W)
            Label(confirm, text=detail[i-4], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 8)
    else:
        confirm=tk.Tk()
        confirm.title("Booking Not Successful")
        confirm.geometry('1350x800+0+0')
        confirm.configure(bg=color)
        Label(confirm, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 1, columnspan=7)
        Label(confirm, text="Sorry !!", bg=color, font=('Comic Sans MS', 16)).grid(row=1, column =3)
        Label(confirm, text="Your Ticket Booking was not sucessful!", bg=color, font=('Comic Sans MS', 14, "bold")).grid(row=2, column = 2, columnspan = 4)
        Label(confirm, text='  \n  ', bg=color, font=('Times New Roman', 12)).grid(row=3, column=0)
        Label(confirm, text='Error 0x19c : Incomplete Sequence', bg=color, font=('Comic Sans MS', 14, "bold")).grid(row = 4, column = 1, columnspan = 2)
        Label(confirm, text='For more details please send an email to errors@Cinestarcinema.com or visit the nearest cinema with your booking ID ', bg=color, font=('Times', 14)).grid(row=5,  column=1, columnspan = 7)
        Label(confirm, text='and error code', bg=color, font=('Times', 14)).grid(row=6,  column=0 , columnspan = 2)
        
def cancel(file_window):
    file_window.destroy()
    mainl.clear()
    detail.clear()
    py.hotkey('fn','f5')
    
#Login - admin page
def login():
    window.destroy()
    admin = tk.Tk()
    admin.title("Login")
    admin.geometry('1350x800+0+0')
    
    def new_window():
        global  Login_ID, password
        Login_ID = LogID.get()
        password = pas.get()
        if Login_ID != 'admin' and password != int('0000'):
            tk.messagebox.showerror(title='Error', message = 'Invalid ID or Password')
        else:
            admin_main(admin)
        
    Label(admin, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 0, columnspan=4)
    Label(admin, text="Login ID", bg=color, font=('Calibri', 13)).grid(row=4)
    Label(admin, text="\n", bg=color, font=('Calibri', 13)).grid(row=2)
    Label(admin, text="Password", bg=color, font=('Calibri', 13)).grid(row=5)
    LogID = Entry(admin)
    LogID.grid(row=4, column=1)
    
    pas = Entry(admin)
    pas.grid(row=5, column=1)
    
    Button(admin, text='Next', command=lambda: new_window()).grid(row=16, column = 2)
    Button(admin, text='Cancel', command=lambda: cancel(admin)).grid(row=16, column = 3)
    
    Label(admin, text="\n", bg=color, font=('Calibri', 13)).grid(row=18)


#Admin mainpage
def admin_main(file_destroy):
    file_destroy.destroy()
    main = tk.Tk()
    main.title("admin")
    main.geometry('1350x800+0+0')
    
    Button(main, text='Display', width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda : admin_display(main)).pack()
    Button(main, text='Search', width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda : admin_search(main)).pack()
    Button(main, text='Modify', width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda : admin_modify(main)).pack()
    Button(main, text='Delete', width=13, height=3, bg=color, font=('Comic Sans MS', 12), command=lambda : admin_delete(main)).pack()
    main.mainloop()

#To display all records
def admin_display(file_destroy):
    file_destroy.destroy()
    display = tk.Tk()
    display.title("admin")
    display.geometry('1500x800+0+0')

    mycursor.execute('select table_one.booking_id, movie_name, day, time, seats, cost, customer_name, email_id, mobile_no from table_one, table_two where table_one.booking_id = table_two.booking_id;')
    rec = mycursor.fetchall()
    Label(display, text='\n').grid(row = 0, column= 0)

    for heading in range(6):
        Label(display, text=l1[heading]).grid(row = 1, column= heading)
    for heading in range(6, 9):
        Label(display, text=l2[heading-6]).grid(row = 1, column= heading)
    i=2
    for query in rec:
        for j in range(len(query)):
            Label(display, width=len(str(query[j])), text=query[j]).grid(row = i, column= j)
        i+=1
    Label(display, text="\n", bg=color, font=('Calibri', 13)).grid(row=15)
    Label(display, text="\n", bg=color, font=('Calibri', 13)).grid(row=16)
    Button(display, text='Admin Page', command=lambda: admin_main(display)).grid(row=16, column = 8)
    Button(display, text='Home', command=lambda: cancel(display)).grid(row=16, column = 9)

#To search for records
def admin_search(file_destroy):
    file_destroy.destroy()
    search = tk.Tk()
    search.title("admin")
    search.geometry('1350x800+0+0')
        
    def search_id(en):
        global search_ID
        search_ID = (searchID.get())
        next()

    Label(search, text="Booking ID", bg=color, font=('Calibri', 13)).grid(row=2)
    searchID = Entry(search)
    searchID.grid(row=2, column=1)
    searchID.bind('<Return>', search_id)

    Label(search, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 3, columnspan=4)
    
    def next():
        mycursor.execute('select booking_id from table_one')
        rec = mycursor.fetchall()
        ids = list(list(x) for x in rec)
        if [int(search_ID)] in ids:
            mycursor.execute('select table_one.booking_id, movie_name, day, time, seats, cost, customer_name, email_id, mobile_no from table_one, table_two where table_one.booking_id = table_two.booking_id and table_one.booking_id = {}'.format(search_ID))
            rec = mycursor.fetchall()
            record = list(list(x) for x in rec)
            print(record)
            
            Label(search, text='Booking Details', bg=color, font=('Times', 14, 'bold')).grid(row=4,  column=1, columnspan = 2)
            Label(search, text='Personal Details', bg=color, font=('Times', 14, 'bold')).grid(row=4,  column=6, columnspan = 2)

            for i in range(5,10):
                Label(search, text=l1[i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 1, sticky = W)
                Label(search, text=record[0][i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 2)
            Label(search, text=l1[-1], bg=color, font=('Comic Sans MS', 12)).grid(row=10, column = 1, sticky = W)
            Label(search, text='AED  '+str(record[0][5]), bg=color, font=('Comic Sans MS', 12)).grid(row=10, column = 2)

            for i in range(5,8):
                Label(search, text=l2[i-5], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 6, sticky = W)
                Label(search, text=record[0][i+1], bg=color, font=('Comic Sans MS', 12)).grid(row=i, column = 7)
        else:
            Label(search, text='No ID found', bg=color, font=('Times', 14, 'bold')).grid(row=4,  column=6, columnspan = 2)
            
    Label(search, text="\n", bg=color, font=('Calibri', 13)).grid(row=15)
    Label(search, text="\n", bg=color, font=('Calibri', 13)).grid(row=16)
    Button(search, text='Admin Page', command=lambda: admin_main(search)).grid(row=16, column = 8)
    Button(search, text='Home', command=lambda: cancel(search)).grid(row=16, column = 9)
    
#To modify record
def admin_modify(file_destroy):
    file_destroy.destroy()
    modify = tk.Tk()
    modify.title("admin")
    modify.geometry('1350x800+0+0')
    
    def b_id(en):
        global BID
        BID = change_row.get()
        
        mycursor.execute('select booking_id from table_one')
        record = mycursor.fetchall()
        if (int(BID),) not in record:
            Label(modify, text = 'No Record Found', font=('Calibri', '14', 'bold')).grid(row=5, column =1)
   
    def show():
        global head
        head = clicked.get()
        head = label.config( text =  head )
        print(head)
    
        def edit_var(en):
            global edit
            edit = mod.get()
            print(edit)
            
        #Entry Box
        mod = Entry(modify)
        mod.grid(row=4, column=2)
        mod.bind('<Return>', edit_var)
        
    def modifying_row():
        print(clicked.get(), edit, BID)
        if clicked.get() in ['movie_name', 'day', 'time', 'seats']:
            mycursor.execute('update table_one set {} = "{}" where booking_id = {}'.format(clicked.get(), edit, BID))
            mycon.commit()
        else:
            mycursor.execute('update table_two set {} = "{}" where booking_id = {}'.format(clicked.get(), edit, BID))
            mycon.commit()
        Label(modify, text = 'Successfully Updated',  font=('Calibri', '14', 'bold')).grid(row=12, column = 4)

    options = ['movie_name', 'day', 'time', 'seats', 'customer_name', 'email_id', 'mobile_no']

    clicked = StringVar()
    clicked.set( options[0] )
  
    drop = OptionMenu( modify , clicked , *options )
    drop.grid(row = 2, column = 1)
  
    Label(modify, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 3, columnspan=4)
    Label(modify, text="Booking ID", bg = color, font=('Times', 14)).grid(row=1, column = 1)
    
    change_row = Entry(modify)
    change_row.grid(row=1, column=2)
    change_row.bind('<Return>', b_id)
    
    button = Button(modify , text = "Click Me" , command = show , width = 12).grid(row = 2, column =2)
    button = Button(modify , text = "Update" , command = modifying_row , width = 12).grid(row = 7, column =2)
  
    label = Label(modify , text = " " )
    label.grid(row = 4, column  =1)
    
    Label(modify, text="\n", bg=color, font=('Calibri', 13)).grid(row=15)
    Label(modify, text="\n", bg=color, font=('Calibri', 13)).grid(row=16)
    Button(modify, text='Admin Page', command=lambda: admin_main(modify)).grid(row=16, column = 8)
    Button(modify, text='Home', command=lambda: cancel(modify)).grid(row=16, column = 9)
    
#To delete records
def admin_delete(file_destroy):
    file_destroy.destroy()
    delete = tk.Tk()
    delete.title("admin")
    delete.geometry('1350x800+0+0')

    def search_id(en):
        global search_ID
        search_ID = (searchID.get())
        next()

    Label(delete, text="Cinestar Cinema", bg = color ,fg='gold3', font=('Times', 20)).grid(row=0, column = 3, columnspan=4)
    Label(delete, text="Booking ID", bg=color, font=('Calibri', 13)).grid(row=2)
    searchID = Entry(delete)
    searchID.grid(row=2, column=1)
    searchID.bind('<Return>', search_id)

    def next():
        try:
            mycursor.execute('delete from table_two where booking_id ={}'.format(int(search_ID)))
            mycursor.execute('delete from table_one where booking_id ={}'.format(int(search_ID)))
            mycon.commit()
            Label(delete, text=" \t Deleted Sucessfully \t", bg=color, font=('Calibri', 13)).grid(row=4, columnspan=3)
        except:
            Label(delete, text=" \t No Record Found \t ", bg=color, font=('Calibri', 13)).grid(row=4, columnspan = 3)
    
    Label(delete, text="\n", bg=color, font=('Calibri', 13)).grid(row=15)
    Label(delete, text="\n", bg=color, font=('Calibri', 13)).grid(row=16)
    Button(delete, text='Admin Page', command=lambda: admin_main(delete)).grid(row=16, column = 8)
    Button(delete, text='Home', command=lambda: cancel(delete)).grid(row=16, column = 9)
    
mainpage()                
window.mainloop()
print(detail)
print(mainl)
73047