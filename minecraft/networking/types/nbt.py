"""Contains definition for minecraft's NBT format.
"""
from __future__ import division
import struct

from .utility import Vector
from .basic import Type, Byte, Short, Integer, Long, Float, Double, ShortPrefixedByteArray, IntegerPrefixedByteArray

__all__ = (
    'Nbt',
)

TAG_End = 0
TAG_Byte = 1
TAG_Short = 2
TAG_Int = 3
TAG_Long = 4
TAG_Float = 5
TAG_Double = 6
TAG_Byte_Array = 7
TAG_String = 8
TAG_List = 9
TAG_Compound = 10
TAG_Int_Array = 11
TAG_Long_Array = 12


class Nbt(Type):

    @staticmethod
    def read(file_object):
        type_id = Byte.read(file_object)
        if type_id != TAG_Compound:
            raise Exception("Invalid NBT header")
        name = ShortPrefixedByteArray.read(file_object).decode('utf-8')
        a = Nbt.decode_tag(file_object, TAG_Compound)
        a['_name'] = name
        return a

    @staticmethod
    def decode_tag(file_object, type_id):
        if type_id == TAG_Byte:
            return Byte.read(file_object)
        elif type_id == TAG_Short:
            return Short.read(file_object)
        elif type_id == TAG_Int:
            return Integer.read(file_object)
        elif type_id == TAG_Long:
            return Long.read(file_object)
        elif type_id == TAG_Float:
            return Float.read(file_object)
        elif type_id == TAG_Double:
            return Double.read(file_object)
        elif type_id == TAG_Byte_Array:
            return IntegerPrefixedByteArray.read(file_object).decode('utf-8')
        elif type_id == TAG_String:
            return ShortPrefixedByteArray.read(file_object)
        elif type_id == TAG_List:
            list_type_id = Byte.read(file_object)
            size = Integer.read(file_object)
            a = []
            for i in range(size):
                a.append(Nbt.decode_tag(file_object, list_type_id))
            return a
        elif type_id == TAG_Compound:
            c = { }
            child_type_id = Byte.read(file_object)
            while child_type_id != TAG_End:
                child_name = ShortPrefixedByteArray.read(file_object).decode('utf-8')
                c[child_name] = Nbt.decode_tag(file_object, child_type_id)
                child_type_id = Byte.read(file_object)
            return c
        elif type_id == TAG_Int_Array:
            size = Integer.read(file_object)
            a = []
            for i in range(size):
                a.append(Integer.read(file_object))
            return a
        elif type_id == TAG_Long_Array:
            size = Integer.read(file_object)
            a = []
            for i in range(size):
                a.append(Long.read(file_object))
            return a
        else:
            raise Exception("Invalid NBT tag type")

    @staticmethod
    def send(value, socket):
        # TODO
        pass


