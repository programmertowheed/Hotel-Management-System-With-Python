import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
from datetime import date
from datetime import datetime
import os


# Reservation class for reservation window
class Reservation:
    def __init__(self, root):
        self.root = root
        self.root.title('Hotel Management System')
        self.root.geometry('1080x535+230+100')
        self.root.resizable(0, 0)
        self.root.configure(bg="#1C2833")
        # windows only (remove the minimize/maximize button)
        self.root.attributes('-toolwindow', True)
        # self.root.overrideredirect(True)
        self.root.focus_force()


        # checklogin or not start
        file = open('logdetails.txt', 'r')
        txt = file.read()
        content = txt.split(",")
        if len(content) != 2:
            self.root.destroy()
            os.system("python main.py")
        else:
            logincontent = content[1].split("=")
            logincon = logincontent[1]
            if logincon != "true":
                self.root.destroy()
                os.system("python main.py")
        # checklogin or not end


        # ========== All Variables ==========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sortby = StringVar()
        self.var_orderby = StringVar()

        self.var_id = StringVar()
        self.var_contact = StringVar()
        self.var_checkin = StringVar()
        self.var_checkout = StringVar()
        self.var_roomtype = StringVar()
        self.var_roomno = StringVar()

        self.var_get_roomtype = ["Select"]
        self.var_get_roomno = ["Select"]

        self.getRoomType()

        # ========== Title ==========
        title = Label(self.root, text="Reservation Details", font=("Montserrat", 12, "bold"), bg="#1B4F72", fg="#fff").place(
            x=0, y=0, relwidth=1, height=40)

        #========== Search Frame ==========
        searchFrame = LabelFrame(self.root, text="Search Reservation", bg="#566573", fg="#fff")
        searchFrame.place(x=450, y=52, width=620, height=70)

        # ========== options ==========
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Select", "Contact", "Check In", "Check Out", "Room Type", "Room No"), state="readonly", justify=LEFT, font=("Montserrat", 13, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("Montserrat", 14, "bold"), bg="#DBE298").place(x=200, y=10, width=180)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_all = Button(searchFrame, text="Show All", command=self.clear, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)


        # ========== Filter Frame Start ==========
        filterFrame = LabelFrame(self.root, text="Sort Reservation", bg="#566573", fg="#fff")
        filterFrame.place(x=450, y=140, width=620, height=70)

        # ========== options ==========
        cmb_sort = ttk.Combobox(filterFrame, textvariable=self.var_sortby, values=("ID", "Contact", "Check In", "Check Out", "Room Type", "Room No"),state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_sort.place(x=10, y=10, width=180)
        cmb_sort.current(0)
        cmb_order = ttk.Combobox(filterFrame, textvariable=self.var_orderby, values=("ASC", "DESC"),state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_order.place(x=200, y=10, width=180)
        cmb_order.current(0)
        btn_sort = Button(filterFrame, text="Sort", command=self.sort, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_default = Button(filterFrame, text="Default", command=self.sortDefault, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)
        # ========== Filter Frame End ==========

        # ========== content ==========
        # ========== Add Reservation Frame ==========
        reservationFrame = LabelFrame(self.root, text="Add New Reservation", bg="#1C2833", fg="#fff")
        reservationFrame.place(x=10, y=45, width=425, height=230)
        # ====== row1 ==========
        lbl_contact = Label(self.root, text="Contact", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=70)
        lbl_checkin = Label(self.root, text="Check In", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=110)
        lbl_checkout = Label(self.root, text="Check Out", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=150)
        lbl_roomtype = Label(self.root, text="Room Type", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=190)
        lbl_roomno = Label(self.root, text="Room No", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=230)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Montserrat", 12), bg="#DBE298").place(x=120, y=70, width=215, height=25)
        self.txt_checkin = Entry(self.root, textvariable=self.var_checkin, state="readonly", font=("Montserrat", 12), bg="#DBE298").place(x=120, y=110, width=215, height=25)
        self.txt_checkout = Entry(self.root, textvariable=self.var_checkout, state="readonly", font=("Montserrat", 12), bg="#DBE298").place(x=120,y=150,width=215,height=25)
        # txt_roomtype = Entry(self.root, textvariable=self.var_roomtype, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=190,width=300,height=25)
        cmb_roomtype = ttk.Combobox(self.root, textvariable=self.var_roomtype, values=self.var_get_roomtype, state="readonly",justify=LEFT, font=("Montserrat", 13, "bold"))
        cmb_roomtype.place(x=120, y=190, width=300)
        cmb_roomtype.current(0)
        # txt_roomno = Entry(self.root, textvariable=self.var_roomno, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=230,width=300,height=25)
        cmb_roomno = ttk.Combobox(self.root, textvariable=self.var_roomno, values=self.var_get_roomno, state="readonly", justify=LEFT, font=("Montserrat", 13, "bold"))
        cmb_roomno.place(x=120, y=230, width=300)
        cmb_roomno.current(0)

        # ========== button ==========
        btn_get_customer = Button(self.root, text="Get", command=self.getCustomerData, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=350, y=68, width=75, height=30)
        btn_get_checkin_date = Button(self.root, text="Get Date", command=self.getCheckInData, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=350, y=108, width=75, height=30)
        btn_get_checkout_date = Button(self.root, text="Get Date", command=self.getCheckOutData, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=350, y=148, width=75, height=30)
        btn_add = Button(self.root, text="Add", command=self.add, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=10, y=290, width=95, height=30)
        btn_uproomtype = Button(self.root, text="Update", command=self.update, font=("Montserrat", 12, "bold"), bg="#008CBA", fg="#fff", activebackground="#1B4F72", activeforeground="#fff", cursor="hand2").place(x=120, y=290, width=95, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Montserrat", 12, "bold"), bg="#f44336", fg="#fff", activebackground="#FF0000", activeforeground="#fff", cursor="hand2").place(x=230, y=290, width=95, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Montserrat", 12, "bold"), bg="#555555", fg="#fff", activebackground="#454545", activeforeground="#fff", cursor="hand2").place(x=340, y=290, width=95, height=30)

        # ========== Customer Info Frame ==========
        self.customerInfoFrame = LabelFrame(self.root, text="Customer Info", bg="#1C2833", fg="#fff")
        self.customerInfoFrame.place(x=10, y=340, width=425, height=190)

        self.lbl_cus_name = Label(self.customerInfoFrame, text="Name", font=("Montserrat", 12), fg="#fff", bg="#1C2833")
        self.lbl_cus_name.place(x=10, y=5)
        self.lbl_cus_name_val = Label(self.customerInfoFrame, text="N/A", font=("Montserrat", 10), fg="#fff", bg="#1C2833")
        self.lbl_cus_name_val.place(x=100, y=5)
        self.lbl_cus_email = Label(self.customerInfoFrame, text="Email", font=("Montserrat", 12), fg="#fff", bg="#1C2833")
        self.lbl_cus_email.place(x=10, y=35)
        self.lbl_cus_email_val = Label(self.customerInfoFrame, text="N/A", font=("Montserrat", 10), fg="#fff", bg="#1C2833")
        self.lbl_cus_email_val.place(x=100, y=35)
        self.lbl_cus_phone = Label(self.customerInfoFrame, text="Phone", font=("Montserrat", 12), fg="#fff", bg="#1C2833")
        self.lbl_cus_phone.place(x=10, y=70)
        self.lbl_cus_phone_val = Label(self.customerInfoFrame, text="N/A", font=("Montserrat", 10), fg="#fff", bg="#1C2833")
        self.lbl_cus_phone_val.place(x=100, y=70)
        self.lbl_cus_nationality = Label(self.customerInfoFrame, text="Nationality", font=("Montserrat", 12), fg="#fff", bg="#1C2833")
        self.lbl_cus_nationality.place(x=10, y=100)
        self.lbl_cus_nationality_val = Label(self.customerInfoFrame, text="N/A", font=("Montserrat", 10), fg="#fff", bg="#1C2833")
        self.lbl_cus_nationality_val.place(x=100, y=100)
        self.lbl_cus_address = Label(self.customerInfoFrame, text="Address", font=("Montserrat", 12), fg="#fff", bg="#1C2833")
        self.lbl_cus_address.place(x=10, y=130)
        self.lbl_cus_address_val = Label(self.customerInfoFrame, text="N/A", font=("Montserrat", 10), fg="#fff", bg="#1C2833")
        self.lbl_cus_address_val.place(x=100, y=130)

        # ========== Reservation details table ============
        tbl_frame = Frame(self.root, bd=3, relief=RIDGE)
        tbl_frame.place(x=450, y=220, width=620, height=310)

        scrolly = Scrollbar(tbl_frame, orient=VERTICAL)
        scrollx = Scrollbar(tbl_frame, orient=HORIZONTAL)

        self.ReservationTable = ttk.Treeview(tbl_frame, columns=("id", "contact", "checkin", "checkout", "roomtype", "roomno"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ReservationTable.xview)
        scrolly.config(command=self.ReservationTable.yview)
        self.ReservationTable.heading("id", text="ID")
        self.ReservationTable.heading("contact", text="Contact")
        self.ReservationTable.heading("checkin", text="Check In")
        self.ReservationTable.heading("checkout", text="Check Out")
        self.ReservationTable.heading("roomtype", text="Room Type")
        self.ReservationTable.heading("roomno", text="Room No")

        self.ReservationTable["show"] = "headings"

        self.ReservationTable.column("id", width=50)
        self.ReservationTable.column("contact", width=150)
        self.ReservationTable.column("checkin", width=150)
        self.ReservationTable.column("checkout", width=150)
        self.ReservationTable.column("roomtype", width=150)
        self.ReservationTable.column("roomno", width=150)

        self.ReservationTable.pack(fill=BOTH, expand=1)
        self.ReservationTable.bind("<ButtonRelease-1>", self.getData)

        # Reservation details show function
        self.show()

    # ========== Get Room Type ===========
    def getRoomType(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        cur.execute("SELECT roomtype, roomno FROM room")
        rows = cur.fetchall()
        for t in rows:
            self.var_get_roomtype.append(t[0])
            self.var_get_roomno.append(t[1])

    # =============== add function =========
    def add(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_contact.get() == "" or self.var_checkin.get() == ""  or self.var_checkout.get() == ""  or self.var_roomtype.get() == "Select" or self.var_roomno.get() == "Select":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            else:
                cur.execute("SELECT * FROM customer WHERE phone=" + self.var_contact.get() + " ")
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Enter valid contact number", parent=self.root)
                else:
                    cur.execute("INSERT INTO reservation (contact,checkin,checkout,roomtype, roomno) values(?,?,?,?,?)", (
                        self.var_contact.get(),
                        self.var_checkin.get(),
                        self.var_checkout.get(),
                        self.var_roomtype.get(),
                        self.var_roomno.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Reservation added successfully", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Show function =========
    def show(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM reservation")
            rows = cur.fetchall()
            self.ReservationTable.delete(*self.ReservationTable.get_children())
            for row in rows:
                self.ReservationTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Get data function =========
    def getData(self, ev):
        f = self.ReservationTable.focus()
        content = self.ReservationTable.item(f)
        row = content['values']
        self.var_id.set(row[0])
        self.var_contact.set(row[1])
        self.var_checkin.set(row[2])
        self.var_checkout.set(row[3])
        self.var_roomtype.set(row[4])
        self.var_roomno.set(row[5])

    # =============== Update function =========
    def update(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_contact.get() == "" or self.var_checkin.get() == "" or self.var_checkout.get() == "" or self.var_roomtype.get() == "Select" or self.var_roomno.get() == "Select":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            elif self.var_id.get() == "":
                messagebox.showerror("Error", "You can't update data without select any record", parent=self.root)
            else:
                cur.execute(
                    "UPDATE reservation set contact=?, checkin=?, checkout=?, roomtype=?, roomno=? WHERE id=?", (
                        self.var_contact.get(),
                        self.var_checkin.get(),
                        self.var_checkout.get(),
                        self.var_roomtype.get(),
                        self.var_roomno.get(),
                        self.var_id.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Reservation updated successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Delete function =========
    def delete(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Please select a reservation", parent=self.root)
            else:
                cur.execute("SELECT * FROM reservation WHERE id=?", (self.var_id.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid reservation", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete this reservation?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM reservation WHERE id=?", (self.var_id.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Reservation deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Clear function =========
    def clear(self):
        self.var_id.set("")
        self.var_contact.set("")
        self.var_checkin.set("")
        self.var_checkout.set("")
        self.var_roomtype.set("Select")
        self.var_roomno.set("Select")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.var_sortby.set("ID")
        self.var_orderby.set("ASC")
        self.show()

    # =============== Search function =========
    def search(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM reservation WHERE " + self.var_searchby.get().replace(" ", "").lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ReservationTable.delete(*self.ReservationTable.get_children())
                    for row in rows:
                        self.ReservationTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Sort function =========
    def sort(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM reservation ORDER BY " + self.var_sortby.get().replace(" ", "").lower() + " " + self.var_orderby.get() + " ")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.ReservationTable.delete(*self.ReservationTable.get_children())
                for row in rows:
                    self.ReservationTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Sort default ============
    def sortDefault(self):
        self.var_sortby.set("ID")
        self.var_orderby.set("ASC")
        self.sort()


    # =============== Get Customer Info ============
    def getCustomerData(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_contact.get() == "":
                messagebox.showerror("Error", "Please input customer contact number", parent=self.root)
            else:
                cur.execute("SELECT * FROM customer WHERE phone=" + self.var_contact.get() + " ")
                row = cur.fetchone()
                if row == None:
                    self.lbl_cus_name_val.config(text="N/A")
                    self.lbl_cus_email_val.config(text="N/A")
                    self.lbl_cus_phone_val.config(text="N/A")
                    self.lbl_cus_nationality_val.config(text="N/A")
                    self.lbl_cus_address_val.config(text="N/A")
                    messagebox.showerror("Error", "Invalid contact number", parent=self.root)
                else:
                    self.lbl_cus_name_val.config(text=f'{str(row[1])}')
                    self.lbl_cus_email_val.config(text=f'{str(row[2])}')
                    self.lbl_cus_phone_val.config(text=f'{str(row[3])}')
                    self.lbl_cus_nationality_val.config(text=f'{str(row[5])}')
                    self.lbl_cus_address_val.config(text=f'{str(row[8])}')
        except Exception as ex:
            messagebox.showerror("Error", "Enter valid contact number", parent=self.root)

    # ================ Get check in date ============
    def getCheckInData(self):
        todays_date = date.today()
        year = todays_date.year
        month = todays_date.month
        day = todays_date.day

        self.cal_win = Toplevel(self.root)
        self.cal_win.geometry('300x280+660+180')
        self.cal_win.attributes('-toolwindow', True)
        self.cal = Calendar(self.cal_win, selectmode="day", year=year, month=month, day=day)
        self.cal.pack(padx=10, pady=10)
        date_btn = Button(self.cal_win, text="Get Date", command=self.getCheckIn, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2")
        date_btn.pack(padx=10, pady=10)

    # ================ Get check out date ============
    def getCheckOutData(self):
        todays_date = date.today()
        year = todays_date.year
        month = todays_date.month
        day = todays_date.day

        self.cal_win = Toplevel(self.root)
        self.cal_win.geometry('300x280+660+180')
        self.cal_win.attributes('-toolwindow', True)
        self.cal = Calendar(self.cal_win, selectmode="day", year=year, month=month, day=day)
        self.cal.pack(padx=10, pady=10)
        date_btn = Button(self.cal_win, text="Get Date", command=self.getCheckOut, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2")
        date_btn.pack(padx=10, pady=10)

    # Check in function
    def getCheckIn(self):
        self.var_checkin.set("")
        select_date = datetime.strptime(self.cal.get_date(), '%m/%d/%y').date()
        current_date = date.today()
        if select_date < current_date:
            messagebox.showerror("Error", "Can't select before today's date", parent=self.cal_win)
        else:
            self.var_checkin.set(select_date)
            self.cal_win.destroy()
            self.root.focus_force()

    # Check out function
    def getCheckOut(self):
        self.var_checkout.set("")
        select_date = datetime.strptime(self.cal.get_date(), '%m/%d/%y').date()
        checkin_date = datetime.strptime(self.var_checkin.get(), '%Y-%m-%d').date()

        if select_date < checkin_date:
            messagebox.showerror("Error", "Can't select before check in date", parent=self.cal_win)
        else:
            self.var_checkout.set(select_date)
            self.cal_win.destroy()
            self.root.focus_force()


if __name__ == "__main__":
    root = Tk()
    obj = Reservation(root)
    root.mainloop()