from typing import Callable, Dict, List

from foxlin.core.sophy import DBOperation, LEVEL

class FoxBox:
    """
    Foxbox is abs class as a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache and file-based db

    dbom: database operation manager
    """
    level: str = 'set level of operation'

    def operate(self, obj: DBOperation):
        operator: Callable = getattr(self, obj.op_name.lower()+'_op')
        operator(obj)

        if obj.callback:
            if self.level == obj.callback_level:
                obj.callback(obj)

class BoxManager:
    """
    Box manager design like a router
    for route & manager operations

    Parameters
    ----------
    *box: FoxBox
        get list of box for route operations by level
    auto_enable: bool = True
        by default box's are disable, must enable them
    """

    def __init__(self, *box: FoxBox, auto_enable: bool = True):
        self.box_list:    Dict[LEVEL, FoxBox] = {}
        self.__on_box_list: Dict[LEVEL, FoxBox] = {}

        self.add_box(*box, auto_enable=auto_enable)

    def operate(self, op: DBOperation):
        # send operation to own their boxes
        level_list = set(op.levels) & self.__on_box_list.keys()
        list(map(lambda level: self.__on_box_list[level].operate(op), level_list))
 
    def add_box(self, *box: FoxBox, auto_enable: bool = True):
        box_tray = {}
        for b in box:
            bargs = (b, FoxBox)
            assert isinstance(*bargs) or issubclass(*bargs)
            box_tray[b.level] = b

        if auto_enable:
            self.__on_box_list.update(box_tray)

        self.box_list.update(box_tray)

    def remove_box(self, level: LEVEL):
        self.box_list.pop(level)
        return self.__on_box_list.pop(level) # return removed box

    def enable_box(self, level: LEVEL) -> bool:
        # for enable a box to handle operations of specified level 
        if level in self.box_list.keys():
            box = self.box_list[level]
            self.__on_box_list[level] = box
            # return True for enable success 
            return True
        return False

    def disable_box(self, level:LEVEL) -> bool:
        if level in self.__on_box_list.keys():
            self.__on_box_list.pop(level)
            return True
        return False

