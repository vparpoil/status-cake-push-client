#!/usr/bin/python
# coding: utf8
from contextlib import contextmanager
import os
import json
import logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import socket
from contextlib import closing

# get an instance of the logger object this module will use
logger = logging.getLogger(__name__)


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printWarn(text):
    print(bcolors.WARNING + text + bcolors.ENDC)
    logger.warn(bcolors.WARNING + text + bcolors.ENDC)


def printFail(text):
    print(bcolors.FAIL + text + bcolors.ENDC)
    logger.critical(bcolors.FAIL + text + bcolors.ENDC)


def printInfo(text):
    print(bcolors.OKGREEN + text + bcolors.ENDC)
    logger.info(bcolors.OKGREEN + text + bcolors.ENDC)


def loadTests():
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    # load settings
    with open(scriptPath + "/tests.json") as json_data:
        try:
            data = json.load(json_data)
            if "tests" in data:
                return data["tests"]
            else:
                printFail("Json structure must be : {'tests': []}")
                exit()
        except ValueError as error:
            printFail("Json not readable")
            exit()


def testPing(test):
    response = os.system('ping -c 1 {ip}'.format(ip=test['ip']))
    if response == 0:
        pingStatusCake(test['statusCakeUrl'])
    else:
        printFail('Ping test failed for {ip}'.format(ip=test['ip']))
    return


def testMongo(test):
    try:
        port = 27017
        url = "mongodb://{user}:{password}@{host}:{port}/{database}".format(
            user=test['user'], password=test['password'], host=test['ip'], port=port, database=test['database'])

        MongoClient(url, serverSelectionTimeoutMS=10, connectTimeoutMS=20000).server_info()

        pingStatusCake(test['statusCakeUrl'])

    except ServerSelectionTimeoutError:
        printFail('Mongo test failed for host: {host}'.format(host=test['ip']))
    return


def testCurl(test):
    try:
        result = os.popen("curl {url}".format(url=test['url'])).read()
        if test['textToMatch'] in result:
            pingStatusCake(test['statusCakeUrl'])
        else:
            printFail(
                'Curl test failed for {url} - no match for {textToMatch}'.format(url=test['url'],
                                                                                 textToMatch=test['textToMatch']))
    except:
        printFail('Curl test failed for {url}'.format(url=test['url']))
    return


def testPort(test):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((test["url"], test["port"])) == 0:
            pingStatusCake(test['statusCakeUrl'])
        else:
            printFail('Port test failed for {url} - port {port} is closed'.format(url=test['url'],
                                                                                  port=test['port']))
    return


def pingStatusCake(url):
    printInfo("Status Cake Ping for url: {url}".format(url=url))
    os.system('curl "{url}"'.format(url=url))
    return


def testPostgresql(test):
    import psycopg2
    try:
        conn = psycopg2.connect(
            host=test['ip'],
            database=test['database'],
            port=test['port'],
            user=test['user'],
            password=test['password'],
            sslmode=test['sslmode']
        )
        conn.close()
        pingStatusCake(test['statusCakeUrl'])
    except (Exception, psycopg2.DatabaseError):
        printFail('Postgresql test failed for host: {host}'.format(host=test['ip']))
    return


def testSystemctl(test):
    import subprocess
    try:
        # Execute the systemctl command to get the service status
        cmd = ["systemctl", "status", test['service']]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)

        # Check if the service is active (running)
        if "Active: active (running)" in output:
            pingStatusCake(test['statusCakeUrl'])
        else:
            printFail('Systemctl test failed for service: {service}'.format(service=test['service']))
    except subprocess.CalledProcessError as e:
        printFail('Systemctl test failed for service: {service}'.format(service=test['service']))
    return
