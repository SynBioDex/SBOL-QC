"""
Read an SBOL file and display its contents
"""

# Add SBOL directory to PYTHONPATH
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import sbol
import libsbol

doc = sbol.Document()
# doc.read('test.xml')


DC = sbol.DNAComponent(doc, 'http://examples.com/DC')
SA = sbol.SequenceAnnotation(doc, 'http://examples.com/DC/SA1')
SA2 = sbol.SequenceAnnotation(doc, 'http://examples.com/DC/SA2')
seq = sbol.DNASequence(doc, 'http://examples.com/DC/Seq')

DC2 = sbol.DNAComponent(doc, 'http://examples.com/DC/SA1/DC')
DC.display_id = 'Parent Component'
DC2.display_id = 'Child Component'
DC.sequence = seq
DC.annotations.append(SA)
DC.annotations.append(SA2)
SA.strand = '-'
SA.subcomponent = DC2
seq.nucleotides = 'actg'
seq.strand = '-'

print('\n'.join(doc.uris))

print('Total SBOL Objects: %d' %doc.num_sbol_objects)
print('Collections: %d' %len(doc.collections))
print('Components: %d' %len(doc.components))
print('Annotations: %d' %len(doc.annotations))
print('Sequences: %d' %len(doc.sequences))
print('---')


DC_copy = DC.deepcopy('#1')

print('\n'.join(doc.uris))
print('Total SBOL Objects: %d' %doc.num_sbol_objects)
print('Collections: %d' %len(doc.collections))
print('Components: %d' %len(doc.components))
print('Annotations: %d' %len(doc.annotations))
print('Sequences: %d' %len(doc.sequences))
print('---')
out = raw_input()

SA = sbol.SequenceAnnotation(doc, 'http://yuckyuck.yuck')
print SA.uri
print SA.start
SA.start = 1
print SA.start
print SA.end
SA.precedes.append(SA2)
SA.precedes[0].uri
SA2 = SA.precedes[0]
print(len(SA.precedes))
SA.precedes.remove(SA2)
print(len(SA.precedes))
#SA.end = 10
#print SA.end
#print SA.strand
#SA.strand = '+'
#print SA.strand
#print repr(SA.subcomponent)
#SA.subcomponent = sbol.DNAComponent(doc, 'http://yuck.yuck')
#print repr(SA.subcomponent)
## addPrecedesRelationship
## removePrecedesRelationship
## getNumPrecedes
## getNthPrecedes
## precedes
## printSequenceAnnotation
#SA.__del__()