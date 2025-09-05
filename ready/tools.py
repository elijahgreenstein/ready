"""
Title: Ready Tools
Date Created: 2022-Dec-12
Last Updated: 2022-Dec-12

A set of tools for working with the Ready app in the Django shell.
"""

import uuid
from ready.models import ItemInstance

def repeat(inst_uuid, x_duplicates):
    """Create x number of duplicates of an item instance"""
    iteminstance = ItemInstance.objects.get(id=uuid.UUID(inst_uuid))
    for x in range(x_duplicates):
        iteminstance.pk = None
        iteminstance.save()

def new_id():
    """Return a new UUID"""
    return(uuid.uuid4())

