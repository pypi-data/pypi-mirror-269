__version__ = "1.2.1"
__packagename__ = "autorerun"


def updatePackage():
    from time import sleep
    from json import loads
    import http.client
    print(f"Checking updates for Package {__packagename__}")
    try:
        host = "pypi.org"
        conn = http.client.HTTPSConnection(host, 443)
        conn.request("GET", f"/pypi/{__packagename__}/json")
        data = loads(conn.getresponse().read())
        latest = data['info']['version']
        if latest != __version__:
            try:
                import pip
                pip.main(["install", __packagename__, "--upgrade"])
                print(f"\nUpdated package {__packagename__} v{__version__} to v{latest}\nPlease restart the program for changes to take effect")
                sleep(3)
            except:
                print(f"\nFailed to update package {__packagename__} v{__version__} (Latest: v{latest})\nPlease consider using pip install {__packagename__} --upgrade")
                sleep(3)
        else:
            print(f"Package {__packagename__} already the latest version")
    except:
        print(f"Ignoring version check for {__packagename__} (Failed)")


import threading
class Runner(threading.Thread):

    def __init__(self, toRun:dict[str, list[str]], toCheck:list[str], reCheckInterval:int=1):
        """
        Initialise the Runner with appropriate parameters and use the start() method to start the process
        :param toRun: dictionary with filenames to run as the keys and list of all arguments to pass as the value
        :param toCheck: list of all the filenames to check for updates
        :param reCheckInterval: count in seconds to wait for update check
        """
        from subprocess import Popen as __Popen
        from time import sleep as __sleep
        from sys import executable as __executable
        from os import stat as __stat
        import customisedLogs as __customisedLogs
        self.__Popen = __Popen
        self.__sleep = __sleep
        self.__executable = __executable
        self.__stat = __stat
        self.__customisedLogs = __customisedLogs
        threading.Thread.__init__(self)
        self.logger = self.__customisedLogs.Manager()
        self.programsToRun = toRun
        self.programsToCheck = toCheck
        self.currentProcesses:list[__Popen] = []
        self.reCheckInterval:float = reCheckInterval
        self.lastFileStat = self.fetchFileStats()
        self.startPrograms()


    def run(self):
        """
        Overriding run from threading.Thread
        Infinite Loop waiting for file updates and re-run the programs if updates found
        :return:
        """
        while True:
            if self.checkForUpdates():
                self.startPrograms()
            self.__sleep(self.reCheckInterval)


    def fetchFileStats(self)->dict[str, float]:
        """
        Checks current file state
        Returns a list containing tuples containing each file and its last modified state
        If a to-be-checked file gets added, or goes missing, it is treated as a file update
        :return:
        """
        tempStats:dict[str, float] = {}
        for filename in self.programsToCheck:
            try:
                tempStats[filename] = self.__stat(filename).st_mtime
            except: ## file is not present
                tempStats[filename] = 0
        return tempStats


    def checkForUpdates(self)->bool:
        """
        Checks if current file state matches old known state
        Returns a boolean if current received file state differs from the last known state
        :return:
        """
        fileStat = self.fetchFileStats()
        if self.lastFileStat != fileStat:
            changes = []
            for file in fileStat:
                if fileStat[file] != self.lastFileStat[file]:
                    changes.append(file)
            self.logger.success("FILE CHANGED", "\n".join(changes))
            self.lastFileStat = fileStat
            return True
        else:
            return False


    def startPrograms(self):
        """
        Respawns processes
        Kills last running processes if any and then respawn newer processes for each file to be run
        :return:
        """
        temp = self.currentProcesses.copy()
        if temp:
            self.logger.success("PROCESS", "Killing previous processes")
        for _process in temp:
            if _process and not _process.poll():
                _process.kill()
                _process.wait()
                self.currentProcesses.remove(_process)
        for program in self.programsToRun:
            self.currentProcesses.append(self.__Popen([self.__executable, program]+self.programsToRun[program]))
            self.logger.success("PROCESS", "Started new process")
