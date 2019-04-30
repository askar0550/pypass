"""Complete."""
# import os.path
import sqlite3 as sql
from time import gmtime, strftime
import privy




class Db02:
    """File and encryption"""
    def __init__(self, account, host, user, passd, key):
        self.account = account
        self.host = host
        self.user = user
        self.key = account+key
        self.passd = passd
        self.now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # self.secc = 3
        self.path = "C:\\Users\\Public\\vault.db"
        Db02.usertable(self)
        # self.row = Doc01.filecheck(self)



    def usertable(self):
        """First time table set"""
        with sql.connect(self.path) as conn:
            c_4 = conn.cursor()
            c_1 = conn.cursor()
            maintable = c_1.execute("SELECT CASE WHEN tbl_name = \"Accounts\" THEN"+
                                    " 1 ELSE 0 END FROM sqlite_master WHERE"+
                                    " tbl_name = \"UsersMaster\" AND type = \"table\"")
            if maintable.fetchone() is None:
                c_4.execute("CREATE TABLE Accounts (Account " +
                            "TEXT,acc_host TEXT, acc_user TEXT, acc_pass TEXT, Datel TEXT)")





    def usercheck(self):
        """Check the user unicity being aware of host name."""
        with sql.connect(self.path) as conn:
            # Db02.usertable(self)
            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select Account, acc_host, acc_user, acc_pass"+
                                    " FROM Accounts WHERE Account =? and acc_host =?" +
                                    " and acc_user =?", (self.account, self.host, self.user))

                if query.fetchone():
                    mssgg = 1
                else:
                    mssgg = 0

            except TypeError:
                mssgg = 0
        return mssgg



    def hosts(self):
        """retrieve all saved hosts for the host dropdown"""
        with sql.connect(self.path) as conn:
            conn.row_factory = lambda cursor, row: row[0]

            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select acc_host"+
                                    " FROM Accounts WHERE Account =?",\
                                     (self.account,))

                mssgg = sorted(list(set(query.fetchall())))

            except TypeError:
                mssgg = None
        return mssgg

    def accounts(self, hosst):
        """retrive list of accounts in specific host"""
        with sql.connect(self.path) as conn:
            conn.row_factory = lambda cursor, row: row[0]

            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select acc_user"+
                                    " FROM Accounts WHERE Account =?" +
                                    "AND acc_host=?",\
                                     (self.account, hosst))

                mssgg = sorted(list(set(query.fetchall())))


            except TypeError:
                mssgg = None
        return mssgg

    def write(self):
        """Writes in file and save."""
        with sql.connect(self.path) as conn:
            # Db02.usertable(self)
            c_2 = conn.cursor()
            mssgg = ""
            try:
                c_2.execute("INSERT INTO Accounts (Account, acc_host, acc_user, acc_pass, Datel)"+
                            " VALUES (?, ?, ?, ?, ?)", \
                            (self.account, self.host, self.user,\
                             Db02.hashcreator(self, self.passd), self.now))
                conn.commit()
                mssgg = format(Db02.jewls(self)) + " passwords in vault"
            except TypeError:
                mssgg = "No account"

        return mssgg

    def jewls(self):
        """check account vault size"""
        with sql.connect(self.path) as conn:
            # Db02.usertable(self)
            c_2 = conn.cursor()
            try:
                query = c_2.execute("Select count(*)"+
                                    " FROM Accounts WHERE Account =?", (self.account,))

                temp = query.fetchone()
                mssgg = format(temp[0])
            except TypeError:
                mssgg = "0"
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

            query = c_3.execute("SELECT acc_pass FROM Accounts WHERE Account = ?"+
                                "AND acc_host =? AND acc_user=?", \
                                (self.account, self.host, self.user))
            hashh = query.fetchone()[0]

            #c_3.close()
        return hashh

    def datefind(self):
        """return date"""
        date = ""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()

            query = c_3.execute("SELECT substr(Datel,1,10) FROM Accounts WHERE Account = ?"+
                                "AND acc_host =? AND acc_user=?", \
                                (self.account, self.host, self.user))
            date = query.fetchone()[0]

            #c_3.close()
        return date

    def datediff(self):
        """return date"""
        date = ""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()

            query = c_3.execute("SELECT julianday() - julianday(Datel)"+
                                " FROM Accounts WHERE Account = ?"+
                                "AND acc_host =? AND acc_user=?", \
                                (self.account, self.host, self.user))
            date = query.fetchone()[0]

            #c_3.close()
        return date

    def readd(self):
        """Retrieve password."""
        return (privy.peek(Db02.hashfind(self), self.key.encode('utf-8'))).decode('utf-8')

    def updatepss(self):
        """Update the password"""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()
            c_3.execute("UPDATE Accounts SET acc_pass=?, Datel=? WHERE Account = ?"+
                        "AND acc_host =? AND acc_user=?", \
                        (Db02.hashcreator(self, self.passd), self.now, \
                        self.account, self.host, self.user))
            conn.commit()
        mssgg = True
        return mssgg



    def deleterow(self):
        """Delete saved password"""
        with sql.connect(self.path) as conn:
            c_3 = conn.cursor()
            c_3.execute("DELETE FROM Accounts WHERE Account = ?"+
                        "AND acc_host =? AND acc_user=?", \
                        (self.account, self.host, self.user))
            conn.commit()
        mssgg = True
        return mssgg
