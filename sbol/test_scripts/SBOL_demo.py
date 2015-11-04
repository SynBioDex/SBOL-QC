"""
Read an SBOL file and display its contents
"""

# Add SBOL module directory to PYTHONPATH
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import sbol

def populate_subcomponents(parent_component):
    for ann in parent_component.annotations:
        i_start = ann.start - 1
        i_end = ann.end
        sub_seq_nucleotides = parent_component.sequence.nucleotides[i_start:i_end]
        #ann.subComponent = sbol.DNAComponent(doc, '%s//subComponent' %ann.uri)
        ann.subcomponent.sequence = sbol.DNASequence(doc, '%s//Sequence' %ann.subcomponent.uri )
        ann.subcomponent.sequence.nucleotides = sub_seq_nucleotides

def find_sequence_homologs(target_seq):
    result_handle = NCBIWWW.qblast("blastn", "nt", target_seq)
    blast_records = list(NCBIXML.parse(result_handle))
    rec = blast_records[0]

    E_VALUE_THRESH = 0.04
    variant_acc_nos = []
    variant_nucleotides = []
    variant_urls = []
    for alignment in rec.alignments:
        hsp = alignment.hsps[0]  # high-scoring pairs
        variant_acc_nos.append( str(alignment.accession) )
        variant_nucleotides.append( str(hsp.sbjct) )
        #cds_variant_urls.append(alignment.accession)

    return variant_acc_nos, variant_nucleotides, variant_urls

def remove_annotation(parent_component, deleted_ann):
    """ An annotation is removed.  The precedes relationship, start and end indexes of other annotations
    are updated accordingly """

    downstream_ann = deleted_ann.precedes[0]  # Find annotation downstream of the one to be removed

    # Finds the upstream annotation that precedes the annotation to be removed
    for ann in parent_component.annotations:
        if deleted_ann in ann.precedes:
            upstream_ann = ann

    # Update precedes relationship of annotations
    upstream_ann.precedes.remove(upstream_ann.precedes[0])
    upstream_ann.precedes.append(downstream_ann)

    # Update all start and end indices for annotations downstream from insertion
    deletion_size = deleted_ann.end - deleted_ann.start + 1
    while (len(upstream_ann.precedes) > 0):
        downstream_ann = upstream_ann.precedes[0]
        old_start = downstream_ann.start
        old_end = downstream_ann.end
        new_start = old_start - deletion_size
        new_end = old_end - deletion_size
        downstream_ann.start = new_start
        downstream_ann.end = new_end
        upstream_ann = downstream_ann

    #doc.sequences.remove(deleted_ann.subcomponent.sequence)
    #doc.components.remove(deleted_ann.subcomponent)
    #doc.annotations.remove(deleted_ann)
    parent_component.annotations.remove(deleted_ann)


def insert_annotation_downstream(parent_component, upstream_ann, insert_ann):
    """ A new annotation is inserted after an upstream annotation.
    The precedes relationship, start and end indexes are update accordingly.
    The annotation is expected to have a subComponent and Sequence object attached"""
    parent_component.annotations.append(insert_ann)

    # Update start and end of annotation
    insert_size = insert_ann.end
    insert_ann.start = upstream_ann.end + 1
    insert_ann.end = upstream_ann.end + insert_size

    # Update precedes relationship of annotations
    downstream_ann = upstream_ann.precedes[0]  # Assumes annotations only have one precedes relationship
    upstream_ann.precedes.remove(upstream_ann.precedes[0])
    upstream_ann.precedes.append(insert_ann)
    insert_ann.precedes.append(downstream_ann)

    # Update all start and end indices for annotations downstream from insertion
    upstream_ann = insert_ann
    while (len(upstream_ann.precedes) > 0):
        downstream_ann = upstream_ann.precedes[0]
        old_start = downstream_ann.start
        old_end = downstream_ann.end
        new_start = old_start + insert_size
        new_end = old_end + insert_size
        downstream_ann.start = new_start
        downstream_ann.end = new_end
        upstream_ann = downstream_ann

def insert_annotation_upstream(parent_component, insert_ann, downstream_ann):
    """ A new annotation (upstream) is inserted before the downstream annotation
    The precedes relationship, start and end indexes are update accordingly """
    #print downstream_ann.uri
    #print
    for i_ann, ann in enumerate(parent_component.annotations):
        #print i_ann, ann.uri
        if downstream_ann in ann.precedes:
            upstream_uri = ann.uri  # finds the annotation upstream, because it owns the precedes
    print 'Upstream uri: %s' %upstream_uri
    upstream_ann = parent_component.annotations[upstream_uri]
    insert_annotation_downstream(parent_component, upstream_ann, insert_ann)

def assemble_subcomponents(parent_component):
    parent_seq_len = 0
    for ann in parent_component.annotations:
        parent_seq_len = parent_seq_len + len(ann.subcomponent.sequence.nucleotides)
    assembled_seq = 'n' * parent_seq_len
    for ann in parent_component.annotations:
        #assembled_seq[ann.start:ann.end] = ann.subcomponent.sequence.nucleotides
        assembled_seq = assembled_seq[:ann.start - 1] + \
                        ann.subcomponent.sequence.nucleotides + \
                        assembled_seq[ann.end:]
    parent_component.sequence.nucleotides = assembled_seq

def print_downstream_Annotations(ann):
    reader_head = ann
    print reader_head.uri,
    while reader_head.precedes:
        reader_head = reader_head.precedes[0]
        print '->', reader_head.uri,
    print

doc = sbol.Document()
doc.read('test.xml')
progenitor = doc.components[0]

SO_cds = 'http://purl.obolibrary.org/obo/SO_0000316'  # Sequence Ontology uri for CDS
for component in doc.components:
    if component.type == SO_cds: target_cds = component
