#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, create_engine, bindparam
from sqlalchemy.orm import session
from sqlalchemy.ext.declarative import declarative_base
import os
import sys
from file_util.file_util import File


def db_conn(dburl):
    engine = create_engine(dburl)
    return engine


def search_path(pathname, engine):
    for dirname, subdirs, files in os.walk(pathname):
        for fname in files:
            print("[Debug]: path: {0}, fname: {1}".format(dirname, fname))
            f = File(fname, dirname)
            f.save(engine)


def main(path):
    dburl = os.environ(["DB_URL"])
    engine = create_engine(dburl)
    search_path(path, engine)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
