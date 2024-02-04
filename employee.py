import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os

# Employee class for employee window
class Employee:
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

        self.var_id = StringVar()
        self.var_username = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_phone = StringVar()
        # self.var_address = StringVar()
        self.var_salary = StringVar()


        #========== Search Frame ==========
        searchFrame = LabelFrame(self.root, text="Search Employee", bg="#566573", fg="#fff")
        searchFrame.place(x=250, y=20, width=680, height=70)

        # ========== options ==========
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Select", "Username", "Email", "Gender", "Phone", "Address", "Salary"), state="readonly", justify=CENTER, font=("Montserrat", 13, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("Montserrat", 14, "bold"), bg="#DBE298").place(x=200, y=10)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=455, y=7, width=100, height=30)
        btn_show_all = Button(searchFrame, text="Show All", command=self.clear, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=570, y=7, width=100, height=30)

        # ========== title ==========
        title = Label(self.root, text="Employee Details", font=("Montserrat", 12, "bold"), bg="#2280C5", fg="#fff").place(x=50, y=110, width=980)

        # ========== content ==========
        # ====== row1 ==========
        lbl_username = Label(self.root, text="User Name", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=50, y=150)
        lbl_phone = Label(self.root, text="Phone", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=420, y=150)
        lbl_address = Label(self.root, text="Address", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=660, y=150)

        txt_username = Entry(self.root, textvariable=self.var_username, font=("Montserrat", 12), bg="#DBE298").place(x=150, y=150, width=230, height=25)
        txt_phone = Entry(self.root, textvariable=self.var_phone, font=("Montserrat", 12), bg="#DBE298").place(x=480, y=150, width=150, height=25)
        self.txt_address = Text(self.root, font=("Montserrat", 12), bg="#DBE298")
        self.txt_address.place(x=730, y=150, width=300, height=50)

        # ====== row2 ==========
        lbl_email = Label(self.root, text="Email", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=50,y=200)
        lbl_gender = Label(self.root, text="Gender", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=420, y=200)
        lbl_salary = Label(self.root, text="Salary", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=50,y=250)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("Montserrat", 12), bg="#DBE298").place(x=150, y=200, width=230, height=25)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER,font=("Montserrat", 13, "bold"))
        cmb_gender.place(x=480, y=200, width=180)
        cmb_gender.current(0)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("Montserrat", 12), bg="#DBE298").place(x=150,y=250,width=230,height=25)



        # ========== button ==========
        btn_add = Button(self.root, text="Add", command=self.add, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=480, y=250, width=110, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Montserrat", 12, "bold"), bg="#008CBA", fg="#fff", activebackground="#1B4F72", activeforeground="#fff", cursor="hand2").place(x=610, y=250, width=110, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Montserrat", 12, "bold"), bg="#f44336", fg="#fff", activebackground="#FF0000", activeforeground="#fff", cursor="hand2").place(x=740, y=250, width=110, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Montserrat", 12, "bold"), bg="#555555", fg="#fff", activebackground="#454545", activeforeground="#fff", cursor="hand2").place(x=870, y=250, width=110, height=30)


        # ========== Employee details table ============
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=300, relwidth=1, height=240)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("id", "username", "email", "gender", "phone", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("id", text="User ID")
        self.EmployeeTable.heading("username", text="User Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("phone", text="Phone")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("id", width=50)
        self.EmployeeTable.column("username", width=150)
        self.EmployeeTable.column("email", width=150)
        self.EmployeeTable.column("gender", width=150)
        self.EmployeeTable.column("phone", width=150)
        self.EmployeeTable.column("address", width=150)
        self.EmployeeTable.column("salary", width=150)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.getData)

        # Employee details show function
        self.show()



    # =============== add function =========
    def add(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_username.get() == "" or self.var_email.get() == "" or self.var_gender.get() == "Select" or self.var_phone.get() == "" or self.txt_address.get('1.0', END) == "" or self.var_salary.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            else:
                cur.execute("INSERT INTO employee (username,email, gender, phone, address, salary) values(?,?,?,?,?,?)", (
                    self.var_username.get(),
                    self.var_email.get(),
                    self.var_gender.get(),
                    self.var_phone.get(),
                    self.txt_address.get('1.0', END),
                    self.var_salary.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Employee added successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Show function =========
    def show(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Get data function =========
    def getData(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']
        self.var_id.set(row[0])
        self.var_username.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_phone.set(row[4])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[5])
        self.var_salary.set(row[6])

    # =============== update function =========
    def update(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_username.get() == "" or self.var_email.get() == "" or self.var_gender.get() == "Select" or self.var_phone.get() == "" or self.txt_address.get(
                    '1.0', END) == "" or self.var_salary.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            elif self.var_id.get() == "":
                messagebox.showerror("Error", "You can't update data without select any record", parent=self.root)
            else:
                cur.execute(
                    "UPDATE employee set username=?, email=?, gender=?, phone=?, address=?, salary=? WHERE id=?", (
                        self.var_username.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_phone.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_id.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Delete function =========
    def delete(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Please select an employee", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE id=?", (self.var_id.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid employee", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete this employee?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE id=?", (self.var_id.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Clear function =========
    def clear(self):
        self.var_id.set("")
        self.var_username.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_phone.set("")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
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
                cur.execute("SELECT * FROM employee WHERE " + self.var_searchby.get().lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)





if __name__ == "__main__":
    root = Tk()
    obj = Employee(root)
    root.mainloop()