# coding: utf-8

from .model import Model


class Language(Model):
    _table = 'language'

    def _create_columns(self):
        return super()._create_columns() + [
            {'key': 'TEXT UNIQUE'},
            {'image': 'TEXT'},
        ]

#
# l = Language()
# l.create_table()
# l.insert({'key': 'en-EN', 'image': 'img/flags/gb.svg'})
