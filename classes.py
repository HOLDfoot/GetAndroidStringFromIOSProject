# encoding=UTF-8

class PairModel:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def __str__(self):
        return "key:%s,value:%s" % (self.key, self.value)
