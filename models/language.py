# coding: utf-8

from .model import Model


class Language(Model):
    _table = 'language'

    def _create_columns(self):
        return super()._create_columns() + [
            {'key': 'TEXT UNIQUE'},
            {'image': 'TEXT'},
        ]

    def get_by_key(self, key):
        language_id = self.select("WHERE key = '%s'" % key)
        if language_id:
            return language_id[0]
        raise KeyError('Language not found !')
