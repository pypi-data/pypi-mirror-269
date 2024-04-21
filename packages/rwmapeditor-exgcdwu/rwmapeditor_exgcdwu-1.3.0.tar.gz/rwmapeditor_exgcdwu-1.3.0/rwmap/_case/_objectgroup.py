# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et

import rwmap._util as utility
import rwmap._frame as frame
from rwmap._case._object import TObject

class ObjectGroup(frame.ElementOri):
    def __init__(self, properties:frame.ElementProperties, object_list:list[TObject])->None:
        super().__init__(properties)
        self._object_list = object_list

    def __iter__(self):
        return self._object_list

    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        properties = frame.ElementProperties.init_etElement(root)
        object_list = [TObject.init_etElement(tobject) for tobject in root if tobject.tag == "object"]
        return cls(properties, object_list)
    
    def output_str(self, objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "".join([self._object_list[i].output_str() + "\n" for i in range(0, -1)]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
    
    def __repr__(self)->str:
        return self.output_str()

    def output_etElement(self)->et.Element:
        root = et.Element("objectgroup")
        self._properties.output_etElement(root)
        for tobject in self._object_list:
            tobject_element = et.Element("object")
            tobject.output_etElement(tobject_element)
            root.append(tobject_element)
        return root
    
    def addObject(self, default_properties:dict[str, str] = {}, optional_properties:dict[str, str] = {}, other_properties:list[et.Element] = [])->None:
        self._object_list.append(TObject("object", default_properties, optional_properties, other_properties))

