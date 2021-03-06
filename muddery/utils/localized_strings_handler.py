"""
This model translates default strings into localized strings.
"""

from evennia.utils import logger
from muddery.worlddata.dao.localized_strings_mapper import LOCALIZED_STRINGS


class LocalizedStringsHandler(object):
    """
    This model translates default strings into localized strings.
    """
    def __init__(self):
        """
        Initialize handler
        """
        self.loaded = False
        self.clear()

    def clear(self):
        """
        Clear data.
        """
        self.dict = {}

    def reload(self):
        """
        Reload local string data.
        """
        self.clear()

        # Load localized string model.
        try:
            for record in LOCALIZED_STRINGS.all():
                # Add db fields to dict. Overwrite system localized strings.
                self.dict[(record.category, record.origin)] = record.local

            self.loaded = True
        except Exception as e:
            print("Can not load custom localized string: %s" % e)

    def translate(self, origin, category="", default=None):
        """
        Translate origin string to local string.
        """
        if not self.loaded:
            self.reload()

        try:
            # Get local string.
            local = self.dict[(category, origin)]
            if local:
                return local
        except:
            pass

        if default is None:
            # Else return origin string.
            return origin
        else:
            return default


# main dialogue handler
LOCALIZED_STRINGS_HANDLER = LocalizedStringsHandler()


# translator
def _(origin, category="", default=None):
    """
    This function returns the localized string.
    """
    return LOCALIZED_STRINGS_HANDLER.translate(origin, category, default)
