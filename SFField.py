import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Iterable, Optional
from html import escape

from .SFType import *


@dataclass
class SFField:
    full_name: str
    label: str
    length: Optional[int]
    required: bool
    dtype: SFType
    unique: bool

    @classmethod
    def from_xml(cls, xml: str):
        tree = ET.fromstring(xml)
        fields = {k: v for k, v in map(lambda x: (x.tag.split('}')[-1], x.text), tree.iter())}
        full_name = fields['fullName']
        if full_name is None:
            raise Exception('full_name is None')
        label = fields.get('label')
        if label is None:
            label = full_name

        length = fields.get('length')
        length = None if length is None else int(length)
        required: bool = False if fields.get('required') is None or fields.get('required') == 'false' else True
        unique: bool = False if fields.get('unique') is None or fields.get('unique') == 'false' else True
        formula = fields.get('formula')
        dtype = fields.get('type')
        scale = fields.get('scale')
        scale = None if scale is None else int(scale)
        precision = fields.get('precision')
        precision = None if precision is None else int(precision)
        relationshipLabel = fields.get('relationshipLabel')
        relationshipName = fields.get('relationshipName')
        referenceTo = fields.get('referenceTo')

        ntype: SFType

        match dtype:
            case 'AutoIncrementNumber':
                ntype = AutoIncNum()
            case ('Formula' | 'Checkbox') as f:
                match f:
                    case 'Formula':
                        ntype = Formula(formula)
                    case 'Checkbox':
                        ntype = CheckBox(formula)
            case 'Lookup' | 'Extended Lookup' as f:
                if relationshipLabel is None or relationshipName is None or referenceTo is None:
                    print(f'One of {relationshipLabel=}, {relationshipName=}, or {referenceTo=} is None when type is {f} for {label}')
                    ntype = Lookup(str(relationshipLabel), str(relationshipName), str(referenceTo))
                    return SFField(full_name, label, length, required, ntype, unique)
                match f:
                    case 'Lookup':
                        ntype = Lookup(relationshipLabel, relationshipName, referenceTo)
                    case 'Extended Lookup':
                        ntype = ExtLookup(relationshipLabel, relationshipName, referenceTo)
            case 'Currency':
                ntype = Currency()
            case 'Date':
                ntype = Date()
            case 'DateTime':
                ntype = DateTime()
            case 'Email':
                ntype = Email()
            case 'Geolocation' | 'Location':
                ntype = Geolocation()
            case 'Hierarchy':
                ntype = Hierarchy()
            case 'Html':
                ntype = Html()
            case 'MasterDetail':
                ntype = MasterDetail()
            case 'Number':
                if scale is None or precision is None:
                    raise ValueError(f'{scale=} or {precision=} is None when dtype is Number')
                ntype = Number(scale, precision)
            case 'Percent':
                ntype = Percent()
            case 'Phone':
                ntype = Phone()
            case 'Picklist':
                ntype = Picklist()
            case 'MultiselectPicklist':
                ntype = PicklistMulti()
            case 'Summary':
                ntype = Summary()
            case 'Text':
                if length is None:
                    length = 0
                ntype = Text(length)
            case 'TextArea':
                ntype = TextArea()
            case 'TextAreaLong' | 'LongTextArea':
                ntype = TextAreaLong()
            case 'TextAreaRich':
                ntype = TextAreaRich()
            case 'TextEncrypted':
                ntype = TextEncrypted()
            case 'Time':
                ntype = Time()
            case 'Url':
                ntype = URL()
            case None:
                ntype = Text(0)
            case _:
                raise ValueError(f'{dtype=} isn\'t defined on {label}')
    
        return SFField(escape(full_name), escape(label), length, required, ntype, unique)

    def to_dot(self) -> str:
        return f"""<TR><TD port="{self.full_name}" ALIGN="LEFT" BORDER="0">
        {'<FONT color="red">*</FONT>' if self.required else ''}{self.full_name} ({self.label}): {self.dtype}{f"({self.length})" if self.length else ""}{' <FONT color="blue">UNIQUE</FONT>' if self.unique else ''}
    </TD></TR>"""

    @classmethod
    def from_folder(cls, folder_path: str) -> Iterable['SFField']:
        yield from map(lambda file: SFField.from_xml(open(file, encoding='utf-8').read()), os.scandir(folder_path) if os.path.exists(folder_path) else [])

if __name__ == '__main__':
    xml = open('Loss_Reasons_del__c.field-meta.xml').read()
    ob = SFField.from_xml(xml)
    print(ob.to_dot())