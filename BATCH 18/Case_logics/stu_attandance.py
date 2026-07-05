from Student_details import student_information
from Decorator import decorate

present = []
absent = []
attand_complete = "no"


def attandance():
    global attand_complete
    decorate.space()
    print("Enter P for Present and A for Absent:: ")
    decorate.space()
    decorate.hyphen50()
    for student in student_information.total_students:
        while True:
            status = input(f"{student}: ").upper()
            if status == "P":
                present.append(student)
                break
            elif status == "A":
                absent.append(student)
                break
            else:
                print("Oops! Wrong input. Use only P (Present) or A (Absent).")
    attand_complete = "yes"           
    decorate.hyphen50() 
    decorate.space()



def attandance_report():
    decorate.equal25()
    print(" ATTENDANCE REPORT".center(25)) 
    decorate.equal25()
    print(f"Present Students :  {len(present)}".center(25))
    print(f"Absent Students  :  {len(absent)}".center(25))
    decorate.hyphen25()
    print(f"Total Students   :  {len(present)+len(absent)}".center(25))
    decorate.hyphen25()
  


def absent_list():    
    decorate.hyphen25()
    print("ABSENT LIST".center(25))
    decorate.hyphen25()
    for i in range(len(absent)):
        print(f"{i+1}. {absent[i]}")
