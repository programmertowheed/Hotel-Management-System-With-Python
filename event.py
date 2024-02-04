import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os

# Event class for event window
class Event:
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
        self.var_title = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        # ========== title ==========
        title = Label(self.root, text="Event Details", font=("Montserrat", 12, "bold"), bg="#1B4F72", fg="#fff").place(
            x=0, y=0, relwidth=1, height=40)

        #========== Search Frame ==========
        searchFrame = LabelFrame(self.root, text="Search Event", bg="#566573", fg="#fff")
        searchFrame.place(x=450, y=60, width=620, height=70)

        # ========== options ==========
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Select", "Title", "Date", "Time"), state="readonly", justify=LEFT, font=("Montserrat", 13, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("Montserrat", 14, "bold"), bg="#DBE298").place(x=200, y=10, width=180)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_all = Button(searchFrame, text="Show All", command=self.clear, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)


        # ========== content ==========
        eventFrame = LabelFrame(self.root, text="Add New Event", bg="#1C2833", fg="#fff")
        eventFrame.place(x=10, y=52, width=425, height=280)
        # ====== row1 ==========
        lbl_title = Label(self.root, text="Title", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=80)
        lbl_details = Label(self.root, text="Details", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=130)
        lbl_date = Label(self.root, text="Date", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=230)
        lbl_time = Label(self.root, text="Time", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=280)

        txt_title = Entry(self.root, textvariable=self.var_title, font=("Montserrat", 12), bg="#DBE298").place(x=100, y=80, width=300, height=35)
        self.txt_details = Text(self.root, font=("Montserrat", 12), bg="#DBE298")
        self.txt_details.place(x=100, y=130, width=300, height=80)
        txt_date = Entry(self.root, textvariable=self.var_date, font=("Montserrat", 12), bg="#DBE298").place(x=100, y=230, width=300, height=35)
        txt_time = Entry(self.root, textvariable=self.var_time, font=("Montserrat", 12), bg="#DBE298").place(x=100,y=280,width=300,height=35)

        # ========== button ==========
        btn_add = Button(self.root, text="Add", command=self.add, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=10, y=350, width=95, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Montserrat", 12, "bold"), bg="#008CBA", fg="#fff", activebackground="#1B4F72", activeforeground="#fff", cursor="hand2").place(x=120, y=350, width=95, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Montserrat", 12, "bold"), bg="#f44336", fg="#fff", activebackground="#FF0000", activeforeground="#fff", cursor="hand2").place(x=230, y=350, width=95, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Montserrat", 12, "bold"), bg="#555555", fg="#fff", activebackground="#454545", activeforeground="#fff", cursor="hand2").place(x=340, y=350, width=95, height=30)


        # ========== Event details table ============
        tbl_frame = Frame(self.root, bd=3, relief=RIDGE)
        tbl_frame.place(x=450, y=140, width=620, height=400)

        scrolly = Scrollbar(tbl_frame, orient=VERTICAL)
        scrollx = Scrollbar(tbl_frame, orient=HORIZONTAL)

        self.EventTable = ttk.Treeview(tbl_frame, columns=("id", "title", "details", "date", "time"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EventTable.xview)
        scrolly.config(command=self.EventTable.yview)
        self.EventTable.heading("id", text="Event ID")
        self.EventTable.heading("title", text="Event title")
        self.EventTable.heading("details", text="Event details")
        self.EventTable.heading("date", text="Event date")
        self.EventTable.heading("time", text="Event time")

        self.EventTable["show"] = "headings"

        self.EventTable.column("id", width=50)
        self.EventTable.column("title", width=150)
        self.EventTable.column("details", width=150)
        self.EventTable.column("date", width=150)
        self.EventTable.column("time", width=150)

        self.EventTable.pack(fill=BOTH, expand=1)
        self.EventTable.bind("<ButtonRelease-1>", self.getData)

        # Event details show function
        self.show()



    # =============== add function =========
    def add(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_title.get() == "" or self.txt_details.get('1.0', END) == "" or self.var_date.get() == "" or self.var_time.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            else:
                cur.execute("INSERT INTO event (title,details,date, time) values(?,?,?,?)", (
                    self.var_title.get(),
                    self.txt_details.get('1.0', END),
                    self.var_date.get(),
                    self.var_time.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Event added successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Show function =========
    def show(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM event")
            rows = cur.fetchall()
            self.EventTable.delete(*self.EventTable.get_children())
            for row in rows:
                self.EventTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Get data function =========
    def getData(self, ev):
        f = self.EventTable.focus()
        content = self.EventTable.item(f)
        row = content['values']
        self.var_id.set(row[0])
        self.var_title.set(row[1])
        self.txt_details.delete('1.0', END)
        self.txt_details.insert(END, row[2])
        self.var_date.set(row[3])
        self.var_time.set(row[4])

    # =============== update function =========
    def update(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_title.get() == ""  or self.txt_details.get('1.0', END) == "" or self.var_date.get() == "" or self.var_time.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            elif self.var_id.get() == "":
                messagebox.showerror("Error", "You can't update data without select any record", parent=self.root)
            else:
                cur.execute(
                    "UPDATE event set title=?, details=?, date=?, time=? WHERE id=?", (
                        self.var_title.get(),
                        self.txt_details.get('1.0', END),
                        self.var_date.get(),
                        self.var_time.get(),
                        self.var_id.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Event updated successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Delete function =========
    def delete(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Please select an event", parent=self.root)
            else:
                cur.execute("SELECT * FROM event WHERE id=?", (self.var_id.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid event", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete this event?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM event WHERE id=?", (self.var_id.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Event deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Clear function =========
    def clear(self):
        self.var_id.set("")
        self.var_title.set("")
        self.txt_details.delete('1.0', END)
        self.var_date.set("")
        self.var_time.set("")
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
                cur.execute("SELECT * FROM event WHERE " + self.var_searchby.get().lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EventTable.delete(*self.EventTable.get_children())
                    for row in rows:
                        self.EventTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)





if __name__ == "__main__":
    root = Tk()
    obj = Event(root)
    root.mainloop()