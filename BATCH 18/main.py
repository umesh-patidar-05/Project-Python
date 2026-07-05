from Decorator import decorate
from Date_Time import date
from Case_logics import stu_attandance, get_information

def main():

    decorate.equal50()
    print("INFOBEANS BATCH 18 MANAGER".center(50))    
    decorate.equal50()
    
    decorate.space()
    decorate.space()
    print(f"Today is {date.today()} and only {date.days_left()} days are left.")
    decorate.space()

    decorate.hyphen50()
    print("1. Attendance")
    print("2. Attendance Report")
    print("3. Absent Students List")
    print("4. Student Information")
    decorate.hyphen50()


    
    while True:
        
        choice = input("Enter your choice: ")
        match choice:

            case "1":
                if stu_attandance.attand_complete == "no":
                    stu_attandance.attandance()     
                else:
                    print("Attendance already completed. You cannot mark it again.")    
            
            case "2":
                if stu_attandance.attand_complete=="yes":
                    stu_attandance.attandance_report()
                else:
                    print("Please complete the attendance first.")    

            case "3":
                if stu_attandance.attand_complete=="yes":
                    stu_attandance.absent_list()
                else:
                    print("Please complete the attendance first.")            
    
            case "4":
                get_information.details()

            case _:
                print("invalid")

main()
