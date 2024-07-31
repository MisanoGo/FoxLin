import os

from foxlin.core.operation.base import DBOperation, Log, LEVEL, LOG

from .base import FoxBox


class LogBox(FoxBox):
    level: LEVEL = LOG

    def operate(self, obj: DBOperation):
        path = '.log'
        
        print(f"Number of logs: {len(obj.logs)}")  # Debug print
        
        log_text = []
        for log in obj.logs:
            print(f"Processing log: {log.box_level}")  # Debug print
            attributes = [str(getattr(log, i, '')) for i in log.__annotations__.keys()]
            log_line = ' ; '.join(attributes) + '\n'
            log_text.append(log_line)
        

        if not os.path.exists(path):
            with open(path, 'w') as log_file:
                header = ' ; '.join([i.upper() for i in Log.__annotations__.keys()]) + '\n'
                log_file.write(header)
                print(f"Wrote header: {header}")  # Debug print

        with open('.log', 'a') as log_file:
            log_file.writelines(log_text)
            print(f"Wrote {len(log_text)} lines to log file")  # Debug print