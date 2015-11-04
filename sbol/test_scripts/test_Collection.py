"""
Test property getters/setters for DNAComponents
Check DNAComponent.type, since this was just implemented in libSBOL
Check remove methods, since these were just added to libSBOL
"""

# Add SBOL directory to PYTHONPATH
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import sbol

doc = sbol.Document()

col1 = sbol.Collection(doc, 'https://blahblahblah.com/1')
col2 = sbol.Collection(doc, 'https://blahblahblah.com/2')
col3 = sbol.Collection(doc, 'https://blahblahblah.com/3')
col3.display_id = 'promoter library'
print len(doc.collections)

doc.collections.remove(col2)
print len(doc.collections)

col1.__del__()
print len(doc.collections)

print doc.collections[0].uri
print doc.collections[0].display_id
print doc.collections[0].name

dc = sbol.DNAComponent(doc, 'https://blahblahblah.com//component/1')
col3.components.append(dc)
print dc in col3.components
print col3
exit()
