from munge.base import CodecBase

try:
    import MySQLdb
    import MySQLdb.cursors

except ImportError:
    pass

from urllib.parse import urlsplit


class MysqlEndpoint:
    def __init__(self, cxn, database, table):
        self.database = database
        self.table = table
        self.cxn = cxn


class Mysql(CodecBase):
    supports_list = True

    extensions = ["mysql"]
    __kwargs = {}

    def set_type(self, name, typ):
        if name == "dict":
            self.__kwargs["object_pairs_hook"] = typ

    def open(self, url, mode="r", stdio=True):
        res = urlsplit(url)
        print("opening ", url)
        (db, sep, table) = res.path.strip("/").partition("/")

        fobj = MysqlEndpoint(
            MySQLdb.connect(
                host=res.hostname,
                user=res.username,
                passwd=res.password,
                cursorclass=MySQLdb.cursors.DictCursor,
            ),
            database=db,
            table=table,
        )
        #        cursor = db.cursor()
        #        cursor.execute(query)
        #        res = cursor.fetchall()
        return fobj

    # native mysql connection
    def load(self, fobj):
        cursor = fobj.cxn.cursor()
        cursor.execute(f"select * from {fobj.database}.{fobj.table}")
        return cursor.fetchall()

    def loads(self, instr):
        raise NotImplementedError()

    def dump(self, data, fobj):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()
