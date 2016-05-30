
# coding: utf-8

# In[2]:

'''

__author__ = "TM Seminar SoSe2016"
__authors__ = "Philip Duerholt, Ulrike Henny, Michael Huber"
__email__ = "philip.duerholt@stud-mail.uni-wuerzburg.de, ulrike.henny@uni-wuerzburg.de, michael.huber@stud-mail.uni-wuerzburg.de"
__license__ = ""
__version__ = ""
__date__ = 2016-05-23

'''

import os
import glob
from lxml import etree
from _collections import defaultdict
import re


missingFiles=[]

def parseXML(directory, outdir):
    mets = etree.parse(directory)
    xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
    filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})

    print(filePathYear)

    structLink= mets.xpath('/mets:mets/mets:structLink/mets:smLink', namespaces={'mets':'http://www.loc.gov/METS/',
                                                                                 'xlink':'http://www.w3.org/1999/xlink'})

    d = defaultdict(list)
    
    for child in structLink:
        k = child.get('{http://www.w3.org/1999/xlink}from')
        v = child.get('{http://www.w3.org/1999/xlink}to')
        d[k].append(v)
        
    for item in d:
        xpathE ='//mets:structMap[@TYPE="LOGICAL"]//mets:div[@ID="'+item+'"]'
        structMap = mets.xpath(xpathE, namespaces= {'mets':'http://www.loc.gov/METS/'})

        structMapElement = structMap[0]
        
        #print(str(structMapElement.get('LABEL')))
        
        if structMapElement.get('LABEL') != None:
            xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
            filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})
            labelname = re.sub('[^a-zA-ZäüöÄÖÜß0-9_ ]', '' , structMapElement.get('LABEL'))
            label = os.path.join(filePathYear[0], labelname)
            
            #print("CURRENT LABEL ==== ", label)
            
            fileList = d[item]

            createFile(label, fileList, directory, outdir)
            
            
            
def createFile(label, fileList, directory, outdir):
    '''
    dir1 = wo die Datein hinsollen
    dir2 = wo die Datein herkommen
    '''
    
    #print("LABEL ===== " + label)
    
    dirname = re.sub(' ', '' , re.sub('[.,]', '_', label[:12]))
    
    filename = label[8:12] + "_" + re.sub(' ', '_' , label[13:200]) + '.txt'
    
    print("CURRENT FILENAME ==== " + filename)
    
    dir1 = os.path.join(outdir, os.path.join(dirname, filename))
    
    print("CURRENT DIR ==== " + dir1)
    
    dir2 = os.path.join(directory[:-15], 'fulltext')

    for item in fileList:
        
        sourcename = os.path.join(dir2, item[4:] + '.xml')
        
        if os.path.isfile(sourcename):
            
            with open (sourcename, 'r', encoding = "utf-8") as r:
                data = r.read()
                if not os.path.exists(os.path.dirname(dir1)):
                    os.makedirs(os.path.dirname(dir1))
                with open (dir1, 'a', encoding = "utf-8" ) as f:
                    f.write(re.sub('¬ ', '', (re.sub('\n*<[^>]*>*\n*', '', (re.sub('</line>', ' ', data))))))
        else:
            missingFiles.append(item[4:])


            
def parseFolders(indir, outdir):
    indir = os.path.join(os.getcwd(), indir)
    outdir = os.path.join(os.getcwd(), outdir)
    print(indir)
    print(outdir)
    for item in glob.glob(os.path.join(indir, '*/export_mets.xml')):
        print(item)
        parseXML(item, outdir)
    with open("ERROR_LOG.txt", 'w', encoding = "utf-8") as err:
        err.write(';\n'.join(missingFiles))
    
parseFolders('raw', 'pre')
'''
################################## HIER STEHT DER WICHTIGE TEIL ####################################################

- parseFolders nimmt zwei Argumente: indir (input directory) und outdir (output directory)
- dieses Script sollte sich im selben Ordner befinden, wie der Ordner mit allen "vls-suubdfggb(usw.)" Ordnern
- in meinem Script heißt mein Ordner mit allen "vls-suubdfggb(usw.)" Ordnern drin "raw"
- ihr könnt einen anderen Namen für diesen Ordner wählen, aber dann müsst ihr unten '/raw/' mit eurem Ordnernamen ersetzen
- z.B. statt 'raw' steht bei dir 'sammlung'
- in den "vls-suubdfggb(usw.)" Ordnern sind zwei Dinge (1) ein Ordner namens 'fulltext' und (2) eine Datei 'export_mets.xml'
- dieses Script erzeugt zur Ausgabe einen Ordner mit den namen 'pre' und er wird im selben Ordner sein, wie dieses Script
- der Prozess dauert ziemlich lange
- die Ordnerstruktur beachtet nicht die Bände

################################## HIER STEHT DER WICHTIGE TEIL ####################################################
'''
        
        
parseFolders('raw', 'pre')