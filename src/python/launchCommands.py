'''
 use default command depending on extentions 
'''
import sys
import os 
import time
import subprocess
import argparse
import pandas as pd 
import shlex

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        END = '\033[0m'
        def disable(self):
                self.HEADER = ''
                self.OKBLUE = ''
                self.OKGREEN = ''
                self.WARNING = ''
                self.FAIL = ''
                self.ENDC = ''

"""
https://stackoverflow.com/questions/35817/how-to-escape-os-system-calls
"""
def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

"""
Launcher run using Popen : [self.binary , self.pre_argument ] + argument_list + [ self.post_argument ]
"""
class Launcher() : 

    def __init__(self, binary, suffixes, pre_argument= '', post_argument = '' ):
        self.binary		= binary
        self.suffixes 	= suffixes 
        self.pre_argument 	= pre_argument 
        self.post_argument 	= post_argument 

    def run(self , argument) :
        commandToDo = '%s %s %s %s'%(self.binary , self.pre_argument, argument, self.post_argument ) 
        print(bcolors.WARNING+"---> RUN : "+bcolors.FAIL+commandToDo+bcolors.END)
        os.system(commandToDo)

    def runOpen(self , argument_list) :
        aList = [self.binary , self.pre_argument ] + argument_list + [ self.post_argument ] 
        stream = " ".join(x for x in aList ) 
        print(bcolors.WARNING+"---> RUN : " + bcolors.FAIL + stream  + bcolors.END)
        p1 = subprocess.Popen(aList) 

"""
split path into 2 string: first one behind identical to path without the 'extension',
the second one being the extnesion, i.e. the part after the last '.'
"""
def getPathAndExtension(path ):
    filename, file_extension = os.path.splitext(path)
    file_extension = file_extension.replace(".","")
    return filename ,  file_extension

"""
return list of customized 'Launcher'
"""
def defineLaunchers() : 
    # associiate extension with command and argument if any 
    launchers = [ 
        Launcher('ws'  ,   ['conn', 'hex'] ),
        Launcher('ws'  ,   ["fra"] ),
        Launcher('az'  ,   ['tmp','tria','quad','brd','tube',
            'dat','hmtc','stl','astl'], pre_argument = '-S', post_argument = ''),
        Launcher('evince' 	, ['pdf','ps','gs','PDF'] ) ,
        Launcher('libreoffice',
            ['odt','xls','ppt','doc','ods','docx','csv','xlsx','odp','pptx']),
        Launcher('ristretto', ['png','gif','jpg','bmp','ppm','pgm'] ),
        Launcher('python'  , ['py']   ) ,
        Launcher('paraview', ['pvd','vtu','tec','vtk','vtp','pvsm'] ) ,
        Launcher('tec'     , ['lpk','plt','lay']) ,
        Launcher('vlc'     , ['mp4','mkv',"avi","mpg","flv","m2t"] ), # ffplay ? 
        Launcher('gmsh'    , ['msh','geo'] ) ,
        Launcher('xfig'    , ['fig'] ),
        Launcher('gnuplot' , ['gnu'] ), # this is not rekonize extension at all ! 
        Launcher('yEd'     , ['graphml'] ),
        Launcher('pdflatex', ['tex'] ),
        Launcher('chromium-browser', ["html"]) ,
        Launcher('geomview', ['off'] ) 
    ]
    return launchers 

def getBinaryFromExtension(launchers ):
    # build reverse dict 
    binary_from_extension = {}
    for launcher in launchers :
        for extension in launcher.suffixes: 
            if not extension in binary_from_extension.keys() :
                binary_from_extension[extension] = launcher.binary
            else : 
                raise KeyError ("mulitple extension for %s"%extension) 
    # check unicity : ...TODO
    return binary_from_extension

def getLauncherFromBinary(launchers ):
    # build reverse dict 
    launcher_from_binary = {}
    for launcher in launchers :
        launcher_from_binary[launcher.binary] = launcher
    return launcher_from_binary

'''
check if all file provided as arguments of the script have the same extension 
    if yes:    launch them all with the same command. We assume the command is compatible.  
    else :     launch them with different commands sequentially. We do want to group file that can launched with the same command together 
'''
def main () : 
    NoA=len(sys.argv)
    if not NoA > 1   :
        print("no argument passed") 
        return 
    # get lauchers 
    launchers = defineLaunchers() 
    binary_from_extension = getBinaryFromExtension(launchers )
    launcher_from_binary = getLauncherFromBinary(launchers )
    filenames = [] 
    name_wo_extension_s = []
    extensions = []
    for i in range(1, NoA)    : 
        inputfile = sys.argv[i]
        filenames.append(inputfile ) 
        name_wo_extension, extension = getPathAndExtension(inputfile )
        name_wo_extension_s.append(name_wo_extension)
        extensions.append( extension)
    df = pd.DataFrame({"inputfile": filenames, "name_wo_extension": name_wo_extension_s, "extension": extensions })
    df = df.loc[df.extension.isin(binary_from_extension.keys())]
    df.loc[:, "binary"] = df.apply(lambda x :binary_from_extension[ x["extension"]], axis = 1)
    print( df)
    groups = df.groupby("binary")
    for binary, dfc in groups :
        print( df)
        filenames_concatenated = ''
        for arg in dfc.inputfile : 
            filenames_concatenated += ' %s'%arg
        launcher = launcher_from_binary[binary]
        launcher.run( filenames_concatenated )
        #launcher.runOpen(dfc.inputfile.to_list()) 
        
main() 
