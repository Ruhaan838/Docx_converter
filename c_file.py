from tkinter import messagebox
from os import path,chdir,system
def C_run(c, current_page):
    if 0 <= current_page - 1 < len(c):
        if not c:
            messagebox.showerror("Error", f"No C File Selected for {current_page}")
            return
        c_file = c[current_page-1]
        try:
            c_directory = path.dirname(c_file)
            chdir(c_directory)
            compilation_cmd = f'gcc "{c_file}" -o my_program'
            compilation_result = system(compilation_cmd)
            if compilation_result == 0:
                system('start cmd /k my_program')
            else:
                messagebox.showerror("Compilation Error", "There was an error during compilation.")
        except Exception as e:
            messagebox.showerror("Error",f"Error running C program:{str(e)}")
    else:
        messagebox.showerror("Error", f"No C File Selected for {current_page}")
