#!/usr/bin/python

import sys
import argparse
import os

from models import LogFile, Task1, Task2, Task3, Task4, Task5
from orm_builder import MysqlOrmBuilder
from mysql_orm_client import MysqlOrmConnection


class ExceptionScript(Exception):
    def __init__(self, text):
        self.txt = text


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-U', '--user')
    parser.add_argument('-P', '--password')
    parser.add_argument('-d', '--database')
    parser.add_argument('-i', '--ip')
    parser.add_argument('-p', '--port')
    return parser


def passage(folder):
    for element in os.scandir(folder):
        if element.is_file():
            yield folder + '/' + element.name
        elif element.is_dir():
            yield from passage(element.path)


def line_gen(f_name):
    f_name.seek(0)
    while True:
        line = f_name.readline()
        if not line:
            break
        yield line


def number_all_requests(file_open, session, file_id):
    count = 0
    for _ in line_gen(file_open):
        count += 1
    task1 = Task1(
        counter=count,
        file_id=file_id
    )
    session.add(task1)
    session.commit()
    return count


def number_type_requests(file_open, session, file_id):
    request_dict = {}
    for line in line_gen(file_open):
        line_split = line.split()
        type_request = line_split[5][1:]
        if type_request in request_dict:
            request_dict[type_request] += 1
        else:
            request_dict.update({type_request: 1})
    for element in request_dict:
        task2 = Task2(
            request_type=element,
            counter=request_dict[element],
            file_id=file_id
        )
        session.add(task2)
    session.commit()
    return request_dict


def biggest_requests_10(file_open, session, file_id):
    mas_value = list()
    for line in line_gen(file_open):
        line_split = line.split()
        request_element = list()
        request_element.append(line_split[5][1:])
        request_element.append(line_split[6])
        request_element.append(line_split[0])
        request_element.append(line_split[3][1:])
        request_element.append(line_split[9])
        check = False
        if not mas_value:
            mas_value.append(request_element)
            check = True
        for key, item in enumerate(mas_value):
            if int(line_split[9]) > int(item[4]):
                mas_value.insert(key, request_element)
                check = True
                if len(mas_value) > 10:
                    mas_value.pop()
                break
        if len(mas_value) < 10 and check is False:
                mas_value.append(request_element)
    for element in mas_value:
        task3 = Task3(
            request_type=element[0],
            url=element[1],
            ip=element[2],
            date=element[3],
            size=element[4],
            file_id=file_id
        )
        session.add(task3)
    session.commit()
    return mas_value


def top_10_client_error_counter(file_open, session, file_id):
    mas_value = {}
    for line in line_gen(file_open):
        line_split = line.split()
        request_element = list()
        request_element_str = ''
        request_element.append(line_split[5][1:])
        request_element_str += line_split[5][1:]
        request_element.append(line_split[6])
        request_element_str += line_split[6]
        request_element.append(line_split[8])
        request_element_str += line_split[8]
        request_element.append(line_split[0])
        request_element_str += line_split[0]
        if (500 > int(line_split[8]) >= 400):
            if request_element_str not in mas_value:
                mas_value.update({request_element_str: [1, request_element]})
            else:
                mas_value[request_element_str][0] += 1
    mas_value = [value[1] for key, value in sorted(mas_value.items(), key=lambda item: item[1][0], reverse=True)[:10]]
    for element in mas_value:
        task4 = Task4(
            request_type=element[0],
            url=element[1],
            error_code=element[2],
            ip=element[3],
            file_id=file_id
        )
        session.add(task4)
    session.commit()
    return mas_value


def top_10_client_error_biggest(file_open, session, file_id):
    mas_value = list()
    for line in line_gen(file_open):
        line_split = line.split()
        request_element = list()
        request_element.append(line_split[5][1:])
        request_element.append(line_split[6])
        request_element.append(line_split[8])
        request_element.append(line_split[0])
        request_element.append(line_split[9])
        check = False
        if (500 > int(line_split[8]) >= 400):
            if not mas_value:
                mas_value.append(request_element)
                check = True
            for key, item in enumerate(mas_value):
                if int(line_split[9]) > int(item[4]):
                    mas_value.insert(key, request_element)
                    check = True
                    if len(mas_value) > 10:
                        mas_value.pop()
                    break
            if len(mas_value) < 10 and check is False:
                mas_value.append(request_element)
    for element in mas_value:
        task5 = Task5(
            request_type=element[0],
            url=element[1],
            error_code=element[2],
            ip=element[3],
            file_id=file_id
        )
        session.add(task5)
    session.commit()
    return mas_value


def get_all(file_open, session):
    file_row = LogFile(
        name=file_open.name,
    )
    session.add(file_row)
    session.commit()
    number_all_requests(file_open, session, file_row.id)
    number_type_requests(file_open, session, file_row.id)
    biggest_requests_10(file_open, session, file_row.id)
    top_10_client_error_counter(file_open, session, file_row.id)
    top_10_client_error_biggest(file_open, session, file_row.id)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.file:
        norm_filename = os.path.normpath(namespace.file)
        if os.path.exists(norm_filename):
            if namespace.user:
                if namespace.password:
                    if namespace.database:
                        if namespace.ip:
                            if namespace.port:
                                connection = MysqlOrmConnection(namespace.user, namespace.password, namespace.database,
                                                                namespace.ip, int(namespace.port))
                                builder = MysqlOrmBuilder(connection)
                                if os.path.isdir(norm_filename):
                                    file_gen = passage(os.path.normpath(namespace.file))
                                    for num, file_dir in enumerate(file_gen):
                                        with open(os.path.normpath(file_dir), 'r') as file_open:
                                            get_all(file_open, connection.session)
                                else:
                                    with open(norm_filename, 'r') as file_open:
                                        get_all(file_open, connection.session)
                            else:
                                raise ExceptionScript("Choose port")
                        else:
                            raise ExceptionScript("Choose ip")
                    else:
                        raise ExceptionScript("Choose database")
                else:
                    raise ExceptionScript("Choose password")
            else:
                raise ExceptionScript("Choose user")
        else:
            raise ExceptionScript("File/path must exist")
    else:
        raise ExceptionScript("Choose log file")
