#!/usr/bin/env python3
# Author: Hazmirul Afiq @hazmirulz
# Credit: Thanks to Thierry Husson for printTable function.
# Github: https://github.com/IceM4nn/pymysql-cli
# License: GNU GENERAL PUBLIC LICENSE
# Lightweight Pure python interactive pymysql cli client.

import pymysql

# Change this accordingly
HOST     = '' 
USERNAME = ''
PASSWORD = ''
DATABASE = ''

def main():
    try:
        connection = pymysql.connect(host=HOST,
                                     user=USERNAME,
                                 password=PASSWORD,
                                       db=DATABASE,
                              cursorclass=pymysql.cursors.SSDictCursor)
    except Exception as e:
        code, message = e.args
        print("[!] " + message)
        exit(1)

    print("Connected to " + HOST)

    while True:
        try:
            prompt = input("mysql> ")
            if prompt.strip() == 'exit':
                break

            try:   
                with connection:
                    sql = prompt
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    printTable(results)

            except Exception as e:
                code, message = e.args
                print("[!] " + message)

        except KeyboardInterrupt:
            break

    print('Bye!')
    connection.close()


def printTable(myDict, colList=None):
    if not colList: 
        colList = list(myDict[0].keys() if myDict else [])
    myList = [colList]

    for item in myDict: 
        myList.append([str(item[col] or '') for col in colList])

    colSize = [max(map(len,col)) for col in zip(*myList)]

    for i in range(0, 2)[::-1]:
        myList.insert(i, ['-' * i for i in colSize])
    myList.insert(len(myList), ['-' * i for i in colSize])
   
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
    formatSep = '-+-'.join(["{{:<{}}}".format(i) for i in colSize])
    for item in myList: 
        if item[0][0] == '-':
            print('+-'+formatSep.format(*item)+'-+')
        else:
            print('| '+formatStr.format(*item)+' |')

if __name__ == "__main__":
    main()