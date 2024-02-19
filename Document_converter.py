from customtkinter import (CTk, CTkButton, CTkEntry, CTkFont, CTkImage, CTkFrame, CTkLabel, CTkTabview,
                           CTkOptionMenu, set_appearance_mode, CTkTextbox, CTkComboBox)
from tkinter import messagebox
from c_file import C_run
from run_any_file import run_File
from open_any_file import With_open
from submit_for_open import Document_File
from submit_for_text import Document_File_text
from snap_shot import snap, retrieve_images, clear_database
from os import path
from PIL import Image
from output_location import location_folder
class App(CTk):
    def __init__(self):
        super().__init__()

        # size fixing center of the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 900
        window_height = 800

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # title of application
        self.title("Document Creator")

        # stopping the resizing of the application
        self.resizable(False, False)

        #intial items
        self.default_font = CTkFont(size=20)
        self.sp_font = CTkFont(size=40, weight="bold")
        self.counter_index = 1
        self.list_open,self.image_list,self.temp = [],[],[]
        self.list_code_text,self.list_prob_text = [],[]
        self.location_file = ""
        # initialize the application grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # main frame that contain title
        self.main_frame = CTkFrame(self, height=200)
        self.main_frame.grid(row=0, column=0, padx=5, pady=(0, 0), sticky="new")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        self.logo_frame = CTkFrame(self.main_frame,height=50,width=400)
        self.logo_frame.grid(row=0,column = 0, padx=5 ,pady=(5,5),sticky="nsw")

        image_path = path.join(path.dirname(path.realpath(__file__)), "image")

        self.logo_img = CTkImage(Image.open(path.join(image_path, "Main_logo.png")), size=(36, 36))

        self.c_logo_img = CTkImage(dark_image=Image.open(path.join(image_path,"c_logo_light.png")),
                                       light_image=Image.open(path.join(image_path,"c_logo_dark.png")),
                                       size=(70,100))
        
        self.j_logo_img = CTkImage(dark_image=Image.open(path.join(image_path,"j_logo_light.png")),
                                       light_image=Image.open(path.join(image_path,"j_logo_dark.png")),
                                       size=(70,100))
        
        self.p_logo_img = CTkImage(dark_image=Image.open(path.join(image_path,"p_logo_light.png")),
                                       light_image=Image.open(path.join(image_path,"p_logo_dark.png")),
                                       size=(70,100))
        
        # give the text document creator
        self.logo_label = CTkLabel(self.logo_frame, text=" Document Creator", image=self.logo_img, compound="left",
                                    font=CTkFont(size=25, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20, 20), pady=(10, 10))


        self.enrollment_num = CTkLabel(self.main_frame, text="Enrollment Number :",font=self.default_font)
        self.enrollment_num.grid(row=0, column=0, sticky="nse", padx = 30, pady=(15,15))

        #enrollment number entry
        self.en_num_text = CTkEntry(self.main_frame,width=160)
        self.en_num_text.grid(row=0, column=1,columnspan=1, sticky="nse", padx=(0,10),pady=(15,15))

        self.en_num_text.insert(0,"ET22BTCO")
        #teb frame that contain other item
        self.tab_frame = CTkTabview(self, width=250, height=640,anchor="ne")
        self.tab_frame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")

        #define 2 tab 
        self.tab_frame.add("Import Files")
        self.tab_frame.add("Paste Code")
        self.tab_frame.tab("Import Files").grid_columnconfigure(0, weight=1)#add the grid configuration 
        self.tab_frame.tab("Paste Code").grid_columnconfigure(0, weight=1)

        self.button_main_menu("Paste Code")
        self.button_main_menu("Import Files")

        self.daa_c = None
        self.button(self.daa_c,self.daa_import_c,"DAA","Import Files",self.c_logo_img,0,1)
        self.button(self.daa_c,self.daa_code_c,"DAA","Paste Code",self.c_logo_img,0,1)
        
        self.daa_j = None
        self.button(self.daa_j,self.daa_import_j,"DAA","Import Files",self.j_logo_img,0,2)
        self.button(self.daa_j,self.daa_code_j,"DAA","Paste Code",self.j_logo_img,0,2)
        
        self.daa_p = None
        self.button(self.daa_p,self.daa_import_p,"DAA","Import Files",self.p_logo_img,0,3)
        self.button(self.daa_p,self.daa_code_p,"DAA","Paste Code",self.p_logo_img,0,3)

        self.cn_j = None
        self.button(self.cn_j,self.cn_import_j,"CN","Import Files",self.j_logo_img,0,4)
        self.button(self.cn_j,self.cn_code_j,"CN","Paste Code",self.j_logo_img,0,4)

        self.cn_p = None
        self.button(self.cn_p,self.cn_import_p,"CN","Import Files",self.p_logo_img,0,5)
        self.button(self.cn_p,self.cn_code_p,"CN","Paste Code",self.p_logo_img,0,5)

        #side fram for other item's
        self.side_frame = CTkFrame(self, width=450, height=100)
        self.side_frame.grid(row=2, column=0, padx=5, pady=(5, 5), sticky="sew")

        #all button's
        self.appearance_mode_label = CTkLabel(self.side_frame, text="Appearance Mode", anchor="w")
        self.appearance_mode_label.grid(row=12, column=0, padx=5, pady=(5, 0))

        self.appearance_mode_optionemenu = CTkOptionMenu(self.side_frame,values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event,)
        self.appearance_mode_optionemenu.grid(row=13, column=0, padx=20, pady=(10, 10))
        
        self.help = CTkButton(self.side_frame, text="Help", command=self.help)
        self.help.grid(row=13, column=1,padx=20, sticky="ns", pady=10)
        
        self.name = CTkLabel(self.side_frame,text="Create By RUHAAN",anchor="w")
        self.name.grid(row=12,column=1,padx=5,pady=(5,0))

        # default values
        self.appearance_mode_optionemenu.set("System")
    def button_main_menu(self, tab):
        self.tab_frame.tab(f"{tab}").rowconfigure(0, weight=0)
        self.tab_frame.tab(f"{tab}").columnconfigure(0, weight=1)
        self.tab_frame.tab(f"{tab}").columnconfigure(1, weight=1)
        self.tab_frame.tab(f"{tab}").columnconfigure(2, weight=1)
        self.tab_frame.tab(f"{tab}").columnconfigure(3,weight=1)
        self.tab_frame.tab(f"{tab}").columnconfigure(4,weight=1)
        self.tab_frame.tab(f"{tab}").columnconfigure(5,weight=1)

    def button(self,name,command,ADD,tab,photo,i,j):
        name = CTkButton(self.tab_frame.tab(f"{tab}"), text=f"{ADD}",
                                            image=photo,compound="top",anchor="nsew", 
                                            command=command, width=50, height=90,bg_color="transparent",
                                            fg_color="transparent",hover=False,text_color=("black","white"),
                                            font=self.default_font)
        name.grid(row=i, column=j, padx=(0, 25), pady=(40, 5), ipadx=5)  
    # all functions
    def button_event(self):
        messagebox.showinfo("Help !","Under Devlopment")
    def help(self):
        class help(CTk):
            def __init__(self):
                super().__init__()

                # size fixing center of the screen
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()

                window_width = 900
                window_height = 700

                x_position = (screen_width - window_width) // 2
                y_position = (screen_height - window_height) // 2

                self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
                self.default_font = CTkFont(size=15)
                # title of application
                self.title("Help!")
                
                self.temp_list = [path.join(path.dirname(path.realpath(__file__)),'help.txt')]
                # stopping the resizing of the application
                self.resizable(False, False)

                self.help_area = CTkLabel(self,font=self.default_font, justify="left")
                self.help_area.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

                with open (self.temp_list[0] , 'r') as f:
                    help_text = f.read()
                    self.help_area.configure(text=help_text,anchor="w")
        
        help_ins = help()
        help_ins.mainloop()

                
    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

    def daa_import_c(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.import_frame("- DAA","(.c)",self.call_c_open,lambda:C_run(self.list_open,self.counter_index),self.daa_submit)

    def daa_import_j(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.import_frame("- DAA","(.java)",self.call_java_open,lambda:run_File(self.list_open,self.counter_index,"java"),self.daa_submit)

    def daa_import_p(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.import_frame("- DAA","(.py)",self.call_python_open,lambda:run_File(self.list_open,self.counter_index,"python"),self.daa_submit)

    def cn_import_j(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.import_frame("- CN","(.java)",self.call_java_open,lambda:run_File(self.list_open,self.counter_index,"java"),self.cn_submit)

    def cn_import_p(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.import_frame("- CN","(.py)",self.call_python_open,lambda:run_File(self.list_open,self.counter_index,"python"),self.cn_submit)

    def import_frame(self,t_name,code_name,import_file,run_file,submit_button):
        self.frame = CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.title_frame = CTkFrame(self.frame)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.home_button = CTkButton(self.title_frame, text="Home", command=self.back_to_main_screen,width=10)
        self.home_button.grid(row=0, column=0, padx=10, pady=5)

        self.titel_label = CTkLabel(self.title_frame, text=f"Import Files{t_name}", font=self.sp_font)
        self.titel_label.grid(row=0, column=1, padx=200,columnspan=1, pady=5)

        self.content_frame = CTkFrame(self.frame)
        self.content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.q_text = CTkLabel(self.content_frame,text="Paste your Question",font=self.default_font)
        self.q_text.grid(row=1, column=0, padx=10, pady=10,sticky="nw")

        self.q_area = CTkTextbox(self.content_frame, width=550,height=100)
        self.q_area.grid(row=1, column=0,columnspan=2, padx=10, pady=10, sticky="nse")

        self.text_frame = CTkFrame(self.content_frame)
        self.text_frame.grid(row=2,column=0,padx=10,pady=10)
        
        self.text_frame.grid_columnconfigure(0,weight=1)

        self.button_frame = CTkFrame(self.content_frame)
        self.button_frame.grid(row=2,column=1,padx=10,pady=10,sticky="e")

        self.prac_text = CTkLabel(self.text_frame, text="Practical Number", font=self.default_font)
        self.prac_text.grid(row=2, column=0, padx=70, pady=10,sticky="nw")

        self.prac_select = CTkComboBox(self.button_frame, values=["0","1", "2", "3", "4", "5"])
        self.prac_select.grid(row=2, column=1, padx=100, pady=10)

        self.c_file_label = CTkLabel(self.text_frame, text="Import Your Code File", font=self.default_font)
        self.c_file_label.grid(row=3, column=0, padx=70, pady=10,sticky="nw")

        self.c_file_import = CTkButton(self.button_frame, text=f"Import {code_name} File", command=import_file)
        self.c_file_import.grid(row=3, column=1, padx=90, pady=10)

        self.run_code_text = CTkLabel(self.text_frame, text="Click Button to Run Code", font=self.default_font)
        self.run_code_text.grid(row=4, column=0, padx=70, pady=10,sticky="nw")

        self.run_code = CTkButton(self.button_frame, text="Run Code", command=run_file)
        self.run_code.grid(row=4, column=1, padx=90, pady=10)

        self.snap_screen_text = CTkLabel(self.text_frame, text="Take Snapshot your Output", font=self.default_font)
        self.snap_screen_text.grid(row=5,column=0,padx=70,pady=10,sticky="nw")
        
        self.snap_screen = CTkButton(self.button_frame,text="Snap ScreenShot",command=self.call_snap_shot)
        self.snap_screen.grid(row=5,column=1,padx=90,pady=10)
        
        self.info = CTkLabel(self.content_frame,text=f"Import Files for {self.counter_index} Pactical",font=self.default_font)
        self.info.grid(row=8,column=0,padx=10,pady=10,sticky="w")
        
        self.button_frame_title = CTkFrame(self.title_frame)
        self.button_frame_title.grid(row=0, column=1,columnspan=2, padx=0, pady=10,sticky="e")

        self.next_button_dsa = CTkButton(self.button_frame_title, text="Next", command=self.next_page_code,width=10)
        self.next_button_dsa.grid(row=0, column=1,columnspan=2, padx=0, pady=0,sticky="w")
        
        self.reset_button = CTkButton(self.title_frame,text="Reset",command=self.reset_import,width=20)
        self.reset_button.grid(row=0,column=1,padx=(10,50),pady=10,sticky="e")

        self.location_button = CTkButton(self.content_frame,text="Location for Output",command=self.output_location)
        self.location_button.grid(row=8,column=1,padx=(40,130),pady=(10,10))

        self.submit_button = CTkButton(self.content_frame,text="Submit",command=submit_button)
        self.submit_button.grid(row=8,column=1,columnspan=1,padx=10,pady=10, sticky="e")


    def daa_code_c(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.paste_frame(" -DAA",self.daa_submit_text)

    def daa_code_j(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.paste_frame(" -DAA",self.daa_submit_text)

    def daa_code_p(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.paste_frame(" -DAA",self.daa_submit_text)

    def cn_code_j(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.paste_frame(" -CN",self.daa_submit_text)

    def cn_code_p(self):
        roll_no = self.en_num_text.get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter the Enrollment Number.")
            return
        if roll_no == "ET22BTCO":
            messagebox.showerror("Error", "Please Complete the Enrollment Number.")
        else:
            for widget in self.winfo_children():
                widget.grid_remove()
            self.paste_frame(" -CN",self.daa_submit_text)

    def paste_frame(self,t_name,submit_button):
        self.frame = CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.title_frame = CTkFrame(self.frame)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.home_button = CTkButton(self.title_frame, text="Home", command=self.back_to_main_screen,width=10)
        self.home_button.grid(row=0, column=0, padx=10, pady=5)

        self.titel_label = CTkLabel(self.title_frame, text=f"Import Files{t_name}", font=self.sp_font)
        self.titel_label.grid(row=0, column=1, padx=200,columnspan=1, pady=5)

        self.content_frame = CTkFrame(self.frame)
        self.content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.text_frame = CTkFrame(self.content_frame)
        self.text_frame.grid(row=1,column=0,padx=10,pady=10)

        self.text_frame_2 = CTkFrame(self.content_frame)
        self.text_frame_2.grid(row=1, column=1, padx=10, pady=10)

        self.prac_text = CTkLabel(self.text_frame, text="Practical Number", font=self.default_font)
        self.prac_text.grid(row=0, column=0, padx=10, pady=10)

        self.prac_select = CTkComboBox(self.text_frame, values=["0","1", "2", "3", "4", "5"])
        self.prac_select.grid(row=1, column=0, padx=10, pady=10)
        
        self.q_text = CTkLabel(self.text_frame,text="Paste your Question",font=self.default_font)
        self.q_text.grid(row=2, column=0, padx=10, pady=10)

        self.q_area = CTkTextbox(self.text_frame, width=400)
        self.q_area.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.code_text = CTkLabel(self.text_frame_2,text="Paste your Code",font=self.default_font)
        self.code_text.grid(row=1,column=0,padx=10,pady=10)

        self.code_area = CTkTextbox(self.text_frame_2,width=350,wrap="none")
        self.code_area.grid(row=2,column=0,padx=10,pady=10,sticky="nsew")

        self.image_text = CTkLabel(self.text_frame_2,text="Import your Output image",font=self.default_font)
        self.image_text.grid(row=3,column=0,padx=10,pady=10)

        self.image_button = CTkButton(self.text_frame_2,text="Import Iamge",command=self.call_img_open)
        self.image_button.grid(row=4,column=0,padx=10,pady=10)

        self.info = CTkLabel(self.content_frame,text=f"Import Files for {self.counter_index} Pactical",font=self.default_font)
        self.info.grid(row=8,column=0,padx=10,pady=10,sticky="w")
        
        self.next_button_dsa = CTkButton(self.title_frame, text="Next", command=self.next_page_text,width=10)
        self.next_button_dsa.grid(row=0, column=1,columnspan=2, padx=0, pady=10,sticky="e")

        self.location_button = CTkButton(self.content_frame,text="Location for Output",command=self.output_location)
        self.location_button.grid(row=8,column=1,padx=(0,110),pady=(10,10))

        self.reset_button = CTkButton(self.title_frame,text="Reset",command=self.reset_text,width=20)
        self.reset_button.grid(row=0,column=1,padx=(10,50),pady=10,sticky="e")

        self.submit_button = CTkButton(self.content_frame,text="Submit",command=submit_button)
        self.submit_button.grid(row=8,column=1,columnspan=1,padx=10,pady=10, sticky="e")
        
    def reset_text(self):
        self.list_open.clear()
        self.list_code_text.clear()
        self.list_prob_text.clear()
        self.location_file = ""
        self.counter_index = 1
        self.prac_select.set("0")
        self.code_area.delete("0.0","end")
        self.q_area.delete("0.0","end")
        self.info.configure(text=f"Import Files for {self.counter_index} Practical")
        clear_database()

    def reset_import(self):
        self.list_open.clear()
        self.list_code_text.clear()
        self.list_prob_text.clear()
        self.location_file = ""
        self.counter_index = 1
        self.prac_select.set("0")
        self.q_area.delete("0.0","end")
        self.info.configure(text=f"Import Files for {self.counter_index} Practical")
        clear_database()

    def back_to_main_screen(self):
        self.list_open.clear()
        self.list_code_text.clear()
        self.list_prob_text.clear()
        self.location_file = ""
        self.home_button.grid_remove()
        self.frame.grid_remove()
        self.counter_index = 1 
        self.main_frame.grid()
        self.tab_frame.grid()
        self.side_frame.grid()
        clear_database()


    def next_page_code(self):
        amount_prac = self.prac_select.get()
        try:
            amount_prac = int(amount_prac)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid integer, not a string")
            return
        
        if amount_prac <= 0:
            messagebox.showerror("Error", "Enter a positive integer greater than zero")
            return
        if self.counter_index == amount_prac:
            messagebox.showinfo("Success", "The file selection is completed")
        else:
            self.counter_index += 1
            problem = self.q_area.get("0.0","end")
            self.list_prob_text.insert(self.counter_index,f"{problem}")
            self.q_area.delete("0.0","end")
            self.info.configure(text=f"Import Files for {self.counter_index} Practical")
    
    def next_page_text(self):
        amount_prac = self.prac_select.get()
        try:
            amount_prac = int(amount_prac)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid integer, not a string")
            return
        if amount_prac <= 0:
            messagebox.showerror("Error", "Enter a positive integer greater than zero")
        if self.counter_index == amount_prac:
            messagebox.showinfo("Success", "The file selection is completed")
        else:
            self.counter_index += 1
            code = self.code_area.get("0.0","end")
            problem = self.q_area.get("0.0","end")
            self.list_code_text.append(f"{code}")
            self.list_prob_text.append(f"{problem}")
            self.code_area.delete("0.0","end")
            self.q_area.delete("0.0","end")
            self.info.configure(text=f"Import Files for {self.counter_index} Practical")

    def call_c_open(self):
        if self.prac_select.get() == "0":
            messagebox.showerror("Error","Please Select the Practical numbers")
        else:
            With_open(self.list_open,"C ",".c",self.counter_index)

    def call_java_open(self):
        if self.prac_select.get() == "0":
            messagebox.showerror("Error","Please Select the Practical numbers")
        else:
            With_open(self.list_open,"Java ",".java",self.counter_index)
        

    def call_python_open(self):
        if self.prac_select.get() == "0":
            messagebox.showerror("Error","Please Select the Practical numbers")
        else:
            With_open(self.list_open,"Python ",".py",self.counter_index)

    def call_img_open(self):
        if self.prac_select.get() == "0":
            messagebox.showerror("Error","Please Select the Practical numbers")
        else:
            With_open(self.list_open,"Image ",".png",self.counter_index)

    def daa_submit(self):
        if self.location_file == "":
            messagebox.showerror("Error","Select the File location \n where we store the Documnet")

        elif int(self.prac_select.get()) == self.counter_index:
            problem = self.q_area.get("0.0","end")
            self.list_prob_text.insert(self.counter_index,f"{problem}")
            self.q_area.delete("0.0","end")
            doc_dsa = Document_File(self.list_open,self.list_prob_text,self.prac_select.get(),self.counter_index,"",
                                    self.en_num_text.get(),"DAA","DAA",file_location=self.location_file,list_img=self.image_list)
            doc_dsa.docx_file() 
        else:
            messagebox.showerror("Error","Please Select the all of practicals file \n aka use `Next button` ")

    def cn_submit(self):
        if self.location_file == "":
            messagebox.showerror("Error","Select the File location \n where we store the Documnet")

        elif int(self.prac_select.get()) == self.counter_index:
            problem = self.q_area.get("0.0","end")
            self.list_prob_text.insert(self.counter_index,f"{problem}")
            self.q_area.delete("0.0","end")
            doc_dsa = Document_File(self.list_open,self.list_prob_text,self.prac_select.get(),self.counter_index,"",
                                    self.en_num_text.get(),"CN","CN",file_location=self.location_file,list_img=self.image_list)
            doc_dsa.docx_file() 
        else:
            messagebox.showerror("Error","Please Select the all of practicals file \n aka use `Next button` ")

    def daa_submit_text(self):
        if self.location_file == "":
            messagebox.showerror("Error","Select the File location \n where we store the Documnet")

        elif int(self.prac_select.get()) == self.counter_index:
            code = self.code_area.get("0.0","end")
            problem = self.q_area.get("0.0","end")
            self.list_code_text.append(f"{code}")
            self.list_prob_text.append(f"{problem}")
            self.code_area.delete("0.0","end")
            self.q_area.delete("0.0","end")
            doc_oop = Document_File_text(code=self.list_code_text,list2=self.list_prob_text,
                                        image_list=self.list_open,practical_num=self.prac_select.get(),
                                        crr_page=self.counter_index,code_sub="DAA",
                                        enrollment_num=self.en_num_text.get(),sub_name="DAA",
                                        sub_name_small="DAA",file_location=self.location_file)
            doc_oop.docx_file()
        else:
            messagebox.showerror("Error","Please Select the all of practicals file \n aka use `Next button` ")

    def cn_submit_text(self):
        if self.location_file == "":
            messagebox.showerror("Error","Select the File location \n where we store the Documnet")

        elif int(self.prac_select.get()) == self.counter_index:
            code = self.code_area.get("0.0","end")
            problem = self.q_area.get("0.0","end")
            self.list_code_text.append(f"{code}")
            self.list_prob_text.append(f"{problem}")
            self.code_area.delete("0.0","end")
            self.q_area.delete("0.0","end")
            doc_oop = Document_File_text(code=self.list_code_text,list2=self.list_prob_text,
                                        image_list=self.list_open,practical_num=self.prac_select.get(),
                                        crr_page=self.counter_index,code_sub="CN",
                                        enrollment_num=self.en_num_text.get(),sub_name="CN",
                                        sub_name_small="CN",file_location=self.location_file)
            doc_oop.docx_file()
        else:
            messagebox.showerror("Error","Please Select the all of practicals file \n aka use `Next button` ")

    def output_location(self):
        self.location_file = location_folder(self.location_file)

    def call_snap_shot(self):
        if self.prac_select.get() == "0":
            messagebox.showerror("Error","Please Select the Practical numbers")
        else:
            self.iconify()
            index = self.counter_index
            snap(index)
            self.deiconify()
            self.image_list = retrieve_images()
if __name__ == "__main__":
    app = App()
    app.mainloop()

