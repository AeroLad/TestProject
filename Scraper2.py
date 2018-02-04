import glob
import os
import time
import GenericPage
import configparser


scriptDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)),'')


BadINIFiles     = []
LoadedINIFiles  = []

while True:
    iniFiles = []
    WebPages = []
    for dirpath, subdirs, files in os.walk(scriptDirectory):
        for iniFile in files:
            if iniFile.endswith(".ini"):
                iniFiles.append(os.path.join(dirpath,iniFile))

    for iniFile in iniFiles:
        webpage = GenericPage.GenericPage()
        webpage.strINIFile = iniFile
        configFile = webpage.LoadConfigFile()
        if isinstance(configFile,configparser.ConfigParser):
            try:
                module  = __import__(webpage.type)
                klass   = getattr(module,webpage.type)
                webpage = klass()
                webpage.strINIFile = iniFile
                if iniFile in BadINIFiles:
                    BadINIFiles.remove(webpage.strINIFile)
                if (iniFile not in LoadedINIFiles):
                    print("Loaded INI file: %s" %(iniFile))
                    LoadedINIFiles.append(iniFile)
                WebPages.append(webpage)
            except:
                if iniFile not in BadINIFiles:
                    print("Error loading page module: %s" %(iniFile))
                    BadINIFiles.append(iniFile)
                if (iniFile in LoadedINIFiles):
                    LoadedINIFiles.remove(iniFile)
        else:
                if iniFile not in BadINIFiles:
                    print("Error loading INI file: %s" %(iniFile))
                    BadINIFiles.append(iniFile)
                if (iniFile in LoadedINIFiles):
                    LoadedINIFiles.remove(iniFile)

    for webpage in WebPages:
        webpage.StartProcess()

    for webpage in WebPages:
        if webpage.Process != None and webpage.Process.is_alive():
            webpage.Process.join()

    time.sleep(10)
