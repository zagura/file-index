#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, create_engine, bindparam
from sqlalchemy.orm import session
from sqlalchemy.ext.declarative import declarative_base
import os
import sys
from file_util.file_util import File


def main():
    """
    ENV DB_URL for access url to DB
    """
    dburl = os.environ(["DB_URL"])
    engine = create_engine(dburl)
    c = engine.connect()
    if not engine.dialect.has_table(engine, "file"):
        c.execute(
            """create table file (
            path varchar(4096) not null,
            name varchar(4096) not null,
            device varchar(256),
            digest(64) not null,
            inode bigint,
            size bigint,
            constraint file_pk PRIMARY KEY file(path, name));
        """
        )
        c.execute("""create index file_idx on file(digest);""")
    else:
        print("Table exists")
    c.close()


if __name__ == "__main__":
    main()
