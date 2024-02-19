from tkinter import messagebox
from os import path,chdir,system

def run_File(pro_list,current_page,p_name):

    if 0 <= current_page - 1 < len(pro_list):
        if not pro_list:
            messagebox.showerror("Error", f"No {p_name} File Selected for {current_page}")
            return

        crr_dic = pro_list[current_page - 1]

        try:
            python_directory = path.dirname(crr_dic)
            chdir(python_directory)

            system(f'start cmd /k {p_name} "{crr_dic}"')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", f"No {p_name} File Selected for {current_page}")