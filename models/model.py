# coding: utf-8

from .db_connector import get_cursor


class Model:
    _table = 'model'  # Database table

    def select(self):
        sql = self._select()
        conn, cr = get_cursor()
        cr.execute(sql)
        return cr.fetchall()

    def _select(self):
        return "SELECT " + \
            ', '.join(self.get_columns()) + \
            " FROM " + self._table

    def create_table(self):
        sql = self._create_table()
        conn, cr = get_cursor()
        cr.execute(sql)
        conn.commit()
        cr.close()

    def _create_table(self):
        return "CREATE TABLE IF NOT EXISTS " + self._table + "(" + \
            self._create_columns_str() + \
            ")"

    def _create_columns(self):
        return [
            {'id': 'SERIAL PRIMARY KEY'},
            {'create_date': 'TIMESTAMP'}
        ]

    def _create_columns_str(self):
        columns = self._create_columns()
        res = ''
        for column in columns:
            for k in column.keys():
                res += '%s %s,' % (k, column[k])
        return res[:-1]

    def get_columns(self):
        cols = []
        for column in self._create_columns():
            for k in column.keys():
                cols.append(k)
        return cols

    def insert(self, data):
        sql = self._insert(data)
        conn, cr = get_cursor()
        cr.execute(sql, data)
        conn.commit()
        cr.close()

    def _insert(self, data):
        cols, parser = '', ''
        for column in data.keys():
            cols += column + ', '
            parser += '%(' + column + ')s, '
        cols = cols[:-2]
        parser = parser[:-2]
        return "INSERT INTO %s (%s) VALUES (%s)" % (self._table, cols, parser)
