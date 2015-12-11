"""
Quests

The quest class represents the character's quest. Each quest is a quest object stored
in the character. It controls quest's objectives.

"""

from muddery.utils import defines
from muddery.typeclasses.objects import MudderyObject
from muddery.utils.script_handler import SCRIPT_HANDLER
from muddery.utils.dialogue_handler import DIALOGUE_HANDLER
from muddery.utils.localized_strings_handler import LS
from django.conf import settings
from django.db.models.loading import get_model
from evennia.utils import logger


class MudderyQuest(MudderyObject):
    """
    This class controls quest's objectives. Hooks are called when a character doing some things.
    """
    def at_object_creation(self):
        """
        Set achieved objectives to empty.
        """
        self.db.owner = None
        self.db.achieved = {}


    def set_owner(self, owner):
        """
        Set the owner of the skill.
        """
        self.db.owner = owner


    def load_data(self):
        """
        Load quest's data from db.
        """
        super(MudderyQuest, self).load_data()

        self.objectives = {}
        self.not_achieved = {}
        
        key = self.get_info_key()
        if not key:
            return

        # Get objectives.
        obj_records = []
        model_objectives = get_model(settings.WORLD_DATA_APP, settings.QUEST_OBJECTIVES)
        if model_objectives:
            # Get records.
            obj_records = model_objectives.objects.filter(quest=key)

        for obj_record in obj_records:
            objective = {"ordinal": obj_record.ordinal,
                         "type": obj_record.type,
                         "object": obj_record.object,
                         "number": obj_record.number,
                         "desc": obj_record.desc}
            self.objectives[obj_record.ordinal] = objective

            achieved = self.db.achieved.get(key, 0)
            if achieved < obj_record.number:
                if not obj_record.type in self.not_achieved:
                    self.not_achieved[obj_record.type] = [obj_record.ordinal]
                else:
                    self.not_achieved[obj_record.type].append(obj_record.ordinal)


    def return_objectives(self):
        """
        Get the information of all objectives.
        Set desc to an objective can hide the details of the objective.
        """
        objectives = []
        for ordinal in self.objectives:
            desc = self.objectives[ordinal]["desc"]
            if desc:
                # If an objective has desc, use its desc.
                objectives.append({"desc": self.objectives[ordinal]["desc"]})
            else:
                # Or make a desc by other data.
                obj_num = self.objectives[ordinal]["number"]
                achieved = self.db.achieved.get(ordinal, 0)
                
                if self.objectives[ordinal]["type"] == defines.OBJECTIVE_TALK:
                    # talking
                    target = LS("Talk to")
                    name = DIALOGUE_HANDLER.get_npc_name(self.objectives[ordinal]["object"])
        
                    objectives.append({"target": target,
                                       "object": name,
                                       "achieved": achieved,
                                       "total": obj_num,
                                       })
                elif self.objectives[ordinal]["type"] == defines.OBJECTIVE_OBJECT:
                    # getting
                    target = LS("Get")
                    name = ""
                    
                    # Get the name of the objective object.
                    for model_name in settings.COMMON_OBJECTS:
                        model = get_model(settings.WORLD_DATA_APP, model_name)
                        if model:
                            # Get record.
                            try:
                                record = model.objects.get(key=self.objectives[ordinal]["object"])
                                name = record.name
                                break
                            except Exception, e:
                                pass
        
                    objectives.append({"target": target,
                                       "object": name,
                                       "achieved": achieved,
                                       "total": obj_num,
                                       })
                elif self.objectives[ordinal]["type"] == defines.OBJECTIVE_KILL:
                    # getting
                    target = LS("Kill")
                    name = ""

                    # Get the name of the objective character.
                    for model_name in settings.COMMON_OBJECTS:
                        # find in common objects
                        model = get_model(settings.WORLD_DATA_APP, model_name)
                        if model:
                            # Get record.
                            try:
                                record = model.objects.get(key=self.objectives[ordinal]["object"])
                                name = record.name
                                break
                            except Exception, e:
                                pass

                    if not name:
                        # find in world_npcs
                        for model_name in settings.WORLD_NPCS:
                            # find in common objects
                            model = get_model(settings.WORLD_DATA_APP, model_name)
                            if model:
                                # Get record.
                                try:
                                    record = model.objects.get(key=self.objectives[ordinal]["object"])
                                    name = record.name
                                    break
                                except Exception, e:
                                    pass

                    objectives.append({"target": target,
                                       "object": name,
                                       "achieved": achieved,
                                       "total": obj_num,
                                       })

        return objectives


    def is_achieved(self):
        """
        Check all objectives are achieved or not.
        """
        for ordinal in self.objectives:
            obj_num = self.objectives[ordinal]["number"]
            achieved = self.db.achieved.get(ordinal, 0)
    
            if achieved < obj_num:
                return False

        return True


    def finish(self):
        """
        Finish a quest, do its action.
        """
        owner = self.db.owner

        # do quest's action
        if self.action:
            SCRIPT_HANDLER.do_action(caller, None, self.action)

        # remove objective objects
        obj_list = []
        for ordinal in self.objectives:
            if self.objectives[ordinal]["type"] == defines.OBJECTIVE_OBJECT:
                obj_list.append({"object": self.objectives[ordinal]["object"],
                                 "number": self.objectives[ordinal]["number"]})
        if obj_list:
            owner.remove_objects(obj_list)


    def at_objective(self, type, object_key, number=1):
        """
        Called when the owner may finish some objectives.
        
        args:
            type: objective's type defined in defines.py
            object_key(string): the key of the relative object
            number(int): the number of the object
        """
        if not type in self.not_achieved:
            return False

        status_changed = False
        index = 0

        # search all object objectives
        while index < len(self.not_achieved[type]):
            ordinal = self.not_achieved[type][index]
            index += 1

            if self.objectives[ordinal]["object"] == object_key:
                # if this object matches an objective
                status_changed = True

                # add achieved number
                achieved = self.db.achieved.get(ordinal, 0)
                achieved += number
                self.db.achieved[ordinal] = achieved

                if self.db.achieved[ordinal] >= self.objectives[ordinal]["number"]:
                    # if this objective is achieved, remove it
                    index -= 1
                    del(self.not_achieved[type][index])
                                                                    
                    if not self.not_achieved[type]:
                        # if all objectives are achieved
                        del(self.not_achieved[type])
                        break
                                                                                
        return status_changed
