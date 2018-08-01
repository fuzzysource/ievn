import os, sys
import pyautogui
import time

cwd = os.getcwd()
os.listdir(cwd)

def output_folder():
    return os.path.join(os.getcwd(),"DWG-R14\SDO")

def is_dxf(file_name):
    ext = os.path.splitext(file_name)[1]
    if ext.lower() == ".dxf":
        return True
    else:
        return False

def dxf_files (dir):
    file_list = os.listdir(dir)
    return filter(is_dxf, file_list)

def point_to_windows():
    pyautogui.alert("Move the cursor to the PSSE window in 5s")
    time.sleep(3)

def rename_output(file_name):
    output_file = os.path.join(output_folder(), "TO_PSS.RAW")
    new_file = os.path.join(output_folder(), file_name + ".RAW")
    os.rename(output_file, new_file)

def replace_character(file_name):
    raw_file = os.path.join(output_folder(), file_name + ".RAW")
    f = open(raw_file, "r")
    content = f.read().replace("#", "\'")
    f.close()
    f = open(raw_file, "w")
    f.write(content)
    f.close()

def run_psse_exe(dxf):
    file_name = os.path.splitext(dxf)[0]
    pyautogui.typewrite("psse")
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.typewrite(file_name)
    pyautogui.press("enter")
    time.sleep(5)
    rename_output(file_name)
    replace_character(file_name)
    pyautogui.press("enter")

def run_all(working_dir):
    file_names = dxf_files(working_dir)
    point_to_windows()
    for dxf in file_names:
        run_psse_exe(dxf)

run_all(os.getcwd())
