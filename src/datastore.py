import unicodedata
import re
import cabochaparser as parser
import sqlite3
import json

class Datastore():
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect('/var/tmp/nlp/docs.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS docs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                url         TEXT,
                content     TEXT,
                meta_info   BLOB,
                sentences    BLOB,
                chunks       BLOB,
                tokens       BLOB
            )''')

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.conn.close()

    def get_all_ids(self, limit = 20, offset = 0):
        rows = self.conn.execute('SELECT id FROM docs LIMIT ? OFFSET ?', (limit, offset))
        return [row[0] for row in rows]

    def get(self, doc_id, field_name):
        row = self.conn.execute('SELECT {} FROM docs WHERE id = ?'.format(field_name), (doc_id,)).fetchone()
        if row[0] is not None:
            return row[0]
        else:
            return []

    def get_jfield(self, doc_id, field_name):
        row = self.conn.execute('SELECT {} FROM docs WHERE id = ?'.format(field_name), (doc_id,)).fetchone()
        if row[0] is not None:
            return json.loads(row[0])
        else:
            return []

    def save(self, url, content):
        content = content.strip()
        content = content.replace('\r', '')
        content = re.sub('\s+', '', content)
        content = re.sub('ー{3,}', '\n', content)
        content = unicodedata.normalize('NFKC', content)
        sentences, chunks, tokens = parser.parse(content)
        self.conn.execute('INSERT INTO docs(url, content, sentences, chunks, tokens) VALUES (?, ?, ?, ?, ?)', (url, content, json.dumps(sentences), json.dumps(chunks), json.dumps(tokens)))
        self.conn.commit()
