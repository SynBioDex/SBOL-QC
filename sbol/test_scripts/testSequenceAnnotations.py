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

print('Annotations: %d' %len(doc.annotations))

# Show each annotation and its downstream annotation
for i_obj, obj in enumerate(doc.annotations):
    print i_obj, repr(obj), 'precedes -> ', obj.precedes

for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)

# Add a new precedes relationship to each annotation in the document, testing addPrecedes method

for i_obj, obj in enumerate(doc.annotations):
    if i_obj >= len(doc.annotations) - 2:
        j_obj = i_obj + 2 - len(doc.annotations)
    else:
        j_obj = i_obj + 2
    obj.precedes.append(doc.annotations[j_obj])

# Show that the precedes relationship was changed
for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)

# Remove the new annotations, testing the removePrecedes method

for i_obj, obj in enumerate(doc.annotations):
    if i_obj >= len(doc.annotations) - 2:
        j_obj = i_obj + 2 - len(doc.annotations)
    else:
        j_obj = i_obj + 2
    obj.precedes.remove(doc.annotations[j_obj])

for i_obj, obj in enumerate(doc.annotations):
    print 'Number of SA objects SA[%d] object precedes:' %i_obj, len(obj.precedes)

# Test isUpstream and isDownstream
for i_obj, obj in enumerate(doc.annotations):
    print i_obj, repr(obj), 'precedes -> ', obj.precedes
    if obj.precedes:
        print obj.isUpstream(obj.precedes[0])
        print obj.isDownstream(obj.precedes[0])