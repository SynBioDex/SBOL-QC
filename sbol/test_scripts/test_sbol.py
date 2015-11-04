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
doc.write('test_round_trip.xml')

print('Total SBOL Objects: %d' %doc.num_sbol_objects)
print('Collections: %d' %len(doc.collections))
print('Components: %d' %len(doc.components))
print('Annotations: %d' %len(doc.annotations))
print('Sequences: %d' %len(doc.sequences))
print('---')
doc2 = sbol.Document()
doc2.read('test_round_trip.xml')
print('Total SBOL Objects: %d' %doc2.num_sbol_objects)
print('Collections: %d' %len(doc2.collections))
print('Components: %d' %len(doc2.components))
print('Annotations: %d' %len(doc2.annotations))
print('Sequences: %d' %len(doc2.sequences))

SA = sbol.SequenceAnnotation(doc, 'http://yuckyuck.yuck')
print SA.uri
print SA.start
SA.start = 1
print SA.start
print SA.end
SA.end = 10
print SA.end
print SA.strand
SA.strand = '+'
print SA.strand
print repr(SA.subcomponent)
SA.subcomponent = sbol.DNAComponent(doc, 'http://yuck.yuck')
print repr(SA.subcomponent)
# addPrecedesRelationship
# removePrecedesRelationship
# getNumPrecedes
# getNthPrecedes
# precedes
# printSequenceAnnotation
SA.__del__()