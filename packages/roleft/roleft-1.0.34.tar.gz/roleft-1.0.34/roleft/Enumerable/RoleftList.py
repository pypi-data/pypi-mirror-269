import random
from typing import Dict, List, Generic, MutableSequence, TypeVar, Callable, Union

# import copy
import json

from roleft.Entities.RoleftKeyValue import KeyValue


T = TypeVar("T")
TOut = TypeVar("TOut")


# class xList(MutableSequence[T], Generic[T]):
class xList(Generic[T]):
    # def __init__(self, list: List[T] = []) -> None:
    #     self.__items: List[T] = list

    # 来自 chatgpt: 这是因为在 Python 中，函数默认参数的默认值在函数定义时被计算，
    # 而不是每次函数调用时重新计算。对于可变对象（如列表、字典等），
    # 如果将其作为默认参数，它只会在函数定义时被创建一次，并且之后所有调用该函数的实例都会共享同一个默认对象。
    def __init__(self, list: List[T] = []) -> None:
        self.__items: List[T] = list if len(list) > 0 else []

    # def __genRefOtherList(self) -> list[T]:
    #     tpl = tuple(self.__items)
    #     return list(tpl)

    def CloneNew(self):
        # tp1 = tuple(self.__items)
        return xList[T](list(self.__items))

    def Add(self, item: T):
        self.__items.append(item)
        return self

    def Exists(self, predicate: Callable[[T], bool]) -> bool:
        for x in self.__items:
            if predicate(x):
                return True

        return False

    def AddRange(self, others: list[T]):
        self.__items += others
        return self

    def RemoveAt(self, index: int):
        del self.__items[
            index
        ]  # 【闻祖东 2023-07-26 102651】其实 self.__items.pop(index) 也可以
        return self

    def Remove(self, item: T):
        self.__items.remove(item)
        return self

    @property
    def Count(self):
        return len(self.__items)

    def Clear(self):
        self.__items = []
        return self

    def FindAll(self, predicate: Callable[[T], bool]):
        lst = []
        for x in self.__items:
            if predicate(x):
                lst.append(x)

        return xList[T](lst)

    def First(self, predicate: Callable[[T], bool]):
        newItems = self.FindAll(predicate).ToList()
        return newItems[0] if len(newItems) > 0 else None

    def Find(self, predicate: Callable[[T], bool]):
        return self.First(predicate)

    def FirstIndex(self, predicate: Callable[[T], bool]):
        index = 0
        for x in self.__items:
            if predicate(x):
                return index
            index += 1

        return -1

    def ToList(self):
        return self.__items

    def InsertAt(self, item: T, index: int):
        self.__items.insert(index, item)
        return self

    def RemoveAll(self, predicate: Callable[[T], bool]):
        indexes = list[int]()
        index = 0
        for item in self.__items:
            if predicate(item):
                indexes.append(index)
            index += 1

        indexes.reverse()
        for idx in indexes:
            self.RemoveAt(idx)

        return self

    def Shuffle(self):
        random.shuffle(self.__items)
        return self

    def Print(self):
        print(self.__items)

    def Select(self, predicate: Callable[[T], TOut]):
        lst = []
        for x in self.__items:
            lst.append(predicate(x))

        return xList[TOut](lst)

    def OrderByAsc(self, predicate: Callable[[T], str]):
        xstKts = self.Select(lambda x: KeyValue(predicate(x), x))
        lstKeys = xstKts.Select(lambda x: x.key).ToList()
        lstKeys.sort()

        lstFin = []
        newLst = self.CloneNew()
        for key in lstKeys:
            item = newLst.First(lambda x: key == predicate(x))
            lstFin.append(item)
            newLst.Remove(item)

        newLst = xList[T](lstFin)
        self.__items = newLst.ToList()
        return self

    def OrderByDesc(self, predicate: Callable[[T], str]):
        xstAsc = self.OrderByAsc(predicate)
        return xstAsc.Reverse()

    def Reverse(self):
        self.__items.reverse()
        return self

    def DistinctBy(self, predicate: Callable[[T], TOut]):
        lst = []
        keys = set()
        for item in self.__items:
            key = predicate(item)
            if key not in keys:
                keys.add(key)
                lst.append(item)

        other = xList[T](lst)
        self.__items = other.ToList()
        return self

    # 【闻祖东 2024-01-19 183900】python应该是不支持这种ForEach，暂时算了吧
    def ForEach(self, predicate: Callable[[T], None]):
        for x in self.__items:
            predicate(x)

    def Contains(self, item: T):
        for x in self.__items:
            if x == item:
                return True

        return False

    def xTake(self, count: int):
        lst = self.__items[:count]
        return xList[T](lst)

    def xSkip(self, count: int):
        # newLst = self.__genRefOtherList()
        newLst = list(self.__items)
        cnt = min(newLst.__len__(), count)
        for i in range(0, cnt):
            newLst.pop(0)

        return xList[T](newLst)

    def Avg(self, predicate: Callable[[T], int | float]):
        return 0 if self.Count == 0 else self.Sum(predicate) / self.Count

    def Sum(self, predicate: Callable[[T], int | float]):
        total = 0.0
        for x in self.__items:
            total = total + predicate(x)

        return total


# lst = xList(['a','b','c','d'])

# # other = [5,6,7]
# hoho = lst.InsertAt('a', 3)
# haha = lst.xInsertAt('c', 3)

lst = xList([1, 2, 3, 4, 5, 2, 4, 1])

# haha = lst.xReverse()
hoho = lst.DistinctBy(lambda x: x)

pass


class Student:
    def __init__(self, id=0, name="", age=0) -> None:
        self.Id = id
        self.Name = name
        self.Age = age
        pass


stus = xList[Student]()
stus.Add(Student(1, "jack", 54))
stus.Add(Student(2, "pony", 47))
stus.Add(Student(3, "雷军", 35))
stus.Add(Student(4, "冯仑", 67))
stus.Add(Student(5, "王大爷", 67))


def AddAge(item: Student):
    item.Age = item.Age + 1


stus.ForEach(AddAge)


# new = stus.OrderByAsc(lambda x: x.Age)
# other = stus.OrderByDesc(lambda x: x.Age)

# disct = stus.DistinctBy(lambda x: x.Age)
pass
