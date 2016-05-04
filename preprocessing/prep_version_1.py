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





