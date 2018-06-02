#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, create_engine, bindparam
from sqlalchemy.orm import session
from sqlalchemy.ext.declarative import declarative_base

import os
import sys
from file_util.file_util import File


def search_digests(engine):
    c = engine.connect()
    # size = 500 MB
    size = 500 * 1024 * 1024
    digests = c.execute(
        """select digest as d, count(*) as c from file where size > {0} group by
    digest having count(*) > 1 order by c desc""".format(
            size
        )
    )
    for d, count in digests:
        print("Digest: {}, count {}".format(d, count))


def main(path):
    dburl = os.environ(["DB_URL"])
    engine = create_engine(dburl)
    search_digest(engine)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
