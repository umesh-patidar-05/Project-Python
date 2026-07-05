from Student_details import student_information
from Decorator import decorate

def details():
    stu_name = input("Enter the student name: ").title()
    decorate.space()
    if stu_name in student_information.students_details:
        decorate.equal25()
        print("STUDENT DETAILS".center(25))
        decorate.equal25()
        print(f"  {"Name".ljust(7)}   : {stu_name}")
        decorate.hyphen25()
        for k,v in student_information.students_details[stu_name].items():
            print(f"  {k.capitalize().ljust(7)}   : {v}")
        decorate.hyphen25()

    else:
        print("who are you")