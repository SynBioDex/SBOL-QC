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
doc.read('test.xml')
print('Total SBOL Objects: %d' %doc.num_sbol_objects)
print('Components: %d' %len(doc.components))
#for i_obj in range(len(doc.components)-1, -1, -1):
for i_obj in range(0, len(doc.components)):
     obj = doc.components[i_obj]
     print 'Component %d' %i_obj
     print '\turi:', obj.uri
     #print '\tsequence:', obj.sequence
     print('\tannotations: %d' %len(obj.annotations))
     print '\tdisplay_id:', obj.display_id
     print '\tdescription:', obj.description
     print '\tname:', obj.name
     print '\ttype:', obj.type
     #print '\ttype:', obj.type
     if obj.sequence:
         #print obj.sequence
         print repr(obj.sequence)
         print obj.sequence.nucleotides

print('\n'.join([ obj.type for obj in doc.components if obj.type]))
print
# test slicing
print('\n'.join([ obj.type for obj in doc.components[:-1] if obj.type]))
print
print('\n'.join([ obj.type for obj in doc.components[0:1] if obj.type]))
print('\n'.join([ obj.type for obj in doc.components[1:2] if obj.type]))
print('\n'.join([ obj.type for obj in doc.components[2:3] if obj.type]))
print('\n'.join([ obj.type for obj in doc.components[3:4] if obj.type]))
print('\n'.join([ obj.type for obj in doc.components[4:5] if obj.type]))
print
print('\n'.join([ obj.type for obj in doc.components[2:-2] if obj.type]))
print

dc = sbol.DNAComponent(doc, 'https://blahblahblah.com/1')
dc.type = 'http://purl.obolibrary.org/obo/SO_0000999'
print dc

print doc.components['https://blahblahblah.com/1'].type
exit()


dc.seq = sbol.DNASequence(doc, 'https://blahblahblah.com//sequence')
# Sequence objects are always flushed last from the standard out buffer for some reason...
print dc.seq

dc.seq.nucleotides = 'gggcttcaa'
print dc.seq.nucleotides

# Test remove methods
SA1 = sbol.SequenceAnnotation(doc, 'https://blahblahblah.com//annotation//1')
SA2 = sbol.SequenceAnnotation(doc, 'https://blahblahblah.com//annotation//2')
dc.annotations.append(SA1)
dc.annotations.append(SA2)
print('\tannotations: %d' %len(dc.annotations))
dc.annotations.remove(SA1)
SA2.__del__()
print('\tannotations: %d' %len(dc.annotations))
exit()
# Test subcomponent getter and setter
dc2 = sbol.DNAComponent(doc, 'https://blahblahblah.com/2')
SA.subcomponent = dc2
print SA
# Remove subcomponent by setting equal to None
SA.subcomponent = None
print SA

