import psycopg2
from psycopg2 import Error


class StudentDatabase:
    """
    A class representing a PostgreSQL database for student records.

    Attributes:
        dbname (str): The name of the database.
        user (str): The username for connecting to the database.
        password (str): The password for connecting to the database.
        host (str): The host address of the database server.
        port (str): The port number for connecting to the database.
        connection (psycopg2.connection): The connection object to interact with the database.
    """

    def __init__(self, dbname, user, password, host, port):
        """
        Initialize the StudentDatabase object with database connection details.

        Args:
            dbname (str): The name of the database.
            user (str): The username for connecting to the database.
            password (str): The password for connecting to the database.
            host (str): The host address of the database server.
            port (str): The port number for connecting to the database.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """
        Establish a connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            print("Connected to the PostgreSQL database successfully")
        except Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def disconnect(self):
        """
        Close the connection to the PostgreSQL database.
        """
        if self.connection:
            self.connection.close()
            print("Disconnected from the PostgreSQL database")

    def execute_query(self, query, params=None):
        """
        Execute a SQL query on the connected database.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters to be used in the query.

        Returns:
            psycopg2.cursor: The cursor object for fetching results.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")

    def getAllStudents(self):
        """
        Retrieve and print all student records from the database.
        """
        print("Printing All Students: ")
        query = "SELECT * FROM students"
        cursor = self.execute_query(query)
        if cursor:
            students = cursor.fetchall()
            for student in students:
                print(student)

    def addStudent(self, first_name, last_name, email, enrollment_date):
        """
        Add a new student record to the database.
        """
        query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)"
        params = (first_name, last_name, email, enrollment_date)
        self.execute_query(query, params)
        print("Added Student:", first_name, last_name)

    def updateStudentEmail(self, student_id, new_email):
        """
        Update the email address of a student in the database.
        """
        query = "UPDATE students SET email = %s WHERE student_id = %s"
        params = (new_email, student_id)
        self.execute_query(query, params)
        print("Updated Email for:", new_email, "Student ID:", student_id)

    def deleteStudent(self, student_id):
        """
        Delete a student record from the database.
        """
        query = "DELETE FROM students WHERE student_id = %s"
        params = (student_id,)
        self.execute_query(query, params)
        print("Deleted Student:", student_id)


def main():
    # Creating database object
    db = StudentDatabase(
        dbname="A3 - Q1",
        user="postgres",
        password="comp3005",
        host="localhost",
        port="5432",
    )
    db.connect()

    # Create Schema
    schema_query = """
        CREATE TABLE students (
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE
    );
    """
    db.execute_query(schema_query)

    # Insert Data
    data_query = """
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
    """
    db.execute_query(data_query)

    # Display all students
    db.getAllStudents()

    # Add a new student
    db.addStudent("Joshua", "Test", "another213@email.com", "2024-03-15")

    # Display all students after adding a new student
    db.getAllStudents()

    # Update email of a student
    db.updateStudentEmail(4, "updated@email.com")

    # Display all students after updating email
    db.getAllStudents()

    # Delete a student
    db.deleteStudent(4)

    # Display all students after deleting a student
    db.getAllStudents()

    # Disconnect from the database
    db.disconnect()


main()