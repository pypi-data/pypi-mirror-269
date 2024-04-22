import io

from cbm_files import ProgramFile

from cbm_shell.image_path import ImagePath


class T64ImagePath(ImagePath):
    def __init__(self, drive, entry):
        self.drive = drive
        self.entry = entry
        self.record_len = None

    @property
    def encoded_name(self):
        return self.entry.name

    @property
    def file_type(self):
        return str(self.entry.disk_type)

    @property
    def size_bytes(self):
        return self.entry.end_addr-self.entry.start_addr

    def open(self, mode, ftype=None, record_len=None):
        return io.BytesIO(self.entry.contents())

    def exists(self):
        return True

    def name(self, encoding):
        return self.entry.name.decode(encoding)

    def unique_name(self, encoding):
        if b'~' in self.entry.unique_name and not self.entry.unique_name.endswith(b'~'):
            pos = self.entry.unique_name.index(b'~')
            suffix = self.entry.unique_name[pos:].decode()
            return self.name(encoding)+suffix
        return self.name(encoding)

    def file_info(self, token_set, encoding):
        info = "{}: {}, size={} bytes".format(self.name(encoding), self.file_type, self.size_bytes)
        if self.file_type == 'PRG':
            with self.open('rb') as fileh:
                prg = ProgramFile(fileh, token_set, encoding)
            if prg:
                info += ", start=${:04x}".format(prg.start_addr)

        return info

    def unlink(self):
        raise NotImplementedError("Cannot remove files from .t64 images")
