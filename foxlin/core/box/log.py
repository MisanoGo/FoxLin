import os

from .fox import FoxBox
from foxlin.core.sophy import DBOperation, Log

class LogBox(FoxBox):
    level: str = 'log'

    def operate(self, obj: DBOperation):
        path = '.log'
        log_text = [
            ' ; '.join([*[getattr(log,i) for i in log.__annotations__.keys()], '\n'])
            for log in obj.logs
        ]

        if not os.path.exists(path):
            with open(path, 'w') as log_file:
                log_file.write((' ; '.join([i.upper() for i in Log.__annotations__.keys()])+'\n'))

        with open('.log','a') as log_file:
            log_file.writelines(log_text)

