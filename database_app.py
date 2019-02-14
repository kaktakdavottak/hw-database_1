import psycopg2
from psycopg2.extensions import AsIs


DATABASE = 'mydb'
USER = 'semen'


# создает таблицы
def create_db(database_name=DATABASE, user_name=USER):
    with psycopg2.connect('dbname=%s user=%s' % (database_name, user_name)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("""CREATE TABLE student (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL,
                gpa numeric(10,2),
                birth timestamp with time zone);
                """)
            curs.execute("""CREATE TABLE course (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL);
                """)
            curs.execute("""CREATE TABLE student_course (
                id serial PRIMARY KEY NOT NULL,
                student_id INTEGER REFERENCES student(id),
                course_id INTEGER REFERENCES course(id));
                """)

# возвращает студентов определенного курса
def get_students(course_id):
    pass


# создает студентов и
# записывает их на курс
def add_students(course_id, students):
    pass


# просто создает студента
def add_student(student):
    columns = student.keys()
    values = [student[column] for column in columns]
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            insert_statement = 'insert into student (%s) values %s'
            curs.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            curs.execute(curs.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))
    print(f'В базу данных {DATABASE} добавлен курс {student["name"]}')


def add_course(course):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("insert into course (name) values (%s)",
                         (course,))
    print(f'В базу данных {DATABASE} добавлен курс {course}')


def get_student(student_id):
    pass


if __name__ == '__main__':
    # create_db()
    # add_course('Python')
    # add_course('PHP')
    student_1 = {
        'name': 'Semen Mineev',
        'gpa': 10.2
    }
    add_student(student_1)
    # print(tuple(student_1.keys()))
    # print(r"bla bla %S" % tuple(student_1.keys()))
