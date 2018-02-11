import glob
import os
import time
import configparser

def fnLoadConfigFile(strFile):
    """Load Configuration INI file.

    Args:
        strFile (str):  Full path to INI file.

    Returns:
        configparser.ConfigParser: Parsed configuration file object.
        None: If unsuccesful.
    """

    try:
        if os.path.isfile(strFile) == False:
            return None
        objConfigFile = configparser.ConfigParser()
        objConfigFile.read(strFile)
        return objConfigFile
    except Exception as e:
        print("Error loading INI file: "+strFile)
        print(e)
        print(str(e))
        print(e.args)
        return None

def fnLoadClass(strClass,objConfigFile):
    """Load specific class.

    Args:
        strClass (str):  Name of class to be loaded.
        objConfigFile (configparser.ConfigParser): Parsed configuration file object.

    Returns:
        Class (obj): Class instance of requested class.
        None: If unsuccesful.
    """
    try:
        module  = __import__("Modules."+strClass,fromlist=["*"])
        klass   = getattr(module,strClass)
        obj     = klass(objConfigFile)
        return  obj
    except Exception as e:
        print("Error loading module in: "+strFile)
        print("Specified module: "+strClass)
        print(e)
        print(str(e))
        print(e.args)
        return None

if __name__ == "__main__":

    scriptDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)),'')

    while True:
        start_time = time.time()
        WebPages = []
        for dirpath, subdirs, files in os.walk(scriptDirectory):
            for strIniFile in files:
                if strIniFile.endswith(".ini"):
                    strIniFile = os.path.join(dirpath,strIniFile)
                    objConfigFile = fnLoadConfigFile(strIniFile)
                    if objConfigFile != None:
                        strClassType    = objConfigFile['Page']['type']
                        objClass = fnLoadClass(strClassType,objConfigFile)
                        if objClass != None:
                            WebPages.append(objClass)

        for WebPage in WebPages:
            if WebPage.is_alive(): WebPage.join()

        end_time = time.time()
        print("%i Pages processed in %.2fs" %(len(WebPages),end_time - start_time))
        time.sleep(10)
