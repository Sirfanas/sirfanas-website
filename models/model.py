# coding: utf-8

from .db_connector import get_cursor


class Model:
    _table = 'model'  # Database table

    def select(self, sql_where_clause=''):
        sql = self._select() + ' ' + sql_where_clause
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
        return "CREATE TABLE IF NOT EXISTS " + self._table + " (" + \
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
                if k:
                    cols.append(k)
        return cols

    def insert(self, data):
        sql = self._insert(data)
        conn, cr = get_cursor()

        cr.execute(sql, data)
        new_id = cr.fetchone()['id']
        conn.commit()
        cr.close()
        return new_id

    def _insert(self, data):
        cols, parser = '', ''
        for column in data.keys():
            cols += column + ', '
            parser += '%(' + column + ')s, '
        cols = cols[:-2]
        parser = parser[:-2]
        return "INSERT INTO %s (%s) VALUES (%s) RETURNING id" % (self._table, cols, parser)

    def update(self, update_id, data):
        if 'ids' in data:
            del data['ids']
        sql = self._update(data)
        data['id'] = update_id
        conn, cr = get_cursor()
        cr.execute(sql, data)
        conn.commit()
        cr.close()
        return True

    def _update(self, data):
        data_format = ''
        for col, value in data.items():
            data_format += '%s = %s, ' % (col, '%(' + col + ')s')
        data_format = data_format[:-2]
        return "UPDATE %s SET %s WHERE id = %s" % (self._table, data_format, '%(id)s')
