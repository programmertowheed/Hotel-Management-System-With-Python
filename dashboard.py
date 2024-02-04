from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from tkinter import ttk
from PIL import ImageTk, Image
from reservation import Reservation
from customer import Customer
from room import Room
from admin import Admin
from employee import Employee
from event import Event

# App class for dashboard
class App:
    def __init__(self, root):
        self.newWindow = None
        self.root = root
        self.root.title('Hotel Management System')
        self.root.geometry('1300x650+20+20')
        self.root.resizable(0, 0)
        self.root.configure(bg="#fff")
        # windows only (remove the minimize/maximize button)
        self.root.attributes('-toolwindow', False)

        # Welcome text for dashboard
        self.var_username = "Welcome"

        # Check user login or not start
        file = open('logdetails.txt', 'r')
        txt = file.read()
        content = txt.split(",")
        if len(content) != 2:
            self.root.destroy()
            os.system("python main.py")
        else:
            usercontent = content[0].split("=")
            user = usercontent[1]
            self.var_username = "Welcome, " + user
            logincontent = content[1].split("=")
            logincon = logincontent[1]
            if logincon != "true":
                self.root.destroy()
                os.system("python main.py")
        # check user login or not end

        # Main Frame
        self.mainFrame = ttk.Frame(self.root).pack()

        ################################============= Title ==================###############################
        title = Label(self.mainFrame, text="Hotel Management System", font=("Montserrat", 15, "bold"), compound=LEFT, anchor="w", padx=30, bg="#0f172a", fg="#fff").place(x=200, y=0, relwidth=1, height=40)

        # ============= User Image ==================
        self.userImage = Image.open("photo/user.png")
        self.userImage = self.userImage.resize((30,30), Image.LANCZOS)
        self.userImage = ImageTk.PhotoImage(self.userImage)
        self.user = Label(self.mainFrame, text=self.var_username, image=self.userImage, compound=LEFT, font=("Montserrat", 10, "bold"), padx=10, bg="#0f172a", fg="#fff").place(x=970, y=3)

        ################################============= Left menu start ==================###############################
        # ============= left logo ==================
        self.MenuLogo = Image.open("photo/logoimage.png")
        self.MenuLogo = self.MenuLogo.resize((200,100), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        # Menu Frame
        leftMenu = Frame(self.mainFrame, bd=1, relief=RIDGE, bg="#0f172a")
        leftMenu.place(x=0, y=0, width=200, height=650)

        # Menu Logo
        lbl_menuLogo = Label(leftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)
        # Border bottom
        Frame(leftMenu, width=200, height=2, bg='#D35400').place(x=0, y=102)

        self.dashboard_icon = self.image_resize("dashboard.png")
        btn_dashboard = Button(leftMenu, text="DASHBOARD", image=self.dashboard_icon, command=self.dashboard,
                                 compound=LEFT, padx=8, pady=5, font=("Montserrat", 10, "bold"), bg="#082F4F",
                                 activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w",
                                 cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=150)


        self.reservation_icon = self.image_resize("reservation.png")
        btn_reservation = Button(leftMenu, text="RESERVATION", image=self.reservation_icon, command=self.reservationWin, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=197)

        self.customer_icon = self.image_resize("customer.png")
        btn_customer = Button(leftMenu, text="CUSTOMER", image=self.customer_icon, command=self.customerWin, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=244)

        self.home_icon = self.image_resize("home2.png")
        btn_room = Button(leftMenu, text="ROOM", image=self.home_icon, command=self.roomWin, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=291)

        self.admin_icon = self.image_resize("admin.png")
        btn_admin = Button(leftMenu, text="ADMIN", image=self.admin_icon, command=self.adminWin, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=338)

        self.employee_icon = self.image_resize("employee.png")
        btn_employee = Button(leftMenu, text="EMPLOYEE", command=self.employeeWin, image=self.employee_icon, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=385)

        self.event_icon = self.image_resize("event.png")
        btn_event = Button(leftMenu, text="EVENT", image=self.event_icon, command=self.eventWin, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=430)

        self.logOut_icon = self.image_resize("logout.png")
        btn_log_out = Button(leftMenu, text="LOG OUT", image=self.logOut_icon, command=self.logout, compound=LEFT, padx=8, pady=5 , font=("Montserrat", 10, "bold"), bg="#082F4F", activebackground='#020A11', activeforeground="#fff", fg="#fff", bd=0, anchor="w", cursor="hand2", height=35).pack(side=TOP, fill=X)
        # Frame(leftMenu, width=200, height=1, bg='#A8A8A9').place(x=0, y=475)
        ################################============= Left menu end ==================###############################


        ################################============= Content start ==================###############################
        self.lbl_reservation = Label(self.mainFrame, text="Total Reservation\n 0", bg="#229954", fg="#fff",
                                     font=("Montserrat", 15, "bold"))
        self.lbl_reservation.place(x=220, y=60, height=130, width=250)

        self.lbl_customer = Label(self.mainFrame, text="Total Customer\n 0", bg="#21618C", fg="#fff",
                                  font=("Montserrat", 15, "bold"))
        self.lbl_customer.place(x=490, y=60, height=130, width=250)

        self.lbl_room = Label(self.mainFrame, text="Total Room\n 0", bg="#34495E", fg="#fff",
                              font=("Montserrat", 15, "bold"))
        self.lbl_room.place(x=760, y=60, height=130, width=250)

        self.lbl_admin = Label(self.mainFrame, text="Total Admin\n 0", bg="#1C2833", fg="#fff",
                               font=("Montserrat", 15, "bold"))
        self.lbl_admin.place(x=1030, y=60, height=130, width=250)

        self.lbl_employee = Label(self.mainFrame, text="Total Employee\n 0", bg="#AF601A", fg="#fff",
                                  font=("Montserrat", 15, "bold"))
        self.lbl_employee.place(x=220, y=210, height=130, width=250)

        self.lbl_event = Label(self.mainFrame, text="Total Event\n 0", bg="#884EA0", fg="#fff",
                               font=("Montserrat", 15, "bold"))
        self.lbl_event.place(x=490, y=210, height=130, width=250)
        ################################============= Content end ==================###############################


        ################################============= Footer ==================###############################
        footer = Label(self.mainFrame, text="Hotel Management System | Develop by Jesmin", font=("Montserrat", 10, "bold"), compound=LEFT,
                      anchor="w", padx=780, bg="#0f172a", fg="#fff").place(x=200, y=620, relwidth=1, height=30)

        self.update_statics()

    # Image resize function
    def image_resize(self, image):
        path = "photo/" + image
        image_icon = Image.open(path)
        image_icon = image_icon.resize((22, 22), Image.LANCZOS)
        image_icon = ImageTk.PhotoImage(image_icon)
        return image_icon

    # Dashboard
    def dashboard(self):
        self.close()

    # Reservation window
    def reservationWin(self):
        self.close()
        self.reservation_win = Toplevel(self.root)
        self.newWindow = Reservation(self.reservation_win)

    # Customer window
    def customerWin(self):
        self.close()
        self.customer_win = Toplevel(self.root)
        self.newWindow = Customer(self.customer_win)

    # Room window
    def roomWin(self):
        self.close()
        self.room_win = Toplevel(self.root)
        self.newWindow = Room(self.room_win)

    # Admin window
    def adminWin(self):
        self.close()
        self.admin_win = Toplevel(self.root)
        self.newWindow = Admin(self.admin_win)

    # Employee window
    def employeeWin(self):
        self.close()
        self.employee_win = Toplevel(self.root)
        self.newWindow = Employee(self.employee_win)

    # Event window
    def eventWin(self):
        self.close()
        self.event_win = Toplevel(self.root)
        self.newWindow = Event(self.event_win)

    # Logout
    def logout(self):
        text = ""
        textFile = open('logdetails.txt', 'w')
        textFile.write(text)
        textFile.close()
        self.root.destroy()
        os.system("python main.py")

    # Close child window
    def close(self):
        if self.newWindow != None:
            self.newWindow.root.destroy()

    # Update dashboard content
    def update_statics(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM reservation")
            reservation = cur.fetchall()
            self.lbl_reservation.config(text=f'Total Reservation\n {str(len(reservation))}')

            cur.execute("SELECT * FROM customer")
            customer = cur.fetchall()
            self.lbl_customer.config(text=f'Total Customer\n {str(len(customer))}')

            cur.execute("SELECT * FROM room")
            room = cur.fetchall()
            self.lbl_room.config(text=f'Total Room\n {str(len(room))}')

            cur.execute("SELECT * FROM admin")
            admin = cur.fetchall()
            self.lbl_admin.config(text=f'Total Admin\n {str(len(admin))}')

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee\n {str(len(employee))}')

            cur.execute("SELECT * FROM event")
            event = cur.fetchall()
            self.lbl_event.config(text=f'Total Event\n {str(len(event))}')

            self.root.after(200, self.update_statics)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()


