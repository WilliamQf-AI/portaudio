from __future__ import print_function

import os
import os.path

paRootDirectory = '../../'
paHtmlDocDirectory = os.path.join( paRootDirectory, "doc", "html" )

## Script to check documentation status
## this script assumes that html doxygen documentation has been generated
##
## it then walks the entire portaudio source tree and check that
## - every source file (.c,.h,.cpp) has a doxygen comment block containing
##	- a @file directive
##	- a @brief directive
##	- a @ingroup directive
## - it also checks that a corresponding html documentation file has been generated.
##
## This can be used as a first-level check to make sure the documentation is in order.
##
## The idea is to get a list of which files are missing doxygen documentation.
##
## How to run:
##  $ cd doc/utils
##  $ python checkfiledocs.py

def oneOf_a_in_b(a, b):
    for x in a:
        if x in b:
            return True
    return False

# recurse from top and return a list of all with the given
# extensions. ignore .svn directories. return absolute paths
def recursiveFindFiles( top, extensions, dirBlacklist, includePaths ):
    result = []
    for (dirpath, dirnames, filenames) in os.walk(top):
        if not oneOf_a_in_b(dirBlacklist, dirpath):
            for f in filenames:
                if os.path.splitext(f)[1] in extensions:
                    if includePaths:
                        result.append( os.path.abspath( os.path.join( dirpath, f ) ) )
                    else:
                        result.append( f )
    return result

# generate the html file name that doxygen would use for
# a particular source file. this is a brittle conversion
# which i worked out by trial and error
def doxygenHtmlDocFileName( sourceFile ):
    return sourceFile.replace( '_', '__' ).replace( '.', '_8' ) + '.html'


sourceFiles = recursiveFindFiles( os.path.join(paRootDirectory,'src'), [ '.c', '.h', '.cpp' ], ['.svn', 'mingw-include'], True )
sourceFiles += recursiveFindFiles( os.path.join(paRootDirectory,'include'), [ '.c', '.h', '.cpp' ], ['.svn'], True )
docFiles = recursiveFindFiles( paHtmlDocDirectory, [ '.html' ], ['.svn'], False )



currentFile = ""

def printError( f, message ):
    global currentFile
    if f != currentFile:
        currentFile = f
        print(f, ":")
    print("\t!", message)


for f in sourceFiles:
    if doxygenHtmlDocFileName( os.path.basename(f) ) not in docFiles:
        printError( f, "no doxygen generated doc page" )

    s = open( f, 'rt' ).read()

    if '/**' not in s:
        printError( f, "no doxygen /** block" )  
    
    if '@file' not in s:
        printError( f, "no doxygen @file tag" )

    if '@brief' not in s:
        printError( f, "no doxygen @brief tag" )
        
    if '@ingroup' not in s:
        printError( f, "no doxygen @ingroup tag" )
