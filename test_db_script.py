import datetime
import database
from faker import Faker  # for testing
import random            # for testing

### for testing ###
def test_database(course_name):
    table_name = 'members_list'
    course_date = datetime.date(2021, 9, 10)
    database.create_members_list(course_name)
    fake = Faker('zh_TW')
    Name_ID = {}
    for i in range(10):
        id = database.format_id(random.randint(0, 9999999))
        name = [fake.first_name(), fake.last_name()]
        Name_ID[id] = name
        database.append_to_member_list(course_name, Name_ID[id][0], Name_ID[id][1], id)

    print(Name_ID)
    database.print_roll_call_talbe(course_name)
    for i in range(20):
        course_date = course_date + datetime.timedelta(7)
        print(course_date)
        for j in range(random.randint(0, 9)):
            database.roll_call(course_name, database.format_date(course_date), random.choice(list(Name_ID.keys())))
            if(j%2):
                database.roll_call(course_name, database.format_date(course_date), database.format_id(random.randint(0, 9999999)))


if __name__ == "__main__":
    test_database("database/Calculus")