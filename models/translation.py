# coding: utf-8

from .model import Model
from .language import Language


class Translation(Model):
    _table = 'translation'

    def _create_columns(self):
        return super()._create_columns() + [
            {'language_id': 'INTEGER REFERENCES language (id)'},
            {'key': 'TEXT'},
            {'content': 'TEXT'},
            {'': 'CONSTRAINT unique_language_key UNIQUE (language_id, key)'}
        ]

    def apply_translations(self, lang_code, route, tid, content):
        language_id = Language().get_by_key(lang_code)
        key = route + tid
        translation_id = self.select("WHERE key = '%s' and language_id = '%s'" % (key, language_id['id']))
        if translation_id:
            return self.update(translation_id[0]['id'], {
                'content': content,
            })
        return self.insert({
            'language_id': language_id['id'],
            'key': key,
            'content': content,
        })

    def get_translation(self, lang_code, key):
        language_id = Language().get_by_key(lang_code)
        translation_id = self.select("WHERE key = '%s' AND language_id = '%s'" % (key, language_id['id']))
        if translation_id:
            return translation_id[0]['content']
        return ""

Translation().create_table()