import os
from oss_client.utils import content_md5


class FileObject(object):
    def __init__(self, name="", obj=None, hash_value=None, storage=None):
        if not (obj or hash_value):
            raise ValueError("obj and hash_value both are None")
        self.obj = obj
        self.name = name
        self.suffix = ""
        self.length = 0
        self._content = None
        self.hash_value = hash_value
        self.storage = storage
        names = name.split(".")
        if len(names) > 1:
            self.suffix = names[-1]
        if not self.hash_value and self.obj:
            self._content = self.obj.read()
            self.length = len(self._content)
            self.hash_value = content_md5(self._content)
            self.obj.seek(0, os.SEEK_SET)

    def __str__(self):
        return self.hash_value
    
    def read(self):
        if self._content:
            return self._content
        if self.obj:
            self._content = self.obj.read()
            self.obj.seek(0, os.SEEK_SET)
        return self._content

    def key(self):
        if self.suffix:
            return ".".join([self.hash_value, self.suffix])
        return self.hash_value

    def content(self, range=None):
        r = self.read()
        if r:
            return r
        if self.storage:
            self._content = self.storage.read(self.key(), range)
            return self._content
        raise Exception("can not find content")
