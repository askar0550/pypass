import os.path
import sqlite3 as sql
from time import gmtime, strftime
import privy


class Db03:
    """Database and encryption"""
    def __init__(self, user, passd):
        self.user = user
        self.key = user+passd
        self.passd = passd
        # self.secc = 3
        self.path = "C:\\Users\\Public\\vault.db"
        self.now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.lvl = 10
        Db03.accounttable(self)
    def checker(self):
        """Create DB file."""
        returnstring = False
        if not os.path.exists(self.path):
            conn = sql.connect(self.path)
            conn.close()
            returnstring = True

        return returnstring

    def accounttable(self):
        """First time table set"""
        with sql.connect(self.path) as conn:
            c_4 = conn.cursor()
            c_1 = conn.cursor()
            maintable = c_1.execute("SELECT CASE WHEN tbl_name = \"UsersMaster\" THEN"+
                                    " 1 ELSE 0 END FROM sqlite_master WHERE"+
                                    " tbl_name = \"UsersMaster\" AND type = \"table\"")
            if maintable.fetchone() is None:
                c_4.execute("CREATE TABLE UsersMaster (Account " +
                            "TEXT PRIMARY KEY, Pass TEXT, lvl INTEGER, Datel TEXT)")
                c_4.execute("INSERT INTO UsersMaster (Account, Pass,"+
                            " lvl, Datel) VALUES (?, ?, 1, ?)", \
                            ("admin", privy.hide(b'pasword', \
                                b'adminpasword', 3, salt=None, server=False), self.now))

    def adduser(self):
        """Add user"""
        try:
            with sql.connect(self.path) as conn:
                c_2 = conn.cursor()

                c_2.execute("INSERT INTO UsersMaster (Account, Pass,"+
                            " lvl, Datel) VALUES (?, ?, 0, ?)", \
                            (self.user, Db03.hashcreator(self, self.passd), self.now))
                conn.commit()
                c_2.close()
                return "User created!"
        except sql.Error:
            return "User exists!"

    def checkuser(self):
        """Add user"""

        with sql.connect(self.path) as conn:
            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select Account, Pass, lvl"+
                                    " FROM UsersMaster WHERE Account =?", (self.user,))

                temp = query.fetchone()
                hashs = temp[1]
                lvl = temp[2]
                mssgg = ""
                try:
                    genn = (privy.peek(hashs, self.key.encode('utf-8'))).decode('utf-8')
                    if genn == self.passd:
                        mssgg = "Success!"
                        self.lvl = lvl
                except ValueError:
                    mssgg = "Wrong password!"
            except TypeError:
                mssgg = "Unknown user!"
        return mssgg

    def hashcreator(self, toencrypt):
        """Password encryption."""
        return privy.hide(toencrypt.encode('utf-8'), \
            self.key.encode('utf-8'), 3, salt=None, server=False)

    def hashfind(self):
        """return hash"""
        hashh = ""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()
            query = c_3.execute("SELECT Pass FROM UsersMaster WHERE Account = ?", (self.user,))
            hashh = query.fetchone()[0]
            c_3.close()
        return hashh

    def readd(self):
        """Retrieve password."""
        return (privy.peek(Db03.hashfind(self), self.key.encode('utf-8'))).decode('utf-8')

    def accounts(self):
        """Check login details"""
        with sql.connect(self.path) as conn:
            conn.row_factory = lambda cursor, row: row[0]
            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select Account"+
                                    " FROM UsersMaster")
                mssgg = sorted(list(set(query.fetchall())))


            except TypeError:
                mssgg = None
        return mssgg

    def deleterow(self):
        """Delete saved password"""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()
            c_3.execute("DELETE FROM UsersMaster WHERE Account = ?", \
                        (self.user, ))
            c_4 = conn.cursor()
            c_4.execute("DELETE FROM Accounts WHERE Account = ?", \
                        (self.user, ))
            conn.commit()
        mssgg = True
        return mssgg

    def datefind(self):
        """return date"""
        date = ""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()

            query = c_3.execute("SELECT substr(Datel,1,10) FROM UsersMaster WHERE Account =?", \
                                (self.user,))
            date = query.fetchone()[0]

            #c_3.close()
        return date



    def datediff(self):
        """return date"""
        date = ""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()

            query = c_3.execute("SELECT julianday() - julianday(Datel)"+
                                " FROM UsersMaster WHERE Account = ?", \
                                (self.user,))
            date = query.fetchone()[0]

            #c_3.close()
        return date
