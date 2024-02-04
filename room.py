from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os


class Room:
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
        self.var_floor = StringVar()
        self.var_roomno = StringVar()
        self.var_roomtype = StringVar()

        # ========== Title ==========
        title = Label(self.root, text="Room Details", font=("Montserrat", 12, "bold"), bg="#1B4F72", fg="#fff").place(
            x=0, y=0, relwidth=1, height=40)

        #========== Search Frame ==========
        searchFrame = LabelFrame(self.root, text="Search Room", bg="#566573", fg="#fff")
        searchFrame.place(x=450, y=60, width=620, height=70)

        # ========== options ==========
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Select", "Floor", "Room No", "Room Type"), state="readonly", justify=LEFT, font=("Montserrat", 13, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("Montserrat", 14, "bold"), bg="#DBE298").place(x=200, y=10, width=180)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=395, y=7, width=100, height=30)
        btn_show_all = Button(searchFrame, text="Show All", command=self.clear, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=510, y=7, width=100, height=30)


        # ========== content ==========
        # ========== Add Room Frame ==========
        roomFrame = LabelFrame(self.root, text="Add New Room", bg="#1C2833", fg="#fff")
        roomFrame.place(x=10, y=60, width=425, height=210)
        # ====== row1 ==========
        lbl_floor = Label(self.root, text="Floor", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20, y=90)
        lbl_roomno = Label(self.root, text="Room No", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=150)
        lbl_roomno = Label(self.root, text="Room Type", font=("Montserrat", 12), fg="#fff", bg="#1C2833").place(x=20,y=210)

        lbl_floor = Entry(self.root, textvariable=self.var_floor, font=("Montserrat", 12), bg="#DBE298").place(x=120, y=90, width=300, height=35)
        lbl_roomno = Entry(self.root, textvariable=self.var_roomno, font=("Montserrat", 12), bg="#DBE298").place(x=120, y=150, width=300, height=35)
        lbl_roomtype = Entry(self.root, textvariable=self.var_roomtype, font=("Montserrat", 12), bg="#DBE298").place(x=120,y=210,width=300,height=35)

        # ========== button ==========
        btn_add = Button(self.root, text="Add", command=self.add, font=("Montserrat", 12, "bold"), bg="#196F3D", fg="#fff", activebackground="#088340", activeforeground="#fff", cursor="hand2").place(x=10, y=300, width=95, height=30)
        btn_uproomno = Button(self.root, text="Update", command=self.update, font=("Montserrat", 12, "bold"), bg="#008CBA", fg="#fff", activebackground="#1B4F72", activeforeground="#fff", cursor="hand2").place(x=120, y=300, width=95, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Montserrat", 12, "bold"), bg="#f44336", fg="#fff", activebackground="#FF0000", activeforeground="#fff", cursor="hand2").place(x=230, y=300, width=95, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Montserrat", 12, "bold"), bg="#555555", fg="#fff", activebackground="#454545", activeforeground="#fff", cursor="hand2").place(x=340, y=300, width=95, height=30)


        # ========== Room details table ============
        tbl_frame = Frame(self.root, bd=3, relief=RIDGE)
        tbl_frame.place(x=450, y=140, width=620, height=400)

        scrolly = Scrollbar(tbl_frame, orient=VERTICAL)
        scrollx = Scrollbar(tbl_frame, orient=HORIZONTAL)

        self.RoomTable = ttk.Treeview(tbl_frame, columns=("id", "floor", "roomno", "roomtype"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.RoomTable.xview)
        scrolly.config(command=self.RoomTable.yview)
        self.RoomTable.heading("id", text="Room ID")
        self.RoomTable.heading("floor", text="Room Floor")
        self.RoomTable.heading("roomno", text="Room Room No")
        self.RoomTable.heading("roomtype", text="Room Room Type")

        self.RoomTable["show"] = "headings"

        self.RoomTable.column("id", width=50)
        self.RoomTable.column("floor", width=150)
        self.RoomTable.column("roomno", width=150)
        self.RoomTable.column("roomtype", width=150)

        self.RoomTable.pack(fill=BOTH, expand=1)
        self.RoomTable.bind("<ButtonRelease-1>", self.getData)

        # Room details show function
        self.show()



    # =============== add function =========
    def add(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_floor.get() == "" or self.var_roomno.get() == "" or self.var_roomtype.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            else:
                cur.execute("INSERT INTO room (floor,roomno, roomtype) values(?,?,?)", (
                    self.var_floor.get(),
                    self.var_roomno.get(),
                    self.var_roomtype.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Room added successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Show function =========
    def show(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM room")
            rows = cur.fetchall()
            self.RoomTable.delete(*self.RoomTable.get_children())
            for row in rows:
                self.RoomTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Get data function =========
    def getData(self, ev):
        f = self.RoomTable.focus()
        content = self.RoomTable.item(f)
        row = content['values']
        self.var_id.set(row[0])
        self.var_floor.set(row[1])
        self.var_roomno.set(row[2])
        self.var_roomtype.set(row[3])

    # =============== uproomno function =========
    def update(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_floor.get() == "" or self.var_roomno.get() == "" or self.var_roomtype.get() == "":
                messagebox.showerror("Error", "Field must not be empty", parent=self.root)
            elif self.var_id.get() == "":
                messagebox.showerror("Error", "You can't update data without select any record", parent=self.root)
            else:
                cur.execute(
                    "UPDATE room set floor=?, roomno=?, roomtype=? WHERE id=?", (
                        self.var_floor.get(),
                        self.var_roomno.get(),
                        self.var_roomtype.get(),
                        self.var_id.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Room updated successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Delete function =========
    def delete(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Please select an room", parent=self.root)
            else:
                cur.execute("SELECT * FROM room WHERE id=?", (self.var_id.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid room", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete this room?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM room WHERE id=?", (self.var_id.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Room deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)

    # =============== Clear function =========
    def clear(self):
        self.var_id.set("")
        self.var_floor.set("")
        self.var_roomno.set("")
        self.var_roomtype.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    # =============== Clear function =========
    def search(self):
        con = sqlite3.connect(database=r'hms.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM room WHERE " + self.var_searchby.get().replace(" ", "").lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.RoomTable.delete(*self.RoomTable.get_children())
                    for row in rows:
                        self.RoomTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error for : {str(ex)}", parent=self.root)





if __name__ == "__main__":
    root = Tk()
    obj = Room(root)
    root.mainloop()