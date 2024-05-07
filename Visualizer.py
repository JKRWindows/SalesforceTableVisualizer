import os
from dataclasses import dataclass
from functools import cache
from typing import Iterable

from .SFField import Lookup
from .SFObject import SFObject


@dataclass
class SFVisualizer:
    folder: str
    branch_name: str = 'main'

    @cache
    def get_objects(self) -> Iterable[SFObject]:
        if 'force-app' not in os.listdir(self.folder):
            raise ValueError(f'Couldn\'t locate the "force-app" directory.\nMake sure you run this script in the main directory of your Salesforce app.')
        if self.branch_name not in os.listdir(os.path.join(self.folder, 'force-app')):
            raise ValueError(f'Couldn\'t locate branch "{self.branch_name}" in the force-app dir.')
        f = os.path.join(self.folder, 'force-app', 'main', 'default', 'objects')
        return map(lambda folder: SFObject.from_folder(folder, os.path.join(f, folder)), f)
    
    def get_links(self) -> Iterable[str]:
        yield from (f'{obj.name}:{link.full_name} -> {link.dtype.reference_to}' for obj in self.get_objects() for link in obj.get_linking_fields() if isinstance(link.dtype, Lookup))

    def to_dot(self, indent: str = '    ') -> str:
        return f"""digraph {"{"}
{indent}ordering="out";
{indent}overlap=false;

{indent}""" + f'\n{indent}'.join(map(lambda x: x.to_dot(indent), self.get_objects())) + f"""

{indent}""" + f'\n{indent}'.join(self.get_links()) + f"""
{"}"}"""
