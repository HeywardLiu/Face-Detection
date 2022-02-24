import datetime
import sqlite3
import pandas as pd  
from matplotlib.pyplot import table
from numpy import rad2deg

COURSE_NAME = "database/" + "Physics"
COURSE_DATE = datetime.datetime.today().strftime("%Y_%m_%d")


# format id, date 
def format_id(id):
    if(len(str(id))<7):
        prefix = "0" * (7 - len(str(id)))
        result = prefix + str(id)
        return result
    else:
        return str(id)


def format_date(course_date: datetime):
    return course_date.strftime("%Y_%m_%d")


# for database 
def delete_table(database_name, table_name):
    willing = input("Do you really want to delete %s table in %s ? (Y/N): "%(database_name,table_name))
    if(willing == 'Y'):
        connector = sqlite3.connect(database_name)
        cursor = connector.cursor()
        cursor.execute("""DROP TABLE {}""".format(table_name))
        print("  [Success]: %s has been deleted permanently."%table_name)


def append_col(database_name, table_name, col_name):
    try:
        connector = sqlite3.connect(database_name)
        cursor = connector.cursor()    
        cursor.execute("""ALTER TABLE {} ADD {} VARCHAR""".format(table_name, col_name))
        print_table(database_name, table_name)
        connector.commit()
        connector.close()

    except sqlite3.OperationalError:
        # print("%s already exists" %col_name)
        pass
    


def print_table(database_name, table_name):
    try:
        connector = sqlite3.connect(database_name)
        cursor = connector.cursor()
        table = pd.read_sql_query("""SELECT * FROM {} ORDER BY id """.format(table_name), connector)
        print(table)

        # cursor.execute("""SELECT * FROM {}""".format(table_name))
        # print(cursor.fetchall())
        # connector.commit()

    except sqlite3.OperationalError:
        pass
        print("table: %s was NOT founded in %s"%(table_name,database_name))





#  encapsulation of function ###
def create_members_list(course_name):   # Create a membership table of the course
    connector = sqlite3.connect(course_name) 
    cursor = connector.cursor()
    table_name = "members_list"
    query = """ CREATE TABLE IF NOT EXISTS {} ( 
                    id         TEXT NOT NULL UNIQUE,
                    first_name TEXT,
                    last_name  TEXT
                )""" 
    
    cursor.execute(query.format(table_name))   # Create a table for the course
    connector.commit()
    connector.close()


def append_to_member_list(course_name, first_name, last_name, id):   # append a member into list of course's membership
    try:
        table = "members_list"

        create_members_list(course_name)
        connector = sqlite3.connect(course_name)
        cursor = connector.cursor()
        query = """ INSERT INTO {} (id, first_name, last_name)
                    VALUES (        :id, 
                            :first_name,
                             :last_name
                ) """
        cursor.execute(query.format(table), {        'id': id, 
                                             'first_name': first_name, 
                                              'last_name': last_name
                                            })
        connector.commit()
        connector.close
    except sqlite3.IntegrityError:     # insert duplicate value of UNIQUE KEY will assert an exception
        pass
        # print("%s, you've registered already!"%id)

    except:
        exit("[Exception]: database.py, append_to_member_list, line 89")


def search_studentes(course_name, id):
    connector = sqlite3.connect(course_name)
    cursor = connector.cursor()
    table_name = "members_list"
    query = """ SELECT *
                  FROM {} 
                 WHERE id=:id
            """
    cursor.execute(query.format(table_name), {'id': str(id)})
    student_info = cursor.fetchone()
    connector.commit()
    connector.close()
    return student_info


def is_member(course_name, id):
    if(search_studentes(course_name, id) == None):
        return False
    else:
        return True



#  for roll call of the course ###
def roll_call(course_name, course_date, id):
    if (is_member(course_name, id) == False):
        print("  [Warning]: %s is not the member of this course!"%id)     # make sure the student is the member of this course.
        return

    table_name = "members_list"
    col_name = "__" + course_date
    append_col(course_name, table_name, col_name)  
    
    connector = sqlite3.connect(course_name)
    cursor = connector.cursor()
    try:
        query = """ UPDATE {}
                       SET %s = (?)
                     WHERE id = (?) """.format(table_name) %(col_name)
        cursor.execute(query , ("V", id))  # update the status of appended column 
        connector.commit()                                                           
        connector.close()
        # print("  [Success]: Take a roll call successfully, %s "%id)
        
    except sqlite3.IntegrityError:     # insert duplicate value of UNIQUE KEY will assert an exception
        pass
        # print("%s, you've taken a roll call already!"%id)

    except:
        exit("[Exception]: database.py, roll_call, line 139.")


def print_roll_call_talbe(course_name):
    table_name = "members_list"
    print_table(course_name, table_name)




if __name__ == "__main__":
    print(COURSE_NAME)
    print_roll_call_talbe(COURSE_NAME)