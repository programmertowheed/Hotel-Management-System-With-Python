import os
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import hashlib
import sqlite3

# Login class
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title('Login | Hotel Management System')
        self.root.geometry('925x500+200+50')
        imgIcon = ImageTk.PhotoImage(file='photo/icon.png')
        self.root.iconphoto(False, imgIcon)
        self.root.resizable(0, 0)
        self.root.configure(bg="#fff")
        # windows only (remove the minimize/maximize button)
        self.root.attributes('-toolwindow', False)
        self.fm = Frame(self.root).pack()

        # login submit handler
        def handle_login():
            user = username.get()
            passw = password.get()
            # passw = password.get().encode("utf-8")
            # hashpass = hashlib.md5(passw).hexdigest()

            if user == '' or passw == '':
                messagebox.showerror("Invalid", "username and password are required")
            elif user == '':
                messagebox.showerror("Invalid", "Username is required!")
            elif passw == '':
                messagebox.showerror("Invalid", "Password is required!")
            else:
                con = sqlite3.connect(database=r'hms.db')
                cur = con.cursor()
                cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (user,passw) )
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Incorrect username or password!", parent=self.root)
                else:
                    res = messagebox.showinfo("Success", "You are successfully logged in")
                    if res == 'ok':
                        text = "loginuser="+user+",login=true"
                        textFile = open('logdetails.txt', 'w')
                        textFile.write(text)
                        textFile.close()
                        self.root.destroy()
                        os.system("python dashboard.py")

        # Image
        self.img = ImageTk.PhotoImage(file='photo/log.png')
        Label(self.fm, image=self.img, bg="#fff").place(x=50, y=50)

        # From frame
        from_frame = Frame(self.fm, width=350, height=350, bg="#13162e")
        from_frame.place(x=480, y=70)

        # From heading
        fr_heading = Label(from_frame, text="Log In", fg="#38bdf8", bg="#13162e", font=("Montserrat", 23))
        fr_heading.place(x=125, y=5)

        ################# user field ----------------------------
        def on_enter(e):
            username.delete(0, 'end')

        def on_leave(e):
            name = username.get()
            if name == '':
                username.insert(0, 'Username')

        # username entry
        username = Entry(from_frame, width=25, fg='#fff', border=0, bg="#13162e", font=("Montserrat", 11))
        username.place(x=30, y=80)
        username.insert(0, 'Username')
        username.bind('<FocusIn>', on_enter)
        username.bind('<FocusOut>', on_leave)

        # Border bottom
        Frame(from_frame, width=295, height=2, bg='#fff').place(x=25, y=107)

        ####################### password -----------------------------
        def on_enter(e):
            password.delete(0, 'end')
            password.config(show="*")

        def on_leave(e):
            name = password.get()
            if name == '':
                password.config(show="")
                password.insert(0, 'Password')


        # password entry
        password = Entry(from_frame, width=25, fg='#fff', border=0, bg="#13162e", font=("Montserrat", 11))
        password.place(x=30, y=150)
        password.insert(0, 'Password')
        password.bind('<FocusIn>', on_enter)
        password.bind('<FocusOut>', on_leave)

        # Border bottom
        Frame(from_frame, width=295, height=2, bg='#fff').place(x=25, y=177)

        # Submit button
        Button(from_frame, width=27, pady=7, text="Log In", bg="#57a1f8", fg="#fff", border=0, cursor="hand2",
               command=handle_login, font=("Montserrat", 12, "bold")).place(x=35, y=224)


if __name__ == "__main__":
    root = Tk()
    LogPage = LoginPage(root)
    root.mainloop()


