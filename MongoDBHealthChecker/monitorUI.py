'''
@author: edward pullum
'''
from tkinter import *
import dbConnection as db
from pprint import *
import psutil
import os

class Gui:
    
    # The init creates the buttons, entry, labels, and text box
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.log = "/Users/edwardpullum/mongodb/mongodb.log"

        
        #Top label to show application name an grid position
        self.titleLabel = Label(
                                    frame,
                                    text="MongoDB Health Checker",
                                    font=("Courier", 44)
                                    )
        self.titleLabel.grid(
                        row=0,
                        column=0,
                        columnspan = 10
                        )
        
        self.txtEntry = Entry(frame)
        self.txtEntry.grid(
                            row=1,
                            columnspan=2)
        
        self.dbButton = Button(
                                    frame,
                                    text="Database List",
                                    command=self.getDatabase
                                    )
        self.dbButton.grid(
                            row=2,
                            column=0,
                            sticky=N+S+E+W
                            )
        
        self.dbButton = Button(
                                    frame,
                                    text="Collation List",
                                    command=self.getCollection
                                    )
        self.dbButton.grid(
                            row=2,
                            column=1,
                            sticky=N+S+E+W
                            )
        
        
        
        self.lastErrorButton = Button(
                                        frame,
                                        text="Last DB Error",
                                        command=self.dbLastError
                                        )
        self.lastErrorButton.grid(
                                row=3,
                                sticky=N+S+E+W
                                )
        
        self.buildInfoButton = Button(
                                        frame,
                                        text="Build Info",
                                        command=self.dbBuildInfo
                                        )
        self.buildInfoButton.grid(
                                    row=3,
                                    column=1,
                                    sticky=N+S+E+W
                                    )
        
        self.cpuUsageButton = Button(
                                        frame,
                                        text="CPU Usage",
                                        command=self.cpuUsage
                                        )
        self.cpuUsageButton.grid(
                                    row=4,
                                    column=0,
                                    sticky=N+W+E+S
                                    )
        self.memUsageButton = Button(
                                        frame,
                                        text="Memory Usage",
                                        command=self.getMemUsage
                                        )
        self.memUsageButton.grid(
                                    row=4,
                                    column=1,
                                    sticky=N+E+W+S
                                    )
        
        
        self.dbStatsButton = Button(
                                    frame,
                                    text="DB Stats",
                                    command=self.getDBStats
                                    )
        self.dbStatsButton.grid(
                                row=5,
                                column=0,
                                sticky=N+E+W+S
                                )
        
        self.collStatsButton = Button(
                                        frame,
                                        text="Collation Stats",
                                        command=self.getCollStats
                                        )
        self.collStatsButton.grid(
                                    row=5,
                                    column=1,
                                    sticky=N+E+W+S
                                    )
        
        
        self.statementButton = Button(
                                        frame,
                                        text="Statment Count",
                                        command=self.getStatementCount
                                        )
        self.statementButton.grid(
                                    row=6,
                                    sticky=N+E+W+S
                                    )
        
        self.connectionCountButton = Button(
                                            frame,
                                            text="Connection Count",
                                            command=self.connectionCount
                                            )
        self.connectionCountButton.grid(
                                        row=7,
                                        column=0,
                                        sticky=N+E+W+S
                                        )
        
        self.viewConnectionsButtons = Button(
                                                frame,
                                                text="View Connections",
                                                command=self.viewConnection
                                                )
        self.viewConnectionsButtons.grid(
                                        row=7,
                                        column=1,
                                        sticky=N+E+W+S
                                        )
        
        self.viewLogFileButton = Button(
                                            frame,
                                            text="View Logs",
                                            command=self.getLogs
                                            )
        self.viewLogFileButton.grid(
                                    row=6,
                                    column=1,
                                    sticky=N+E+W+S
                                    )
        
        
        
        
        self.exitButton = Button(
                                    frame,
                                    text="Exit",
                                    command=exit
                                    )
        self.exitButton.grid(
                                row=8,
                                columnspan=2,
                                sticky=N+E+W+S
                                )
        
        
        
        
        self.txtBox = Text(
                            frame,
                            width=100,
                            height=20,
                            wrap=WORD,
                            highlightbackground="grey",)
        self.txtBox.grid(
                            row=1,
                            column=5,
                            columnspan=10,
                            rowspan=10
                            )
        
    def getDatabase(self):
        self.txtBox.delete(1.0, END)
        connect = db.Database()
        dbList = connect.getDatabases()
        self.txtBox.delete('1.0', END)
        for datab in dbList:
            self.txtBox.insert(0.0, datab+"\n")
            
    def getCollection(self):
        self.txtBox.delete(1.0, END)
        if not self.entryEmpty():
            connect = db.Database()
            collectionList = connect.getCollections(self.txtEntry.get())
            self.txtBox.delete(1.0, END)
            for coll in collectionList:
                self.txtBox.insert(0.0, coll+"\n")
        else:
            txt = "Please provide a Database to see all the collections."
            self.txtBox.insert(0.0, txt)
    
    def dbLastError(self):
        connect = db.Database()
        if not self.entryEmpty():
            lastError = connect.getLastError(self.txtEntry.get())
            fromated = pformat(lastError)
            self.txtBox.delete(1.0, END)
            self.txtBox.insert(0.0, fromated)
        else:
            txt = "Please provide a Database to see all the last Error."
            self.txtBox.insert(0.0, txt)
        
    def dbBuildInfo(self):
        connect = db.Database()
        if not self.entryEmpty():
            buildinfo = connect.getBuildinfo(self.txtEntry.get())
            self.txtBox.delete(1.0, END)
            self.txtBox.insert(0.0, pformat(buildinfo))
        else:
            txt = "Please provide a Database to see the build info."
            self.txtBox.insert(0.0, txt)
        
    def cpuUsage(self):
        processId = os.popen("pgrep mongo").read()
        processNum = processId.strip('\n')
        cpuCom = "ps -p {i} -o \%cpu".format(i=processNum)
        cpuUsage = os.popen(cpuCom).read()
        self.txtBox.delete(1.0, END)
        self.txtBox.insert(0.0, cpuUsage)
      
    def getMemUsage(self):
        processId = os.popen("pgrep mongo").read()
        processNum = processId.strip('\n')
        memCom = "ps -p {i} -o \%mem".format(i=processNum)
        memUsage = os.popen(memCom).read()
        self.txtBox.delete(1.0, END)
        self.txtBox.insert(0.0, memUsage)   
        
    def getDBStats(self):
        self.txtBox.delete(0.0, END)
        connect = db.Database()
        if not self.entryEmpty():
            dbStats = connect.getDBStats(self.txtEntry.get())
            self.txtBox.insert(0.0, pformat(dbStats))
        else:
            txt = "Please provide a Database to see the stats."
            self.txtBox.insert(0.0, txt)
        
    def getCollStats(self):
        self.txtBox.delete(0.0, END)
        self.txtBox.insert(0.0, "example: database.collection")
        self.txtBox.insert(0.0, "Please put in the Database name . Collection\n")
        if (len(self.txtEntry.get().split(".")) == 2) and not self.entryEmpty():
            entry = self.txtEntry.get().split(".")
            if self.checkDBandCol(entry[0],entry[1]):
                connect = db.Database()
                colStats = connect.getCollStats(entry[0],entry[1])
                self.txtBox.insert(0.0, pformat(colStats))
            else:
                txt = "The database and collection pair doesn't exists.\n"
                self.txtBox.insert(0.0, txt)
        else:
            txt = "Please provide a Database and collection and input properly to see the stats.\n"
            self.txtBox.insert(0.0, txt)
       
    def getStatementCount(self):
        self.txtBox.delete(0.0, END)
        connect = db.Database()
        sCount=connect.getTransactionCount()
        self.txtBox.insert(0.0, pformat(sCount))   
       
    def connectionCount(self):
        self.txtBox.delete(0.0,END)
        connect= db.Database()
        connCount=connect.getConnectionCount()
        self.txtBox.insert(0.0, connCount)   
       
    def viewConnection(self):
        self.txtBox.delete(0.0,END)
        connect=db.Database()
        viewConn=connect.viewConnectionInfo()
        self.txtBox.insert(0.0, pformat(viewConn)) 
        
    def getLogs(self):
        log = os.popen("tail -50 {f}".format(f=self.log)).read()
        self.txtBox.delete(0.0, END)
        self.txtBox.insert(0.0, log) 

    def checkDBandCol(self, database, coll):
        connect=db.Database()
        dbnames = connect.getDatabases()
        if db in dbnames:
            colnames = connect.getCollections(database)
            if coll in colnames:
                return True
            else:
                return False
        else:
            return False
    
    def entryEmpty(self):
        if (len(self.txtEntry.get())==0):
            return True
        else:
            return False    
    
    
    
    