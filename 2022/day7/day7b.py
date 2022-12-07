# Notes
# Build a dir tree from a list of commands and output
# Directories have no size
# Need to free up space: 40000000

import dataclasses
from typing import Dict, Optional


test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


@dataclasses.dataclass
class Dir:
    name: str
    subdirs: Dict[str, 'Dir']
    files: Dict[str, int]
    parent: Optional['Dir']

    def rsize(self):
        rsize = sum(self.files.values())
        for subdir in self.subdirs.values():
            rsize += subdir.rsize()
        return rsize

    def resolved(self):
        if self.parent:
            return self.parent.resolved() + '/' + self.name
        return ''


def build_tree(commands):
    root = Dir('/', {}, {}, parent=None)
    current_dir = root
    current_dir_name = root.name
    for line in commands:
        line = line.replace('\n', '')
        if line.startswith('$ cd'):
            # CD Command
            if line == '$ cd ..':
                # Done with this dir, go up
                current_dir = current_dir.parent
                current_dir_name = current_dir.name
            else:
                current_dir_name = line[5:]
                current_dir = current_dir.subdirs[current_dir_name]
        elif line.startswith('$ ls'):
            # LS command
            pass
        elif line.startswith('dir'):
            # New directory found
            _, dirname = line.split(' ')
            current_dir.subdirs[dirname] = Dir(dirname, {}, {}, parent=current_dir)
        else:
            # New file found
            filesize, filename = line.split(' ')
            current_dir.files[filename] = int(filesize)

    return root


def list_dirs(root):
    all_dirs = list(root.subdirs.values())
    for dir in root.subdirs.values():
        all_dirs.extend(list_dirs(dir))
    return all_dirs


def find_closest_to(dirs, value):
    closest = None
    closest_off_by = None
    for dir in dirs:
        rsize = dir.rsize()
        if rsize > value:
            off_by = rsize - value
            if not closest_off_by or closest_off_by > off_by:
                closest = dir
                closest_off_by = off_by
    return closest


needed = 40000000

root = build_tree(test_input.splitlines(keepends=False)[1:])
used = root.rsize()
to_free = used - needed
print(f'{used=}, {to_free=}')
dir = find_closest_to(list_dirs(root), to_free)
print(f'{dir.resolved()}: {dir.rsize()}')

root = build_tree(open('day7-input.txt').readlines()[1:])
used = root.rsize()
to_free = used - needed
print(f'{used=}, {to_free=}')
dir = find_closest_to(list_dirs(root), to_free)
print(f'{dir.resolved()}: {dir.rsize()}')
