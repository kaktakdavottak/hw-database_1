import psycopg2
from psycopg2.extensions import AsIs


DATABASE = 'mydb'
USER = 'semen'


# создает таблицы
def create_db(database_name=DATABASE, user_name=USER):
    with psycopg2.connect('dbname=%s user=%s' % (database_name, user_name)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS student (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL,
                gpa numeric(10,2),
                birth timestamp with time zone);
                """)
            curs.execute("""
                CREATE TABLE IF NOT EXISTS course (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL);
                """)
            curs.execute("""
                CREATE TABLE IF NOT EXISTS student_course (
                id serial PRIMARY KEY NOT NULL,
                student_id INTEGER REFERENCES student(id) ON DELETE CASCADE,
                course_id INTEGER REFERENCES course(id) ON DELETE CASCADE);
                """)


# возвращает студентов определенного курса
def get_students(course_id):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("""select student.name, course.id from student
                join student_course on student_course.student_id = student.id
                join course on course_id = course.id
                where course_id = %s
                """, (course_id,))
            return curs.fetchall()


# создает студентов и
# записывает их на курс
def add_students(course_id, students):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("select * from course where course.id = %s",
                         (course_id,))
            contains_id = curs.fetchone()
    if contains_id is not None:
        with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
                as conn:
            for student in students:
                st_id = add_student(student)
                with conn.cursor() as curs:
                    curs.execute("insert into student_course (student_id, course_id) values (%s, %s)",
                                 (st_id, course_id))


# просто создает студента
def add_student(student):
    columns = student.keys()
    values = [student[column] for column in columns]
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            insert_statement = 'insert into student (%s) values %s returning id'
            curs.execute(curs.mogrify(insert_statement,
                                      (AsIs(','.join(columns)),
                                       tuple(values))))
            st_id = curs.fetchone()[0]
            return st_id


def add_course(course):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("insert into course (name) values (%s)",
                         (course,))


def get_student(student_id):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("select * from student where student.id = %s",
                         (student_id,))
            selected_student = curs.fetchone()
            return selected_student


if __name__ == '__main__':
    # create_db()
    # add_course('Python')
    # add_course('PHP')
    # student_1 = {
    #     'name': 'Semen Mineev',
    #     'gpa': 10.2
    # }
    # student_2 = {
    #     'name': 'Alex Isaev',
    #     'gpa': 6.5,
    #     'birth': '1999-07-01'
    # }
    # add_student(student_1)
    # add_student(student_2)
    students = [{'name': 'Andrey', 'gpa': 6.5, 'birth': '1779-07-01'},
                {'name': 'Anton', 'gpa': 2.5, 'birth': '1989-07-04'}]
    add_students(1, students)
    # print(get_student(1))
    # print(get_students(1))
