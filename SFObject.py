import itertools
import os
from dataclasses import dataclass
from typing import Iterable

from .SFField import Lookup, SFField


@dataclass
class SFObject:
    name: str
    fields: Iterable[SFField]

    @classmethod
    def from_folder(cls, name: str, folder_path: str):
        return SFObject(name, SFField.from_folder(os.path.join(folder_path, 'fields')))

    def to_dot(self, indent: str = '    ') -> str:
        self.fields, fields = itertools.tee(self.fields) # pretty much equivalent to calling `.clone()` on an iterator
        return f"""{self.name} [shape=none, label=<
<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">
{indent}<TR><TD BORDER="1">{self.name}</TD></TR>
""" + f'\n{indent}'.join(map(lambda field: field.to_dot(), fields)) + '\n</TABLE> >];'
    
    def get_linking_fields(self) -> Iterable[SFField]:
        yield from filter(lambda field: isinstance(field.dtype, Lookup), self.fields)