# -*- coding: utf-8 -*-
#

class ArrayUtil(object):
    @classmethod
    def isIntersect(cls, array1, array2):
        for element in array1:
            if element in array2:
                return True

        return False