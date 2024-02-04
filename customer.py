import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os

# Customer class
class Customer:
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
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_gender = StringVar()
        self.var_nationality = StringVar()
        self.var_idtype = StringVar()
        self.var_idnumber = StringVar()
        # self.var_address = StringVar()

        # ========== title ==========
        title = Label(self.root, text="Customer Details", font=("Montserrat", 12, "bold"), bg="#1B4F72", fg="#fff").place(x=0, y=0, relwidth=1, height=40)


        #========== Search Frame Start ==========
        searchFrame = LabelFrame(self.root, text="Search Customer", bg="#566573", fg="#fff")
        searchFrame.place(x=450, y=60, width=620, height=70)

        # ========== options ==========
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Select", "Name", "Email", "Phone", "Gender", "Nationality", "ID Type", "ID Number", "Address"), state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("Montserrat", 14, "bold"), bg="#DBE298").place(x=200, y=10, width=180)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_all = Button(searchFrame, text="Show All", command=self.clear, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)
        # ========== Search Frame End ==========

        # ========== Filter Frame Start ==========
        filterFrame = LabelFrame(self.root, text="Sort Customer", bg="#566573", fg="#fff")
        filterFrame.place(x=450, y=140, width=620, height=70)

        # ========== options ==========
        cmb_sort = ttk.Combobox(filterFrame, textvariable=self.var_sortby, values=("ID", "Name", "Email", "Phone", "Gender", "Nationality", "ID Type", "ID Number", "Address"),state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_sort.place(x=10, y=10, width=180)
        cmb_sort.current(0)
        cmb_order = ttk.Combobox(filterFrame, textvariable=self.var_orderby, values=("ASC", "DESC"),state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_order.place(x=200, y=10, width=180)
        cmb_order.current(0)
        btn_sort = Button(filterFrame, text="Sort", command=self.sort, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_default = Button(filterFrame, text="Default", command=self.sortDefault, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)
        # ========== Filter Frame End ==========

        # ========== content ==========
        # ========== Add Customer Frame ==========
        customerFrame = LabelFrame(self.root, text="Add New Customer", bg="#1C2833", fg="#fff")
        customerFrame.place(x=10, y=52, width=425, height=400)
        # ====== row1 ==========
        lbl_name = Label(self.root, text="Name", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=80)
        lbl_email = Label(self.root, text="Email", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=120)
        lbl_phone = Label(self.root, text="Phone", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=160)
        lbl_gender = Label(self.root, text="Gender", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=200)
        lbl_nationality = Label(self.root, text="Nationality", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=240)
        lbl_idtype = Label(self.root, text="ID type", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=280)
        lbl_idnumber = Label(self.root, text="ID Number", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=320)
        lbl_address = Label(self.root, text="Address", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=360)


        txt_name = Entry(self.root, textvariable=self.var_name, font=("Montserrat", 12), bg="#DBE298").place(x=120, y=80, width=300, height=25)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=120,width=300,height=25)
        txt_phone = Entry(self.root, textvariable=self.var_phone, font=("Montserrat", 12), bg="#DBE298").place(x=120, y=160, width=300, height=25)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER,font=("Montserrat", 13, "bold"))
        cmb_gender.place(x=120, y=200, width=300)
        cmb_gender.current(0)
        txt_nationality = Entry(self.root, textvariable=self.var_nationality, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=240,width=300,height=25)
        cmb_idtype = ttk.Combobox(self.root, textvariable=self.var_idtype, values=("Select", "NID", "Passport", "Driving Licence"), state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_idtype.place(x=120, y=280, width=300)
        cmb_idtype.current(0)
        txt_idnumber = Entry(self.root, textvariable=self.var_idnumber, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=320,width=300,height=25)
        self.txt_address = Text(self.root, font=("Montserrat", 12), bg="#DBE298")
        self.txt_address.place(x=120, y=360, width=300, height=70)



        # ========== button ==========
        btn_add = Button(self.root, text="Add", command=self.add, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=10, y=475, width=95, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Montserrat", 12, "bold"), bg="#008CBA", fg="#fff", activebackground="#1B4F72", activeforeground="#fff", cursor="hand2").place(x=120, y=475, width=95, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Montserrat", 12, "bold"), bg="#f44336", fg="#fff", activebackground="#FF0000", activeforeground="#fff", cursor="hand2").place(x=230, y=475, width=95, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Montserrat", 12, "bold"), bg="#555555", fg="#fff", activebackground="#454545", activeforeground="#fff", cursor="hand2").place(x=340, y=475, width=95, height=30)


        # ========== Customer details table ============
        tbl_frame = Frame(self.root, bd=3, relief=RIDGE)
        tbl_frame.place(x=450, y=220, width=620, height=310)

        scrolly = Scrollbar(tbl_frame, orient=VERTICAL)
        scrollx = Scrollbar(tbl_frame, orient=HORIZONTAL)

        self.CustomerTable = ttk.Treeview(tbl_frame, columns=("id", "name", "email", "phone", "gender", "nationality", "idtype", "idnumber", "address"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CustomerTable.xview)
        scrolly.config(command=self.CustomerTable.yview)
        self.CustomerTable.heading("id", text="User ID")
        self.CustomerTable.heading("name", text="Name")
        self.CustomerTable.heading("email", text="Email")
        self.CustomerTable.heading("phone", text="Phone")
        self.CustomerTable.heading("gender", text="Gender")
        self.CustomerTable.heading("nationality", text="Nationality")
        self.CustomerTable.heading("idtype", text="ID Type")
        self.CustomerTable.heading("idnumber", text="ID Number")
        self.CustomerTable.heading("address", text="Address")

        self.CustomerTable["show"] = "headings"

        self.CustomerTable.column("id", width=50)
        self.CustomerTable.column("name", width=150)
        self.CustomerTable.column("email", width=150)
        self.CustomerTable.column("phone", width=150)
        self.CustomerTable.column("gender", width=150)
        self.CustomerTable.column("nationality", width=150)
        self.CustomerTable.column("idtype", width=150)
        self.CustomerTable.column("idnumber", width=150)
        self.CustomerTable.column("address", width=150)

        self.CustomerTable.pack(fill=BOTH, expand=1)
        self.CustomerTable.bind("<ButtonRelease-1>", self.getData)

        # Customer details show function
        self.show()



    # =============== add function =========
    def add(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_gender.get() == "Select" or self.var_nationality.get() == "" or self.var_idtype.get() == "Select" or self.var_idnumber.get() == "" or self.txt_address.get('1.0', END) == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            else:
                cur.execute("SELECT * FROM customer WHERE phone LIKE '%" + self.var_phone.get() + "'")
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Phone number already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO customer (name, email, phone, gender, nationality, idtype, idnumber, address) values(?,?,?,?,?,?,?,?)", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_gender.get(),
                        self.var_nationality.get(),
                        self.var_idtype.get(),
                        self.var_idnumber.get(),
                        self.txt_address.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Customer added successfully", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Show function =========
    def show(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM customer")
            rows = cur.fetchall()
            self.CustomerTable.delete(*self.CustomerTable.get_children())
            for row in rows:
                self.CustomerTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Get data function =========
    def getData(self, ev):
        f = self.CustomerTable.focus()
        content = self.CustomerTable.item(f)
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_phone.set(str(row[3]))
        self.var_gender.set(row[4])
        self.var_nationality.set(row[5])
        self.var_idtype.set(row[6])
        self.var_idnumber.set(row[7])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[8])

    # =============== update function =========
    def update(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_gender.get() == "Select" or self.var_nationality.get() == "" or self.var_idtype.get() == "Select" or self.var_idnumber.get() == "" or self.txt_address.get(
                    '1.0', END) == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            elif self.var_id.get() == "":
                messagebox.showerror("Error", "You can't update data without select any record", parent=self.root)
            else:
                try:
                    cur.execute("SELECT * FROM customer WHERE phone=" + self.var_phone.get() + " ")
                    row = cur.fetchone()

                    if row != None and int(row[0]) != int(self.var_id.get()):
                        messagebox.showerror("Error", "Phone number already exists", parent=self.root)
                    else:
                        cur.execute(
                            "UPDATE customer set name=?, email=?, phone=?, gender=?, nationality=?, idtype=?, idnumber=?, address=? WHERE id=?", (
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_phone.get(),
                                self.var_gender.get(),
                                self.var_nationality.get(),
                                self.var_idtype.get(),
                                self.var_idnumber.get(),
                                self.txt_address.get('1.0', END),
                                self.var_id.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Success", "Customer updated successfully", parent=self.root)
                        self.clear()

                except Exception as ex:
                    messagebox.showerror("Error", "Phone number already exists", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Delete function =========
    def delete(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Please select an customer", parent=self.root)
            else:
                cur.execute("SELECT * FROM customer WHERE id=?", (self.var_id.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid customer", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete this customer?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM customer WHERE id=?", (self.var_id.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Customer deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Clear function =========
    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_gender.set("Select")
        self.var_nationality.set("")
        self.var_idtype.set("Select")
        self.var_idnumber.set("")
        self.txt_address.delete('1.0', END)
        self.var_searchby.set("Select")
        self.var_sortby.set("ID")
        self.var_orderby.set("ASC")
        self.var_searchtxt.set("")
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
                cur.execute("SELECT * FROM customer WHERE " + self.var_searchby.get().replace(" ", "").lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.CustomerTable.delete(*self.CustomerTable.get_children())
                    for row in rows:
                        self.CustomerTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Sort function =========
    def sort(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM customer ORDER BY " + self.var_sortby.get().replace(" ", "").lower() + " " + self.var_orderby.get() + " ")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.CustomerTable.delete(*self.CustomerTable.get_children())
                for row in rows:
                    self.CustomerTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)


    # =============== Sort default ============
    def sortDefault(self):
        self.var_sortby.set("ID")
        self.var_orderby.set("ASC")
        self.sort()





if __name__ == "__main__":
    root = Tk()
    obj = Customer(root)
    root.mainloop()