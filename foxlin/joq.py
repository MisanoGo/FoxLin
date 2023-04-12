class JsonQuery(object):
    def __init__(self, session):
        self.session = session
        self.records = []
        self.reset()

    def reset(self):
        self.records = list(self.session._db['ID'].values())

    def get(self):
        for ID in self.records:
            yield self.session.get_by_id(ID)
        self.reset()

    def SELECT(self,*args,**kwargs):
        return self

    def WHERE(self, column, operator, value):
        self.records = list(self.session._db[column].bvdata[value])
        return self

    def GROUP_BY(self,*args,**kwargs):
        return self

    def ORDER_BY(self,*args,**kwargs):
        return self

    def HAVING(self,*args,**kwargs):
        return self

    def LIMIT(self, n: int):
        self.records = self.records[:n]
        return self
