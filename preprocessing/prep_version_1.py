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
        xpathE ='//mets:structMap//mets:div[@ID="'+item+'"]'
        structMap = mets.xpath(xpathE, namespaces= {'mets':'http://www.loc.gov/METS/'})
        #print(structMap)
        structMapElement = structMap[0]
        #print(etree.tostring(structMapElement, pretty_print=True))
        print(structMapElement.get('LABEL'))
        
        createFile()

def createFile():
    '''
    ToDo: create File with name == structMapElement.get('LABEL') containing a cleansed version of the xmlfile as txt using philips script
    '''


parseXML('/Users/MHuber/Documents/SS2016/TopicModelling/1913-20/vls-suubdfggb-1913-341897/export_mets.xml')
        
    
    




