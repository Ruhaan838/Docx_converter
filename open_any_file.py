from tkinter import filedialog,messagebox

def With_open(Input_open1,name_file,dot_extention,counter):
        input = filedialog.askopenfilename(
            title="Select a file",
            initialdir="/home/user",
            filetypes=[(f"{name_file}files", f"*{dot_extention}")]
        )
        Input_open1.insert(counter,input) 
        messagebox.showinfo("Success !",f"The File Import Successfully from \n {Input_open1[counter-1]}")