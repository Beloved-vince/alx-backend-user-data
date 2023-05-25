#!/usr/bin/env python3
""""""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filter_datum that returns the log message obfuscated:

        Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object
            Update the class to accept a list of strings fields constructor argument.

        Implement the format method to filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.

        DO NOT extrapolate FORMAT manually. The format method should be less than 5 lines long.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Database credentials should NEVER be stored in code or checked into version control. One secure option
    is to store them as environment variable on the application server.

        In this task, you will connect to a secure holberton database to
        read a users table. The database is protected by a username and password that
        are set as environment variables on the server named
        PERSONAL_DATA_DB_USERNAME (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default as an empty string)
        and PERSONAL_DATA_DB_HOST (set the default as “localhost”).

        The database name is stored in PERSONAL_DATA_DB_NAME.

        Implement a get_db function that returns a connector to the database (mysql.connector.connection.MySQLConnection object).

        Use the os module to obtain credentials from the environment
        Use the module mysql-connector-python to connect to the MySQL database (pip3 install mysql-connector-python)
    """
    return mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME', ''),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        port=3306,
    )


def main():
    """
    Implement a main function that takes no arguments and returns nothing.

    The function will obtain a database connection using get_db and retrieve
    all rows in the users table and display
    each row under a filtered format like this:
    Obtains a database connection using get_db and retrieves all rows
    in the users table and display each row under a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    sql_logger = get_logger()
    retrieved_data = []
    for row in cursor:
        message = f'name={row[0]}; email={row[1]}; phone={row[2]}; ' \
                  f'ssn={row[3]}; password={row[4]}; ip={row[5]}; ' \
                  f'last_login={row[6]}; user_agent={row[7]};'
        retrieved_data.append(filter_datum(PII_FIELDS, '***', message, '; '))
    for datum in retrieved_data:
        sql_logger.info(datum)
    cursor.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


if __name__ == '__main__':
    main()