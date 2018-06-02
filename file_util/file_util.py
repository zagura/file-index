#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha256
import os
import stat

Base = declarative_base()


class File(Base):

    __tablename__ = "file"
    name = Column(String, primary_key=True)
    path = Column(String, primary_key=True)
    size = Column(BigInteger)
    inode = Column(BigInteger)
    device = Column(String)
    digest = Column(String)

    def __init__(self, name, path, device=None):
        try:
            print("[DEBUG]: {0} {1}".format(path, name))
            self.name = name
            self.path = path
            self.device = device
            mode = self.get_stat().st_mode
            if stat.S_ISREG(mode):
                self.get_digest()
            else:
                self.digest = sha256(b"").hexdigest()
        except Exception as e:
            print("Exception {}".format(str(e)))
        if not self.digest:
            self.digest = sha256(b"").hexdigest()

    def save(self, engine):
        session = Session(bind=engine)
        session.add(self)
        session.commit()

    def get_digest(self):
        fullname = os.path.join(self.path, self.name)
        digest = sha256()
        with open(fullname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                digest.update(chunk)
        self.digest = digest.hexdigest()

    def get_stat(self):
        stats = os.stat(os.path.join(self.path, self.name))
        self.inode = stats.st_ino
        self.device = stats.st_dev
        self.size = stats.st_size
        return stats


if __name__ == "__main__":
    pass