for ann in doc.annotations:
    if ann.subcomponent == target_cds: target_ann = ann

# print('Total SBOL Objects: %d' %doc.num_sbol_objects)
# print('Collections: %d' %len(doc.collections))
# print('Components: %d' %len(doc.components))
# print('Annotations: %d' %len(doc.annotations))
# print('Sequences: %d' %len(doc.sequences))
#
# for ann in doc.annotations:
#     print ann.start, ann.end
#
# populate_subcomponents(progenitor)




# for i_com in range(len(doc.components)):
#     if doc.components[i_com].type == SO_cds: target_cds = doc.components[i_com]
# for i_ann in range(len(doc.annotations)):
#     if doc.annotations[i_ann].subcomponent == target_cds: target_ann = doc.annotations[i_ann]


# test_ann = sbol.SequenceAnnotation(doc, 'testSA')
# test_ann.start = 1
# test_ann.end = 2
# test_ann.subcomponent = sbol.DNAComponent(doc, 'testDC')
# test_ann.subcomponent.sequence = sbol.DNASequence(doc, 'testSeq')
# test_ann.subcomponent.sequence.nucleotides = 'gc'
# insert_annotation_upstream(progenitor, test_ann, target_ann)
# assemble_subcomponents(progenitor)
#
# print('Total SBOL Objects: %d' %doc.num_sbol_objects)
# print('Collections: %d' %len(doc.collections))
# print('Components: %d' %len(doc.components))
# print('Annotations: %d' %len(doc.annotations))
# print('Sequences: %d' %len(doc.sequences))
# print progenitor.sequence.nucleotides
# for ann in doc.annotations:
#     print ann.start, ann.end
#
# remove_annotation(progenitor, test_ann)
# assemble_subcomponents(progenitor)
#
# print('Total SBOL Objects: %d' %doc.num_sbol_objects)
# print('Collections: %d' %len(doc.collections))
# print('Components: %d' %len(doc.components))
# print('Annotations: %d' %len(doc.annotations))
# print('Sequences: %d' %len(doc.sequences))
# print progenitor.sequence.nucleotides
# for ann in doc.annotations:
#     print ann.start, ann.end

populate_subcomponents(progenitor)

# Import BioPython for BLAST capability
from Bio import Entrez
from Bio.Blast import NCBIWWW, NCBIXML
Entrez.email = "your email here"  # *Always* tell NCBI who you are

variant_acc_nos, variant_nucleotides, variant_urls = find_sequence_homologs(target_cds.sequence.nucleotides)

from copy import copy


print_downstream_Annotations(progenitor.annotations[0])
new_cds = sbol.DNAComponent(doc, '%s_0' %target_cds.uri)
new_cds.display_id = variant_acc_nos[0]
new_cds.sequence = sbol.DNASequence(doc, '%s->Sequence' %new_cds.uri)
new_cds.sequence.nucleotides = variant_nucleotides[0]
new_ann = sbol.SequenceAnnotation(doc, '%s_0' %target_ann.uri)
new_ann.start = 1
new_ann.end = len(new_cds.sequence.nucleotides)
new_ann.subcomponent = new_cds

insert_annotation_downstream(progenitor, target_ann, new_ann)
print_downstream_Annotations(progenitor.annotations[0])

remove_annotation(progenitor, target_ann)
reader_head = progenitor.annotations[0]
print_downstream_Annotations(progenitor.annotations[0])
# for i_variant in range(len(variant_acc_nos))[:3]:
#     print i_variant
#     new_cds = sbol.DNAComponent(doc, '%s_%d' %(target_cds.uri, i_variant))
#     new_cds.name = variant_acc_nos[i_variant]
#     new_cds.display_id = variant_acc_nos[i_variant]
#     new_cds.sequence = sbol.DNASequence(doc, '%s->Sequence' %new_cds.uri)
#     new_cds.sequence.nucleotides = variant_nucleotides[i_variant]
#     new_ann = sbol.SequenceAnnotation(doc, '%s_%d' %(target_ann.uri, i_variant))
#     new_ann.start = 1
#     new_ann.end = len(new_cds.sequence.nucleotides)
#     new_ann.subcomponent = new_cds
#     new_ann.precedes = target_ann.precedes
#     print target_ann
#     print 'Parent'
#     for i_ann, ann in enumerate(progenitor.annotations):
#         print ann.uri, '->',
#     variant = copy(progenitor)
#     print '\nParent - Copy'
#     for i_ann, ann in enumerate(variant.annotations):
#         print ann.uri, '->',
#     insert_annotation_upstream(variant, new_ann, target_ann)
#     print '\nVariant'
#     for i_ann, ann in enumerate(variant.annotations):
#         print ann.uri, '->',
#     exit()
#     remove_annotation(variant, target_ann)#deleteAnnotation
#     for i_ann, ann in enumerate(variant.annotations):
#         print ann.uri, '->',
#     assemble_subcomponents(variant)


"""Annotates Entrez Gene IDs using Bio.Entrez, in particular epost (to
submit the data to NCBI) and esummary to retrieve the information.
Returns a list of dictionaries with the annotations."""

# request = Entrez.epost("gene",id=",".join(id_list))
# try:
#     result = Entrez.read(request)
# except RuntimeError as e:
#     #FIXME: How generate NAs instead of causing an error with invalid IDs?
#     print "An error occurred while retrieving the annotations."
#     print "The error returned was %s" % e
#     sys.exit(-1)
#
# webEnv = result["WebEnv"]
# queryKey = result["QueryKey"]
# data = Entrez.esummary(db="gene", webenv=webEnv, query_key =
#         queryKey)
# annotations = Entrez.read(data)
#
# print "Retrieved %d annotations for %d genes" % (len(annotations),
#         len(id_list))




