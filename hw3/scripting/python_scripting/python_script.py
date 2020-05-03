#!/usr/bin/python

import sys
import argparse
import os
import json


class ExceptionScript(Exception):
    def __init__(self, text):
        self.txt = text


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-j', '--json', action='store_const', const=True)
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


def number_all_requests(file_open, file_write, file_json=None):
    count = 0
    for _ in line_gen(file_open):
        count += 1
    file_write.write(str(count))
    file_write.write("\n")
    if file_json:
        return {'task1': count}
    return count


def number_type_requests(file_open, file_write, file_json=None):
    request_dict = {}
    for line in line_gen(file_open):
        line_split = line.split()
        type_request = line_split[5][1:]
        if type_request in request_dict:
            request_dict[type_request] += 1
        else:
            request_dict.update({type_request: 1})
    for element in request_dict:
        file_write.write(element)
        file_write.write(" ")
        file_write.write(str(request_dict[element]))
        file_write.write("\n")
    if file_json:
        return {'task2': request_dict}
    return request_dict


def biggest_requests_10(file_open, file_write, file_json=None):
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
        for value in element:
            file_write.write(value)
            file_write.write(" ")
        file_write.write("\n")
    if file_json:
        return {'task3': mas_value}
    return mas_value


def top_10_client_error_counter(file_open, file_write, file_json=None):
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
        for value in element:
            file_write.write(value)
            file_write.write(" ")
        file_write.write("\n")
    if file_json:
        return {'task4': mas_value}
    return mas_value


def top_10_client_error_biggest(file_open, file_write, file_json=None):
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
        for key, value in enumerate(element):
            if key == 4:
                element.pop(4)
                continue
            file_write.write(value)
            file_write.write(" ")
        file_write.write("\n")
    if file_json:
        return {'task5': mas_value}

    return mas_value



def biggest_top_memory(file_open, file_write, file_json=None):
    from operator import itemgetter
    mas_value = []
    file_open.seek(0)
    for line in file_open.readlines():
        line_split = line.split()
        request_element = list()
        request_element.append(line_split[5][1:])
        request_element.append(line_split[6])
        request_element.append(line_split[0])
        request_element.append(line_split[3][1:])
        request_element.append(int(line_split[9]))
        mas_value.append(request_element)
    mas_value = sorted(mas_value, key=itemgetter(4), reverse=True)
    for element in mas_value[:10]:
        for value in element:
            file_write.write(str(value))
            file_write.write(" ")
        file_write.write("\n")
    if file_json:
        return {'task3': mas_value[:10]}

    return mas_value[:10]


def print_all(file_open, file_write, file_json=None):
    json_dict = {}
    task_1 = number_all_requests(file_open, file_write, file_json)
    print(task_1)
    file_write.write("------------------------------------")
    file_write.write("\n")
    if file_json:
        json_dict.update(task_1)
    task_2 = number_type_requests(file_open, file_write, file_json)
    print(task_2)
    file_write.write("------------------------------------")
    file_write.write("\n")
    if file_json:
        json_dict.update(task_2)
    task_3 = biggest_requests_10(file_open, file_write, file_json)
    print(task_3)
    file_write.write("------------------------------------")
    file_write.write("\n")
    if file_json:
        json_dict.update(task_3)
    task_4 = top_10_client_error_counter(file_open, file_write, file_json)
    print(task_4)
    file_write.write("------------------------------------")
    file_write.write("\n")
    if file_json:
        json_dict.update(task_4)
    task_5 = top_10_client_error_biggest(file_open, file_write, file_json)
    print(task_5)
    if file_json:
        json_dict.update(task_5)
        file_json.write(json.dumps(json_dict))


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.file:
        norm_filename = os.path.normpath(namespace.file)
        if os.path.exists(norm_filename):
            if os.path.isdir(norm_filename):
                file_gen = passage(os.path.normpath(namespace.file))
                for num, file_dir in enumerate(file_gen):
                    with open(os.path.normpath(file_dir), 'r') as file_open, \
                            open("info_{0}_{1}".format(num, file_dir.split("/")[-1]), "w") as file_write:
                        if namespace.json:
                            with open("json_{}.json".format(num, file_dir.split("/")[-1]), 'w') as file_json:
                                print_all(file_open, file_write, file_json)
                        else:
                            print_all(file_open, file_write)
            else:
                with open(norm_filename, 'r') as file_open, \
                        open("info_{}".format(norm_filename.split("/")[-1]), "w") as file_write:
                    if namespace.json:
                        with open("json_{}.json".format(norm_filename.split("/")[-1]), 'w') as file_json:
                            print_all(file_open, file_write, file_json)
                    else:
                        print_all(file_open, file_write)
        else:
            raise ExceptionScript("File/path must exist")
    else:
        raise ExceptionScript("Choose log file")
