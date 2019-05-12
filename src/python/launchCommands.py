'''
 use default command depending on extentions 
'''

from subprocess import *
import sys
import os 
import time
import subprocess

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


'''
    map inputfile with name.extension 
    and return: name, extension 
    if "." does not exist, extension = ""
    
'''
def get_name_extension_from_file(inputfile) :
    name = ''
    extension = ''
    sringsList = inputfile.split(".")
    try: 
        N = int(len(sringsList)) 
    except : 
        print("Count not split inputfile: {:} using '.' ".format(inputfile))
    if N == 0 : 
        pass
    elif  N == 1 : 
        name = inputfile
    elif N > 1 :
        # concatenate all member but last 
        for i in range(0, N - 1 ) : 
            name += sringsList[i] 
        extension = sringsList[-1]
    else : 
        print ("N = %d is not handled, exit".format(N) ) 
        exit(1) 
    return name, extension 
 
def defineLaunchers() : 
        # group extension to be launched by same command 
        Launchers = [] 
        Gridlist = ['conn', 'hex']
        Topolist = ['fra']
        Surflist = ['tmp','tria','quad','brd','tube','stl','dat','hmtc','stl','astl']
        pdf 	 = ['pdf','ps','gs','PDF'] 
        oo 	 = ['odt','xls','ppt','doc','ods','docx','csv','xlsx','odp','pptx']
        pic 	 = ['png','gif','jpg','bmp','ppm','pgm']
        cfdDB 	 = ['pvd','vtu','tec','vtk','vtp','pvsm']
        py 	= ['py']
        tecplot = ['lpk','plt','lay']
        vidList = ['mp4','mkv',"avi","mpg","flv","m2t"]
        gmshList= ['msh','geo']
        xfigList= ['fig']
        gnuplotList = ['gnu']
        yEdList = ['graphml']
        pdflatexList = ['tex']
        htmlList = ['html']
        geomviewList = ["off"]
        # associiate extension with command and argument if any 
        launchers = [] 
        launchers.append( Launcher( 'ws' 		, Gridlist    ) )
        launchers.append( Launcher( 'ws' 		, Topolist    ) )
        launchers.append( Launcher( 'az' 		, Surflist    , pre_argument = '-S' , post_argument = '') )
        launchers.append( Launcher( 'evince' 	, pdf    ) )
        launchers.append( Launcher( 'libreoffice' 	, oo    ) )
        launchers.append( Launcher( 'ristretto' 	, pic    ) )
        launchers.append( Launcher( 'python3.6' 	, py    ) )
        launchers.append( Launcher( 'paraview' 	, cfdDB    ) )
        launchers.append( Launcher( 'tec'	 	, tecplot    ) )
        launchers.append( Launcher( 'vlc'		, vidList ) ) 
        #launchers.append( Launcher( 'ffplay'	, vidList ) ) 
        launchers.append( Launcher( 'gmsh'		, gmshList ) )
        launchers.append( Launcher( 'xfig'		, xfigList ) ) 
        launchers.append( Launcher( 'gnuplot' 	, gnuplotList ) )    
        launchers.append( Launcher( 'yEd'		, yEdList ) ) 
        launchers.append( Launcher( 'pdflatex'	, pdflatexList ) ) 
        launchers.append( Launcher( 'chromium-browser'	, htmlList ) ) 
        launchers.append( Launcher( 'geomview'	, geomviewList ) ) 
        return launchers 

def main () : 
    NoA=len(sys.argv)
    if not NoA > 1   :
        print("no argument passed") 
        pass   
    else   : 
        # get lauchers 
        launchers = defineLaunchers() 
        # check if all file have the same extension 
        # if yes:    launch them all with the same command. We assume the command is compatible. 
        # else :     launch them with different commands sequentially from first to last after sorting. We don't want to group file that can launched with the same commande together 
        filenames = [] 
        associated_launcher = [] 
        for i    in range(1,    NoA)    : 
            inputfile = sys.argv[i]
            filenames.append(inputfile ) 
        filenames.sort() 

        # scan the extensions and check if at least one of them is different from the other. 
        all_filenames_have_same_extension = True 
        arg_id = -9 
        first = True 
        for i in range(0, len( filenames ))    :
            found_launcher = False 
            arg = filenames[i]
            name, extension = get_name_extension_from_file(arg)
            for j in range(0, len(launchers )) : 
                launcher = launchers[j]    
                if extension in launcher.suffixes : 
                    associated_launcher.append(launcher)
                    found_launcher = True    
                    break 
            # 
            if not found_launcher : 
                print("no file extention for %s"%arg) 
                sys.exit(0)
            print("File name : "+bcolors.HEADER+name+bcolors.END)
            print("Extension : "+bcolors.HEADER+extension+bcolors.END)
            # 
            if first : 
                first = False 
                arg_id = j 
            else : 
                if arg_id != j :
                    all_filenames_have_same_extension = False 

        # scan the extensions and launch the commands 
        if all_filenames_have_same_extension :
            launcher = associated_launcher[0]
            filenames_concatenated = ''
            for arg in filenames : 
                filenames_concatenated += ' %s'%arg
            launcher.run( filenames_concatenated )
        else : 
            for i in range(0, len( filenames )): 
                arg = filenames[i]
                launcher = associated_launcher[i]
                launcher.run( arg ) 
                                                                                                                                                                         
        
main() 
