# coding: utf-8

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname='sirfanas_website', user='postgres', password='admin')


def get_cursor():
    return conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
