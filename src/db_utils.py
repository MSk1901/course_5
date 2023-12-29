import psycopg2

from .abs_classes import DataHandler, DBExecutor


class PostgresExecutor(DBExecutor):

    def __init__(self, password):
        self.__password = password

    @property
    def password(self):
        return self.__password

    def create_database(self, db_name: str):
        """Creates a database"""
        try:
            conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password=self.password,
                host="localhost",
                port="5432"
            )

            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = {db_name}")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")

            conn.close()
        except psycopg2.OperationalError as e:
            raise Exception(e)

    def create_table(self, table_name: str):
        """Creates table employers or vacancies"""
        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:

                    if table_name == "employers":
                        cursor.execute("""
                                CREATE TABLE IF NOT EXISTS employers
                                (
                                    employer_id int PRIMARY KEY,
                                    name varchar(100) NOT NULL,
                                    url varchar(255) NOT NULL
                                );
                                """)

                    elif table_name == "vacancies":
                        cursor.execute("""
                                CREATE TABLE IF NOT EXISTS vacancies
                                (
                                    vacancy_id int PRIMARY KEY,
                                    name varchar(100) NOT NULL,
                                    type varchar(20) NOT NULL,
                                    url varchar(255) NOT NULL,
                                    employer_id int REFERENCES employers (employer_id),
                                    area varchar(100) NOT NULL,
                                    salary_from int NOT NULL,
                                    salary_to int NOT NULL,
                                    schedule varchar(50) NOT NULL,
                                    employment_type varchar(50) NOT NULL,
                                    requirements text
                                );
                                """)
                    else:
                        raise ValueError("Invalid table name")

        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InternalError) as e:
            raise Exception(e)

    def insert_values(self, values, table_name: str):
        pass


class DBManager(DataHandler):

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword: str):
        pass
