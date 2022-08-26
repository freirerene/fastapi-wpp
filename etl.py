import re
from datetime import datetime


class ETL:

    def __init__(self, contact, s, time):

        self.categoria = None
        self.val = None
        self.where = None
        self.type = None

        self.contact = contact
        self.time = time
        self.s = s

        self.day = datetime.fromtimestamp(self.time).day
        self.date = datetime.fromtimestamp(self.time).strftime('%Y-%m') + '-01'

    def proccess(self):

        if re.search('fixo', self.s):

            self.type = 'fixo'

            if re.search('-', self.s):
                self.val = -float(re.search('\d+\.?\d+?', self.s)[0])
                self.categoria = re.search('(?<=categoria:)(\w+)', self.s)[0]
                self.where = re.search('(?<=where:)(\w+)', self.s)[0]

            else:
                self.val = float(re.search('\d+\.?\d+?', self.s)[0])
                self.categoria = re.search('(?<=categoria:)(\w+)', self.s)[0]
                self.where = re.search('(?<=where:)(\w+)', self.s)[0]

        else:

            self.type = 'variavel'

            if self.day < 15:
                self.where = 'first'
            else:
                self.where = 'second'

            if re.search('-', self.s):
                self.val = -float(re.search('\d+\.?\d+?', self.s)[0])
            else:
                self.val = float(re.search('\d+\.?\d+?', self.s)[0])

            if re.search('(?=[^-])(?=[^\s])(?=[^\.])\D+', self.s):
                self.categoria = re.search('(?=[^-])(?=[^\s])(?=[^\.])\D+', self.s)[0]
            else:
                self.categoria = 'none'
