from typing import Callable, Dict, List, Optional, Set

from foxlin.core.database import LEVEL
from foxlin.core.operation import DBOperation

NONE = LEVEL('NONE')

class FoxBox:
    """
    Foxbox is abs class as a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache and file-based db

    dbom: database operation manager
    """
    level: LEVEL = NONE # set level of operation

    def operate(self, obj: DBOperation):
        """
        we use the name has defined in operations.name for finding the function we need to use 
        """
        operator: Callable = getattr(self, obj.op_name.lower()+'_op')
        operator(obj)

        if obj.callback:
            if self.level == obj.callback_level:
                obj.callback(obj)

class BoxManager:
    """
    Manages a collection of FoxBox instances for routing operations.

    Parameters
    ----------
    *box: FoxBox
        FoxBox instances to manage.
    auto_enable: bool, optional
        Automatically enable added boxes (default is True).
    """

    def __init__(self, *box: FoxBox, auto_enable: bool = True):
        self.box_list: Dict[LEVEL, FoxBox] = {}
        self.__box_list: Dict[LEVEL, FoxBox] = {}
        self.add_box(*box, auto_enable=auto_enable)

    def operate(self, op: DBOperation) -> None:
        """Send an operation to boxes that can handle it."""
        level_list: Set[LEVEL] = set(op.levels) & self.__box_list.keys()
        for level in level_list:
            self.__box_list[level].operate(op)

    def add_box(self, *box: FoxBox, auto_enable: bool) -> None:
        """Add one or more boxes to the manager."""
        box_tray: Dict[LEVEL, FoxBox] = {}
        
        for b in box:
            if not isinstance(b, FoxBox):
                raise TypeError(f"Expected instance of FoxBox, got {type(b).__name__}")
            box_tray[b.level] = b

        if auto_enable:
            self.__box_list.update(box_tray)

        self.box_list.update(box_tray)

    def remove_box(self, level: LEVEL) -> Optional[FoxBox]:
        """Remove a box by its level."""
        self.box_list.pop(level, None)
        return self.__box_list.pop(level, None)  # Return the removed box or None

    def enable_box(self, level: LEVEL) -> bool:
        """Enable a box to handle operations for the specified level."""
        if level in self.box_list:
            self.__box_list[level] = self.box_list[level]
            return True
        return False

    def disable_box(self, level: LEVEL) -> bool:
        """Disable a box from handling operations for the specified level."""
        if level in self.__box_list:
            self.__box_list.pop(level)
            return True
        return False