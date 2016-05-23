
# coding: utf-8

# In[2]:

'''

__author__ = "TM Seminar SoSe2016"
__authors__ = "Philip Duerholt, Michael Huber"
__email__ = "philip.duerholt@stud-mail.uni-wuerzburg.de, michael.huber@stud-mail.uni-wuerzburg.de"
__license__ = ""
__version__ = ""
__date__ = 2016-05-23

'''

from lxml import etree
from _collections import defaultdict
import re
import os.path
import glob




def parseXML(directory, outdir):
    '''
  
    
    
    '''
    mets = etree.parse(directory)
    xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
    filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})
    
    print(filePathYear)

    structLink= mets.xpath('/mets:mets/mets:structLink/mets:smLink', namespaces={'mets':'http://www.loc.gov/METS/',
                                                                                 'xlink':'http://www.w3.org/1999/xlink'})
    
    d = defaultdict(list)
    
    #Das in geschweifter Klammern ist der namespace. Im Document ist das "xlink:"
    #from und to sind die Attributnamen von smLink
    
    for child in structLink:
        k = child.get('{http://www.w3.org/1999/xlink}from')
        v = child.get('{http://www.w3.org/1999/xlink}to')
        d[k].append(v)
   
        
    for item in d:
        xpathE ='//mets:structMap[@TYPE="LOGICAL"]//mets:div[@ID="'+item+'"]' #kennt das etree-objekt seine Eltern/Großeltern?
        structMap = mets.xpath(xpathE, namespaces= {'mets':'http://www.loc.gov/METS/'})

        structMapElement = structMap[0]

        if structMapElement.get('LABEL') != None:
            xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
            filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})
            label = filePathYear[0]+'\\'+ structMapElement.get('LABEL')

            fileList = d[item]
            
            createFile(label, fileList, directory, outdir)
            #dir1 als parameter mitgeben um die Information in welchem Band der Artikel zu finden ist zu kreieren

def createFile(label, fileList, directory, outdir):
    '''
    dir1 = wo die Datein hinsollen
    dir2 = wo die Datein herkommen
    '''
    
    print("LABEL ===== " + label)
    
    dir1 = outdir + re.sub(' ', '' , re.sub('[.,]', '_', label[:12])) + '\\' + label[8:12] + "_" + re.sub('[^a-zA-ZäüöÄÖÜß0-9_]', '' , re.sub(' ', '_' , label[12:200])) + '.txt'

    print("DIR ==== " + dir1)
    
    dir2 = directory[:-15] + '\\fulltext\\'

    missingFiles=[]
    for item in fileList:

        if os.path.isfile(dir2 + item[4:]+'.xml'):
            
            with open (dir2 + item[4:]+'.xml','r', encoding = "utf-8") as r:
                data = r.read()
                if not os.path.exists(os.path.dirname(dir1)):
                    os.makedirs(os.path.dirname(dir1))
                with open (dir1, 'a', encoding = "utf-8" ) as f:
                    f.write(re.sub('¬ ', '', (re.sub('\n*<[^>]*>*\n*', '', (re.sub('</line>', ' ', data))))))
        else:
            missingFiles.append(item[4:])
        
        
        
def parseFolders(indir, outdir):
    indir = os.getcwd() + indir
    outdir = os.getcwd() + outdir
    for item in glob.glob(indir + '*/export_mets.xml'):
        print ('doing: ',item)
        parseXML(item, outdir)
        print(item, ': done')
'''
################################## HIER STEHT DER WICHTIGE TEIL ####################################################

- parseFolders nimmt zwei Argumente: indir (input directory) und outdir (output directory)
- dieses Script sollte sich im selben Ordner befinden, wie der Ordner mit allen "vls-suubdfggb(usw.)" Ordnern
- in meinem Script heißt mein Ordner mit allen "vls-suubdfggb(usw.)" Ordnern drin "raw"
- ihr könnt einen anderen Namen für diesen Ordner wählen, aber dann müsst ihr unten '/raw/' mit eurem Ordnernamen ersetzen
- z.B. statt '/raw/' steht bei dir '/sammlung/'
- in den "vls-suubdfggb(usw.)" Ordnern sind zwei Dinge (1) ein Ordner namens 'fulltext' und (2) eine Datei 'export_mets.xml'
- dieses Script erzeugt zur Ausgabe einen Ordner mit den namen 'pre' und er wird im selben Ordner sein, wie dieses Script
- der Prozess dauert ziemlich lange
- die Ordnerstruktur beachtet nicht die Bände

################################## HIER STEHT DER WICHTIGE TEIL ####################################################
'''
        
        
parseFolders('/raw/', '/pre/')


