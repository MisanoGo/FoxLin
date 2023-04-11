

class JsonQuery(object):
    def __init__(self, session):
        self.session = session
        self.records = []
        self.clear()

    def reset(self):
        self.records = list(self.session._db['ID'].values())

    def get(self):
        data = [self.session.select(ID) for ID in self.records]
        self.reset()
        return data

    def SELECT(self,*args,**kwargs):
        return self

    def WHERE(self,*args,**kwargs):
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
