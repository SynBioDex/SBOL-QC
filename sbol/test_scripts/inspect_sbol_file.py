"""
Read an SBOL file and display its contents
"""

# Add SBOL directory to PYTHONPATH
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import sbol

doc = sbol.Document()
doc.read('test.xml')
print('Total SBOL Objects: %d' %doc.num_sbol_objects)
print('Collections: %d' %len(doc.collections))
print('Components: %d' %len(doc.components))
print('Annotations: %d' %len(doc.annotations))
print('Sequences: %d' %len(doc.sequences))
for obj in doc.collections:
    print obj
for obj in doc.components:
    print obj
for obj in doc.sequences:
    print obj

for i_obj, obj in enumerate(doc.annotations):
    print i_obj, repr(obj), 'precedes -> ', obj.precedes

for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)

for i_obj, obj in enumerate(doc.annotations):
    if i_obj >= len(doc.annotations) - 2:
        j_obj = i_obj + 2 - len(doc.annotations)
    else:
        j_obj = i_obj + 2
    obj.addPrecedes(doc.annotations[j_obj])

for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)

for i_obj, obj in enumerate(doc.annotations):
    if i_obj >= len(doc.annotations) - 2:
        j_obj = i_obj + 2 - len(doc.annotations)
    else:
        j_obj = i_obj + 2
    obj.removePrecedes(doc.annotations[j_obj])

for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)