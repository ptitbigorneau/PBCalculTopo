import sys
import os
import glob
import re
from distutils.core import setup 
import py2exe

if len(sys.argv)==1:
    sys.argv.append('py2exe')

def listdirectory(path):
    def istocopy(path):
        return (
                os.path.isfile(path)
                and not path.endswith('.pyc') 
                and not path.endswith('.pyo') 
                )
    return map(os.path.normpath, filter(istocopy, glob.glob(path + os.sep + '*')))

myDataFiles = [
        ('', ['License.txt']),
        ('', ['icone.ico']),
        ('', ['topo.gif']),
    ]
    
options = {'py2exe':{'optimize': 1, 'dll_excludes': ['MSVCP90.dll'],"includes": ["dbhash",],}}

setup(name="PBCalculTopo", version="1b", author="PtitBigorneau", url="http://ptitbigorneau.fr",zipfile = "pbcalcultopo.lib",windows=[{"script":"pbcalcultopo.py","icon_resources":[(1,"icone.ico")]}], data_files = myDataFiles, options=options)    
