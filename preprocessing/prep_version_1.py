'''
ToDo:
folgende Ordnerstruktur sollte erstellt werden:

Jahr -> Band ->Titel1
            ->Titel2
            ->Titel3
            
Wo geht die Reihenfolge verloren? (die Texte werden in der falschen Reihenfolge zusammengeklebt)
-> liegt es an dem returnvalue von etree.xpath?

'''

from lxml import etree
from _collections import defaultdict
import re
import os.path
import glob




def parseXML(directory):
    '''
  
    
    
    '''
    mets = etree.parse(directory)
    xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
    filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})
    
    print(filePathYear)
    #'/Users/MHuber/Documents/SS2016/TopicModelling/
    structLink= mets.xpath('/mets:mets/mets:structLink/mets:smLink', namespaces={'mets':'http://www.loc.gov/METS/',
                                                                                 'xlink':'http://www.w3.org/1999/xlink'})
    #print(structLink)
    
    d = defaultdict(list)
    for child in structLink:
        k = child.get('{http://www.w3.org/1999/xlink}from')
        v = child.get('{http://www.w3.org/1999/xlink}to')
        d[k].append(v)
        #print(k, ": ", v)
        #print(child.get('{http://www.w3.org/1999/xlink}to'))
        #if '{http://www.w3.org/1999/xlink}to' in child.attrib:
            #print(child.attrib('{http://www.w3.org/1999/xlink}to'))
        
        #for key,value in sorted(child.items):
            #print('%s = %r' % (key.tostring(), value.tostring()))
    #print(d['log348270'])
   
        
    for item in d:
        xpathE ='//mets:structMap[@TYPE="LOGICAL"]//mets:div[@ID="'+item+'"]' #kennt das etree-objekt seine Eltern/Großeltern?
        structMap = mets.xpath(xpathE, namespaces= {'mets':'http://www.loc.gov/METS/'})
        #print(structMap)
        structMapElement = structMap[0]
        #print(etree.tostring(structMapElement, pretty_print=True))
        #print(structMapElement.get('LABEL'))
        if structMapElement.get('LABEL') != None:
            xpathVolume ='//mets:structMap//mets:div[@TYPE="volume"]/@LABEL'
            filePathYear = mets.xpath(xpathVolume, namespaces={'mets':'http://www.loc.gov/METS/'})
            label = filePathYear[0]+'/'+ structMapElement.get('LABEL')
            #print (label)
            fileList = d[item]
            #print (fileList)
            createFile(label, fileList)
            #dir1 als parameter mitgeben um die Information in welchem Band der Artikel zu finden ist zu kreieren

def createFile(label, fileList):
    '''
    dir1 = wo die Datein hinsollen
    dir2 = wo die Datein herkommen
    '''
    dir1 = '/Users/MHuber/Documents/SS2016/TopicModelling/newTry/' + label+'.txt'
    #print(dir1)
    dir2 = '/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/vls-suubdfggb-1913-341897/fulltext/'
    missingFiles=[]
    for item in fileList:
        
        #opens finereaderfiles
 
        if os.path.isfile(dir2 + item[4:]+'.xml'):
            with open (dir2 + item[4:]+'.xml','r', encoding = "utf-8") as r:
                data = r.read()
                if not os.path.exists(os.path.dirname(dir1)):
                    os.makedirs(os.path.dirname(dir1))
                with open (dir1, 'a', encoding = "utf-8" ) as f:
                    f.write(re.sub('¬ ', '', (re.sub('\n*<[^>]*>*\n*', '', (re.sub('</line>', ' ', data))))))
        else:
            missingFiles.append(item[4:])
        
        
        

for item in glob.glob('/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/*/export_mets.xml'):
    print ('doing: ',item)
    parseXML(item)
    print(item, ': done')

#parseXML('/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/vls-suubdfggb-1913-341897/export_mets.xml')
        
    
    




