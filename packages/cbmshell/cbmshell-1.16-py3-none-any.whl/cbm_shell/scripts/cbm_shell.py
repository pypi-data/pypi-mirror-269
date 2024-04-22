import argparse
import ast
import glob
import os.path
import shutil
import string
import sys

import petscii_codecs  # noqa: F401
import cmd2
try:
    from cmd2.utils import basic_complete
    compat = True
except ImportError:
    compat = False

from pathlib import Path
from tempfile import NamedTemporaryFile

from cbm_files import BASICFile, DataFile, ProgramFile
from cbm_files.tokensets import token_set_names
from d64 import DiskImage as D64DiskImage

from cbm_shell.disk_image import DiskImage
from cbm_shell.disk_image_path import DiskImagePath
from cbm_shell.image_path import Drive, ImagePath
from cbm_shell.images import Images
from cbm_shell.native_path import NativePath
from cbm_shell.subdirectory import Subdirectory
from cbm_shell.t64_image import T64Image
from cbm_shell.tap_image import TapImage


def is_path(p):
    if isinstance(p, NativePath):
        return not p.is_dir()
    return not isinstance(p, Drive)


class CBMShell(cmd2.Cmd):
    def __init__(self):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        shortcuts.update({'$': 'directory'})
        super().__init__(shortcuts=shortcuts)
        self.prompt = '(cbm) '

        self.encoding = 'petscii-c64en-uc'
        self.token_set = 'basic-v2'
        if compat:
            self.add_settable(cmd2.Settable('encoding', str, 'Text encoding'))
            self.add_settable(cmd2.Settable('token_set', str, 'BASIC tokens'))
        else:
            self.add_settable(cmd2.Settable('encoding', str, 'Text encoding', self))
            self.add_settable(cmd2.Settable('token_set', str, 'BASIC tokens', self))

        self.images = Images()

    def expand_paths(self, files_in):
        ret = []
        for f in files_in:
            if ImagePath.is_image_path(f):
                # drive or path in an image
                drive, path_name = ImagePath.split(f, self.encoding)
                if path_name:
                    image = self.images[drive]
                    expanded = list(image.glob(path_name))
                    if expanded:
                        ret += expanded
                    else:
                        ret.append(image.path(path_name))
                else:
                    # just a drive
                    ret.append(Drive(drive))
            else:
                # local filesystem path
                expanded = os.path.expanduser(f)
                globbed = glob.glob(expanded)
                if globbed:
                    ret += [NativePath(p) for p in globbed]
                else:
                    ret.append(NativePath(expanded))
        return ret

    def src_dest_pairs(self, paths_in, expand_drive=True):
        dest = paths_in[-1]

        if is_path(dest):
            if len(paths_in) != 2:
                # multiple sources
                self.perror("Destination '{!s}' is not a drive or directory".format(dest))
                return None

            src = paths_in[0]
            if not is_path(src):
                # source is a directory or drive
                self.perror("Source '{!s}' is not a path".format(src))
                return None
            return [(src, dest)]

        val = []
        if isinstance(dest, NativePath):
            # destination is a directory
            for src in paths_in[:-1]:
                if isinstance(src, NativePath):
                    if src.is_dir():
                        val += self.src_dest_pairs([p for p in src.iterdir() if p.is_file()]+[dest])
                    else:
                        val.append((src, dest / NativePath(src.name)))
                elif isinstance(src, Drive):
                    if expand_drive:
                        src_image = self.images[src]
                        val += self.src_dest_pairs(list(src_image.expand(b''))+[dest])
                    else:
                        val.append((src, dest))
                else:
                    # source is an image path
                    val.append((src, dest / NativePath(src.name(self.encoding))))
        else:
            # destination is a drive
            image = self.images[dest]
            for src in paths_in[:-1]:
                if isinstance(src, NativePath):
                    if src.is_dir():
                        val += self.src_dest_pairs([p for p in src.iterdir() if p.is_file()]+[dest])
                    else:
                        val.append((src, image.path(src.name_encoded(self.encoding))))
                elif isinstance(src, Drive):
                    if expand_drive:
                        src_image = self.images[src]
                        val += self.src_dest_pairs(list(src_image.expand(b''))+[dest])
                    else:
                        val.append((src, dest))
                else:
                    # source is an image path
                    val.append((src, image.path(src.encoded_name)))

        return val

    attach_parser = argparse.ArgumentParser()
    attach_parser.add_argument('--read-only', action='store_true', help="prevent modifications to image")
    attach_parser.add_argument('image', nargs='+', help="image file name")

    @cmd2.with_argparser(attach_parser)
    def do_attach(self, args):
        """Attach an image to a drive number"""
        mode = 'r' if args.read_only else 'w'
        for path in self.expand_paths(args.image):
            next_drive = self.images.get_free_drive()
            if next_drive is None:
                self.perror("All drives in use")
                return None

            image = None
            if isinstance(path, NativePath):
                path = path.as_path()
                if path.is_file() and DiskImage.is_valid_image(path):
                    image = DiskImage(path, mode, next_drive)
                elif path.is_file() and T64Image.is_valid_image(path):
                    image = T64Image(path, next_drive)
                else:
                    image = TapImage(path, mode, next_drive)
            elif isinstance(path, DiskImagePath) and path.file_type == 'CBM':
                image = Subdirectory(path, next_drive)
            if image:
                self.images[next_drive] = image
                self.poutput("Attached {!s} to {}".format(path, next_drive))
            else:
                self.perror("Cannot attach {!s}".format(path))

    detach_parser = argparse.ArgumentParser()
    detach_parser.add_argument('drive', type=int, nargs='*', help="drive to detach")

    @cmd2.with_argparser(detach_parser)
    def do_detach(self, args):
        """Detach an image from a drive letter"""
        if args.drive:
            drives = args.drive
        else:
            drives = reversed(self.images.all_drives())

        for drive in drives:
            if drive in self.images:
                image = self.images.pop(drive)
                image.close()
                self.poutput("Detached {!s}".format(image))
            else:
                self.perror("Invalid drive: {}". format(drive))

    def do_images(self, args):
        """Display the attached images"""
        if self.images:
            for d in self.images.all_drives():
                ro = 'RW' if self.images[d].writeable else 'RO'
                self.poutput("    {}  {}  {!s}".format(d, ro, self.images[d]))
        else:
            self.poutput("No attached images")

    dir_parser = argparse.ArgumentParser()
    dir_parser.add_argument('drive', nargs='*', help="drive or pattern to list")

    @cmd2.with_argparser(dir_parser)
    def do_directory(self, args):
        """Display directory of a drive"""
        if not args.drive:
            args.drive = [str(d) for d in self.images.all_drives()]

        image = None
        for d in args.drive:
            kwargs = {'encoding': self.encoding}
            if not d[0] in string.digits:
                self.perror("Invalid argument: "+d)
                continue

            kwargs['drive'] = int(d[0])
            if len(d) > 1:
                if d[1] != ':':
                    self.perror("Invalid argument: "+d)
                    continue
                pattern = d[2:].encode(self.encoding)
                if pattern:
                    kwargs['pattern'] = pattern

            if kwargs['drive'] in self.images:
                if image:
                    self.poutput('')
                image = self.images[kwargs['drive']]
                for line in image.directory(**kwargs):
                    self.poutput(line)
            else:
                self.perror("Invalid drive: {}".format(d))

    file_parser = argparse.ArgumentParser()
    file_parser.add_argument('file', nargs='+', help="file")

    @cmd2.with_argparser(file_parser)
    def do_file(self, args):
        """Display information about a file"""
        files = self.expand_paths(args.file)

        for f in files:
            if isinstance(f, Drive):
                self.poutput("Skipping drive {:d}".format(f))
            else:
                self.poutput(f.file_info(self.token_set, self.encoding))

    list_parser = argparse.ArgumentParser()
    list_parser.add_argument('file', nargs='+', help="BASIC program file")
    list_parser.add_argument('--start', type=int, default=0, metavar="LINE", help="starting line number")
    list_parser.add_argument('--end', type=int, default=65535, metavar="LINE", help="ending line number")

    @cmd2.with_argparser(list_parser)
    def do_list(self, args):
        """List contents of a BASIC file"""
        files = self.expand_paths(args.file)

        if len(files) > 1:
            # output to file
            if not isinstance(files[-1], NativePath):
                self.perror("Cannot write listing to image path {!s}".format(files[-1]))
                return None

            path_pairs = self.src_dest_pairs(files, expand_drive=False)

            for src, dest in path_pairs:
                if src.exists():
                    with src.open('rb') as fileh:
                        prg = ProgramFile(fileh, self.token_set, self.encoding)
                    if not isinstance(prg, BASICFile):
                        self.perror("Not a BASIC file: {!s}".format(src))
                        return None
                    with dest.open('w') as fileh:
                        try:
                            for line in prg.to_text(args.start, args.end):
                                print(line, file=fileh)
                        except ValueError as e:
                            self.perror(str(e))
                else:
                    self.perror("File not found, {!s}".format(src))
        else:
            # output to stdout
            for f in files:
                if is_path(f):
                    if f.exists():
                        with f.open('rb') as fileh:
                            prg = ProgramFile(fileh, self.token_set, self.encoding)
                        if not isinstance(prg, BASICFile):
                            self.perror("Not a BASIC file: {!s}".format(f))
                            return None
                        try:
                            for line in prg.to_text(args.start, args.end):
                                self.poutput(line)
                        except ValueError as e:
                            self.perror(str(e))
                    else:
                        self.perror("File not found, {!s}".format(f))
                else:
                    self.poutput("Skipping non-file path {!s}".format(f))

    def hex_int(v):
        return int(v, 0)

    unlist_parser = argparse.ArgumentParser()
    unlist_parser.add_argument('--start', dest='start_addr', type=hex_int, default=0x1201, help="Program start address")
    unlist_parser.add_argument('--type', dest='file_type', default='PRG_RELOC', help="DOS file type")
    unlist_parser.add_argument('file', nargs=(2,), help="file source or destination")

    @cmd2.with_argparser(unlist_parser)
    def do_unlist(self, args):
        """Convert text file to BASIC"""
        files = self.expand_paths(args.file)
        path_pairs = self.src_dest_pairs(files)

        for src, dest in path_pairs:
            self.poutput("Writing {!s} to {!s}".format(src, dest))
            prog = BASICFile(None, start_addr=args.start_addr, token_set=self.token_set, encoding=self.encoding)
            with src.open('r') as in_file:
                try:
                    prog.from_text(in_file)
                except ValueError as e:
                    self.perror(str(e))
                    return None
            with dest.open('wb', ftype=args.file_type) as out_file:
                for line in prog.to_binary():
                    out_file.write(line)

    edit_parser = argparse.ArgumentParser()
    edit_parser.add_argument('file', help="file to edit")

    @cmd2.with_argparser(edit_parser)
    def do_edit(self, args):
        """Edit BASIC program"""
        file_path = self.expand_paths([args.file])[0]

        with file_path.open('rb') as fileh:
            prg = ProgramFile(fileh, self.token_set, self.encoding)
        if not isinstance(prg, BASICFile):
            self.perror("Not a BASIC file: {!s}".format(file_path))
            return None

        with NamedTemporaryFile(mode='w+', buffering=1, prefix="edit-") as tmph:
            for line in prg.to_text():
                print(line, file=tmph)

            self.run_editor(tmph.name)
            tmph.seek(0)
            prg = BASICFile(None, prg.start_addr, self.token_set, self.encoding)
            prg.from_text(tmph)

        with file_path.open('wb') as fileh:
            for line in prg.to_binary():
                fileh.write(line)

    merge_parser = argparse.ArgumentParser()
    merge_parser.add_argument('file', help="file to update")
    merge_parser.add_argument('add_file', nargs='+', help="file to merge")

    @cmd2.with_argparser(merge_parser)
    def do_merge(self, args):
        """Merge one or more BASIC programs"""
        file_path = self.expand_paths([args.file])[0]
        merge_files = self.expand_paths(args.add_file)

        self.poutput("Reading {!s}".format(file_path))
        with file_path.open('rb') as fileh:
            prg = ProgramFile(fileh, self.token_set, self.encoding)
        if not isinstance(prg, BASICFile):
            self.perror("Not a BASIC file: {!s}".format(file_path))
            return None

        for merge_path in merge_files:
            self.poutput("Merging {!s}".format(merge_path))
            with merge_path.open('rb') as fileh:
                merge_prg = ProgramFile(fileh, self.token_set, self.encoding)
                if not isinstance(merge_prg, BASICFile):
                    self.perror("Not a BASIC file: {!s}".format(merge_path))
                    return None

                prg.merge(merge_prg)

        self.poutput("Writing {!s}".format(file_path))
        with file_path.open('wb') as fileh:
            for line in prg.to_binary():
                fileh.write(line)

    renumber_parser = argparse.ArgumentParser()
    renumber_parser.add_argument('file', help="file to renumber")
    renumber_parser.add_argument('--start', type=int, default=10, metavar="LINE", help="starting line number")
    renumber_parser.add_argument('--increment', type=int, default=10, metavar="NUM", help="line number increment")
    renumber_parser.add_argument('--region-start', type=int, metavar="LINE", help="start of region")
    renumber_parser.add_argument('--region-end', type=int, metavar="LINE", help="end of region")

    @cmd2.with_argparser(renumber_parser)
    def do_renumber(self, args):
        """Renumber lines in a BASIC program"""
        file_path = self.expand_paths([args.file])[0]

        self.poutput("Reading {!s}".format(file_path))
        with file_path.open('rb') as fileh:
            prg = ProgramFile(fileh, self.token_set, self.encoding)
        if not isinstance(prg, BASICFile):
            self.perror("Not a BASIC file: {!s}".format(file_path))
            return None

        if args.region_start is None and args.region_end is None:
            self.poutput("Renumbering starting at {}, increments of {}".format(args.start, args.increment))
        else:
            self.poutput("Renumbering lines {}-{} starting at {}, increments of {}".format(args.region_start, args.region_end, args.start, args.increment))
        try:
            prg = prg.renumber(args.start, args.increment, args.region_start, args.region_end)
        except ValueError as e:
            self.perror(str(e))
            return None

        self.poutput("Writing {!s}".format(file_path))
        with file_path.open('wb') as fileh:
            for line in prg.to_binary():
                fileh.write(line)

    text_parser = argparse.ArgumentParser()
    text_parser.add_argument('file', nargs='+', help="Data (SEQ) file")

    @cmd2.with_argparser(text_parser)
    def do_text(self, args):
        """Display contents of data file"""
        files = self.expand_paths(args.file)

        if len(files) > 1:
            # output to file
            if not isinstance(files[-1], NativePath):
                self.perror("Cannot write text to image path {!s}".format(files[-1]))
                return None

            path_pairs = self.src_dest_pairs(files, expand_drive=False)

            for src, dest in path_pairs:
                if src.exists():
                    with src.open('rb') as fileh:
                        seq = DataFile(fileh, self.encoding)
                    with dest.open('w') as fileh:
                        for line in seq.to_text():
                            print(line, file=fileh)
                else:
                    self.perror("File not found, {!s}".format(src))
        else:
            # output to stdout
            for f in files:
                if is_path(f):
                    if f.exists():
                        with f.open('rb') as fileh:
                            seq = DataFile(fileh, self.encoding)
                        for line in seq.to_text():
                            self.poutput(line)
                    else:
                        self.perror("File not found, {!s}".format(f))
                else:
                    self.poutput("Skipping non-file path {!s}".format(f))

    untext_parser = argparse.ArgumentParser()
    untext_parser.add_argument('--type', dest='file_type', default='SEQ', help="DOS file type")
    untext_parser.add_argument('--record-length', type=int, help="REL file record length")
    untext_parser.add_argument('file', nargs=(2,), help="file source or destination")

    @cmd2.with_argparser(untext_parser)
    def do_untext(self, args):
        """Convert text file to data file"""
        if args.file_type == 'REL' and args.record_length is None:
            self.perror("Record length must be defined for REL files")
            return None

        files = self.expand_paths(args.file)
        path_pairs = self.src_dest_pairs(files)

        for src, dest in path_pairs:
            self.poutput("Writing {!s} to {!s}".format(src, dest))
            seq = DataFile(None, encoding=self.encoding)
            with src.open('r') as in_file:
                seq.from_text(in_file)
            with dest.open('wb', ftype=args.file_type, record_len=args.record_length) as out_file:
                for line in seq.to_binary():
                    out_file.write(line)

    copy_parser = argparse.ArgumentParser()
    copy_parser.add_argument('--type', dest='file_type', help="DOS file type")
    copy_parser.add_argument('--record-length', type=int, help="REL file record length")
    copy_parser.add_argument('file', nargs=(2,), help="file source or destination")

    @cmd2.with_argparser(copy_parser)
    def do_copy(self, args):
        """Copy files between images"""
        if args.file_type == 'REL' and args.record_length is None:
            self.perror("Record length must be defined for REL files")
            return None

        files = self.expand_paths(args.file)
        path_pairs = self.src_dest_pairs(files)

        for src, dest in path_pairs:
            if src.exists():
                src_ftype = src.file_type if src.file_type else None
                ftype = args.file_type if args.file_type else src_ftype
                record_len = args.record_length if args.record_length else src.record_len
                self.poutput("Copying {!s} to {!s}".format(src, dest))
                with src.open('rb') as in_file:
                    with dest.open('wb', ftype=ftype, record_len=record_len) as out_file:
                        shutil.copyfileobj(in_file, out_file)
            else:
                self.perror("File not found, {!s}".format(src))
                break

    rename_parser = argparse.ArgumentParser()
    rename_parser.add_argument('old_file', help="existing file")
    rename_parser.add_argument('new_file', help="new name")

    @cmd2.with_argparser(rename_parser)
    def do_rename(self, args):
        """Rename file in an image"""
        old_path = self.expand_paths([args.old_file])[0]
        new_path = self.expand_paths([args.new_file])[0]

        if not isinstance(old_path, DiskImagePath):
            self.perror("Not an image path, {!s}".format(old_path))
            return None
        if old_path.exists():
            if isinstance(new_path, NativePath):
                new_name = new_path.name_encoded(self.encoding)
            elif isinstance(new_path, DiskImagePath):
                new_name = new_path.encoded_name
            else:
                self.perror("Invalid new name, {!s}".format(new_path))
                return None
            self.poutput("Renaming {!s} to {!s}".format(old_path, new_name))
            old_path._path.entry.name = new_name
        else:
            self.perror("File not found, {!s}".format(old_path))

    delete_parser = argparse.ArgumentParser()
    delete_parser.add_argument('file', nargs='+', help="file to delete")

    @cmd2.with_argparser(delete_parser)
    def do_delete(self, args):
        """Delete files"""
        files = self.expand_paths(args.file)

        for path in files:
            if is_path(path):
                self.poutput("Deleting {!s}".format(path))
                try:
                    path.unlink()
                except (FileNotFoundError, NotImplementedError) as e:
                    self.perror(str(e))
            else:
                self.poutput("Skipping {!s}".format(path))

    def do_token_set(self, args):
        """List supported BASIC token sets"""
        for name in token_set_names():
            if not name.startswith('escape-'):
                self.poutput(name)

    mkdir_parser = argparse.ArgumentParser()
    mkdir_parser.add_argument('name', help="subdirectory name")
    mkdir_parser.add_argument('id', help="subdirectory identifier")
    mkdir_parser.add_argument('start_track', type=int, help="starting track")
    mkdir_parser.add_argument('num_blocks', type=int, help="number of blocks")

    @cmd2.with_argparser(mkdir_parser)
    def do_mkdir(self, args):
        """Create a subdirectory (1581 image only)"""
        subdir_path = self.expand_paths([args.name])[0]

        if not isinstance(subdir_path, DiskImagePath):
            self.perror("Not a disk image path, {!s}".format(subdir_path))
            return None

        self.poutput("Creating {!s}".format(subdir_path))
        image = self.images[subdir_path.drive]
        part = image.create_partition(subdir_path.encoded_name, args.start_track, args.num_blocks)
        part.format(subdir_path.encoded_name, args.id.encode(self.encoding))

    lock_parser = argparse.ArgumentParser()
    lock_parser.add_argument('file', nargs='+', help="file to lock")

    @cmd2.with_argparser(lock_parser)
    def do_lock(self, args):
        """Protect files in image from deletion"""
        files = self.expand_paths(args.file)

        for f in files:
            if isinstance(f, DiskImagePath):
                self.poutput("Locking {!s}".format(f))
                f.lock()
            else:
                self.poutput("Skipping {!s}".format(f))

    unlock_parser = argparse.ArgumentParser()
    unlock_parser.add_argument('file', nargs='+', help="file to lock")

    @cmd2.with_argparser(unlock_parser)
    def do_unlock(self, args):
        """Allow files in image to be deleted"""
        files = self.expand_paths(args.file)

        for f in files:
            if isinstance(f, DiskImagePath):
                self.poutput("Unlocking {!s}".format(f))
                f.unlock()
            else:
                self.poutput("Skipping {!s}".format(f))

    cat_parser = argparse.ArgumentParser()
    cat_parser.add_argument('file', help="file to output")

    @cmd2.with_argparser(cat_parser)
    def do_cat(self, args):
        """Output the contents of a file"""
        file_path = self.expand_paths([args.file])[0]

        if file_path.exists():
            with file_path.open('rb') as in_file:
                sys.stdout.buffer.write(in_file.read())
        else:
            self.perror("File not found, {!s}".format(file_path))

    from_petscii_parser = argparse.ArgumentParser()
    from_petscii_parser.add_argument('string', help="PETSCII string to convert")

    @cmd2.with_argparser(from_petscii_parser)
    def do_from_petscii(self, args):
        """Convert string from PETSCII to Unicode"""

        bstr = ast.literal_eval(args.string)
        self.poutput(bstr.decode(self.encoding))

    to_petscii_parser = argparse.ArgumentParser()
    to_petscii_parser.add_argument('string', help="Unicode string to convert")

    @cmd2.with_argparser(to_petscii_parser)
    def do_to_petscii(self, args):
        """Convert string from Unicode to PETSCII"""
        self.poutput(args.string.encode(self.encoding))

    format_parser = argparse.ArgumentParser()
    format_parser.add_argument('label', help='disk label')
    format_parser.add_argument('id', help='disk identifier')
    format_parser.add_argument('filename', type=Path, help='image filename')
    format_parser.add_argument('--type', default='d64', choices=D64DiskImage.supported_types(), help='image type')
    format_parser.add_argument('--force', action='store_true', help='overwrite existing image')

    @cmd2.with_argparser(format_parser)
    def do_format(self, args):
        """Create an empty disk image."""
        if args.filename.exists():
            if args.force:
                args.filename.unlink()
            else:
                self.perror("{!s} already exists".format(args.filename))
                return None

        self.poutput("Creating empty disk image as {!s}, {}:{}, type {}".format(args.filename, args.label, args.id, args.type))
        D64DiskImage.create(args.type, args.filename, args.label.encode(self.encoding), args.id.encode(self.encoding))

    def image_path_complete(self, text, line, begidx, endidx):
        """Path expansion for a file in an image."""
        if ImagePath.is_image_path(text):
            try:
                drive, name = ImagePath.split(text, self.encoding)
                all_paths = self.images[drive].expand(name)
                choices = ["{}:{!s}".format(drive, p.unique_name(self.encoding)) for p in all_paths]
                if hasattr(self, 'basic_complete'):
                    return self.basic_complete(text, line, begidx, endidx, choices)
                return basic_complete(text, line, begidx, endidx, choices)
            except (KeyError, UnicodeEncodeError):
                pass
        return []

    complete_lock = image_path_complete
    complete_unlock = image_path_complete

    def native_image_path_complete(self, text, line, begidx, endidx):
        """Path expansion for a local file or a file in an image."""
        image_complete = self.image_path_complete(text, line, begidx, endidx)
        if image_complete:
            return image_complete

        return self.path_complete(text, line, begidx, endidx)

    complete_attach = native_image_path_complete
    complete_file = native_image_path_complete
    complete_list = native_image_path_complete
    complete_unlist = native_image_path_complete
    complete_edit = native_image_path_complete
    complete_merge = native_image_path_complete
    complete_renumber = native_image_path_complete
    complete_text = native_image_path_complete
    complete_untext = native_image_path_complete
    complete_copy = native_image_path_complete
    complete_rename = native_image_path_complete
    complete_delete = native_image_path_complete
    complete_lock = image_path_complete
    complete_unlock = image_path_complete
    complete_cat = native_image_path_complete


def main():
    c = CBMShell()
    ret = c.cmdloop()

    # close any attached images
    c.images.cleanup()

    sys.exit(ret)
