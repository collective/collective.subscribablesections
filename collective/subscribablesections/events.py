from collective.subscribablesections.subtypes import OpenSectionDescriptor, ClosedSectionDescriptor

def reindex_object(event):
    """ Reindex the subtyped object so the list of interfaces are updated in the catalog """

    if type(event.subtype) in (OpenSectionDescriptor, ClosedSectionDescriptor):
        event.object.reindexObject()

