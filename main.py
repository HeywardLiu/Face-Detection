import collect_samples
import detector
import trainer
import database
from database import COURSE_NAME, COURSE_DATE



def main():
    reg = str(input("have you registered yet? (Y/N): "))
    if(reg == "N"):
        collect_samples.collect_samples(COURSE_NAME)
        trainer.train_data_set()

    database.print_roll_call_talbe(COURSE_NAME)
    print("\n-------------------")
    print("Press Q to exit")
    print("-------------------\n")
    detector.detector(COURSE_NAME, COURSE_DATE)
    database.print_roll_call_talbe(COURSE_NAME)


if __name__ == "__main__":
    main()
