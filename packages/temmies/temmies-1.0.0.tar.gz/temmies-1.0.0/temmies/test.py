from themis import Themis
from os import listdir


def main():
    # Debug
    themis = Themis("s5230837", "B0bit0Dr0g@23!")
    year = themis.get_year(2023, 2024)

    # # Ads
    # ads = year.get_course("Algorithms and Data Structures for CS")
    # ads_as = ads.get_group("Lab Assignments")

    # trains = ads_as.get_group("5. Trains - An Adventure-Drama")
    # trains_one = trains.get_group("Trains: An Adventure-Drama")

    # # Get status
    # status = trains_one.get_status()

    # # Get leading submission
    # leading =  status["leading"]
    # print(leading.files())

    # PF
    pf = year.get_course("Programming Fundamentals (for CS)")
    pf_as = pf.get_group("Lab Session 2")
    
    # Get overall status
    # status = pf_as.get_all_statuses()
    # print(status)
    
    # Get exercise
    exercise = pf_as.get_group("Recurrence")
    
    # Get status
    status = exercise.get_status()[1]["leading"]
    print(status.files())
    # Get leading submission
    # leading =  status["leading"]
    # print(leading.test_cases())
    # print(leading.files())
    
if __name__ == "__main__":
    main()
