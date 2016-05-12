'''
philips stuff:

import re
import glob


for file in glob.glob('raw/*.xml'):
    with open(file, 'r', encoding = "utf-8") as r:
        f = r.read()
        with open('pre/' + file[3:-4]  + '.txt', 'w', encoding = 'utf-8') as text: 
            text.write(re.sub('¬ ', '', (re.sub('\n*<[^>]*>*\n*', '', (re.sub('</line>', ' ', f))))))

'''

from lxml import etree
from _collections import defaultdict
import re
import os.path



def parseXML(directory):
    '''
    maybe add a parser?
    
    
    '''
    mets = etree.parse(directory)
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
        xpathE ='//mets:structMap[@TYPE="LOGICAL"]//mets:div[@ID="'+item+'"]'
        structMap = mets.xpath(xpathE, namespaces= {'mets':'http://www.loc.gov/METS/'})
        #print(structMap)
        structMapElement = structMap[0]
        #print(etree.tostring(structMapElement, pretty_print=True))
        print(structMapElement.get('LABEL'))
        if structMapElement.get('LABEL') != None:
            label = structMapElement.get('LABEL')
            fileList = d[item]
            print (fileList)
            createFile(label, fileList)

def createFile(label, fileList):
    '''
    dir1 = wo die Datein hinsollen
    dir2 = wo die Datein herkommen
    '''
    dir1 = '/Users/MHuber/Documents/SS2016/TopicModelling/noXML/' + label
    dir2 = '/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/vls-suubdfggb-1913-341897/fulltext/'
    missingFiles=[]
    for item in fileList:
        
        #opens finereaderfiles
 
        if os.path.isfile(dir2 + item[4:]+'.xml'):
            with open (dir2 + item[4:]+'.xml','r', encoding = "utf-8") as r:
                data = r.read()
                with open (dir1, 'a', encoding = "utf-8" ) as f:
                    f.write(re.sub('¬ ', '', (re.sub('\n*<[^>]*>*\n*', '', (re.sub('</line>', ' ', data))))))
        else:
            missingFiles.append(item[4:])
        
        
        

parseXML('/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/vls-suubdfggb-1913-341897/export_mets.xml')
        
    
    




