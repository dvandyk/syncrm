#!/usr/bin/python
# vim: set sw=4 sts=4 et tw=120 :

import filelock
import json
import logging as log

from dateutil import parser

class Repository:
    class Item:
        def __init__(self, repo, **kwargs):
            self.repo = repo

            self.id = kwargs['ID']
            self.mtime = parser.parse((kwargs['ModifiedClient'])).timestamp()
            self.name = kwargs['VissibleName'] # sic!
            self.parent_id = kwargs['Parent']
            self.type = kwargs['Type']

            if 'BlobURLGet' in kwargs:
                self.blob_url = kwargs['BlobURLGet']


        def parent(self):
            if self.parent_id == '':
                return None

            return self.repo[self.parent_id]


        def full_name(self):
            parent = self.parent()
            if parent:
                return parent.full_name() + '/' + self.name

            return self.name


    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

        with open(repo_dir + '/.syncrm/client_id') as client_id_file:
            self.client_id = client_id_file.read()

        with open(repo_dir + '/.syncrm/client_token') as client_token_file:
            self.client_token = client_token_file.read()

        self.items = {}


    def __iter__(self):
        return iter(self.items.items())


    def __getitem__(self, key):
        return self.items[key]


    def read_index(self):
        with open(self.repo_dir + '/.syncrm/index', 'r') as index_file:
            self.index = json.load(index_file)
            self.update()


    def write_index(self, index):
        self.index = index
        self.update()
        with open(self.repo_dir + '/.syncrm/index', 'w') as index_file:
            index_file.write(json.dumps(index))


    def update(self):
        self.items = {}
        for item in self.index:
            self.items[item['ID']] = self.Item(self, **item)
            # TODO
            # - delete blobURL and other unused keys
