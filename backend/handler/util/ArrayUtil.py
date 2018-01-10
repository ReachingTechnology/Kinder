# -*- coding: utf-8 -*-
#

class ArrayUtil(object):
    @classmethod
    def isIntersect(cls, array1, array2):
        for element in array1:
            if element in array2:
                return True

        return False

    @classmethod
    def noDuplicateJoin(cls, array1, array2):
        result = array1
        for element in array2:
            if not element in array1:
                result.append(element)
        return result