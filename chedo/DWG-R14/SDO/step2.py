import os, sys

def read_raw(raw_file):
    print("Read file: " + raw_file)
    NUMNAM = 0
    ierr = psspy.read(NUMNAM, raw_file)
    if ierr <> 0:
        print("Invalid raw file")
    return ierr

def check_island(raw_file):
    print("Check island")
    ierr, buses = psspy.tree(1)
    if ierr <> 0:
        print(raw_file + " contains islands")
    return ierr

def run_fd(raw_file):
    print("Run FD")
    ierr = psspy.fdns()
    return ierr

def run_fn(raw_file):
    print("Run FN")
    ierr = psspy.fnsl()
    return ierr

def report_setup(file_name):
    ISLCT = 2 # psse option to output to file
    psspy.report_output(ISLCT, file_name)

def post_report(file_name):
    f = open(file_name, "r")
    lines = f.read().split("\n")
    data = ""
    for line in lines:
        data = data + line[1:] + "\n" # remove the first space at each line
    f.close()
    f = open(file_name, "w")
    f.write(data)
    f.close()

def run_pout_all(raw_file):
    print("Run pout all")
    file_name = os.path.splitext(raw_file)[0] + ".nod"
    report_setup(file_name)
    ierr = psspy.pout()
    psspy.close_report()
    post_report(file_name)
    return ierr

def run_area(raw_file):
    print("Run area")
    file_name = os.path.splitext(raw_file)[0] + ".are"
    report_setup(file_name)
    ierr = psspy.area()
    psspy.close_report()
    post_report(file_name)
    return ierr

def is_raw(file_name):
    ext = os.path.splitext(file_name)[1]
    if ext.lower() == ".raw":
        return True
    else:
        return False

def list_raw_files(dir):
    file_list = os.listdir(dir)
    return filter(is_raw, file_list)

STEPS = [read_raw, check_island, run_fd, run_fn, run_pout_all, run_area]

def process_raw_file(raw_file):
    err = 0
    for step in STEPS:
        err = step(raw_file)
        if err <> 0:
            break
    if err == 0:
        print("Successfully process " + raw_file)
    return err

def run_all():
    raw_files = list_raw_files(os.getcwd())
    err = 0
    for f in raw_files:
        err = process_raw_file(f)
        if err <> 0:
            print("Check file " + f)
            break

run_all()
