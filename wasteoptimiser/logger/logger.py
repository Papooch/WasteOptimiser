from datetime import datetime
import os

class CustomEnum:
    def __init__(self, levels):
        self._levels = levels
        for i, level in enumerate(levels):
            setattr(self, level, i)

    def __getitem__(self, key):
        return self._levels[key]

logType = CustomEnum(['GENERAL', 'PARSER', 'GUI', 'OPTIMISER'])
logLevel = CustomEnum(['DEBUG', 'INFO', 'WARNING', 'ERROR'])

class Logger:
    logType = logType
    logLevel = logLevel

    def __init__(self, log_file_dir=None, min_print_level=0, min_log_level=0, print_function=None):
        self.min_log_level = min_log_level
        self.min_print_level = min_print_level
        self.print_function = print_function or print
        self.log_file = self._create_log_file(log_file_dir, "WasteOptimiser") if log_file_dir else None

    def log(self, message, level=0, ltype=0):
        if(level >= self.min_log_level):
            self._append_log_file(message, level, ltype)
        if(level >= self.min_print_level):
            self.print_function(message)

    def setPrintFunction(self, func):
        self.print_function = func

    def _create_log_file(self, dir, name):
        timestring = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = dir + "/" + name + "-" + timestring + ".log"
        message = "Log file for " + name + " created. Timestamp: " + timestring
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as out:
            out.write("Time, Origin, Level, Message\n")
            out.write(datetime.now().strftime("%H:%M:%S,") + "INFO,GENERAL," + message)
        return filename


    def _append_log_file(self, message, level, ltype):
        if not self.log_file: return
        with open(self.log_file, 'a') as out:
            out.write("\n" + datetime.now().strftime("%H:%M:%S,") + logType[ltype] + "," + logLevel[level] + "," + message)