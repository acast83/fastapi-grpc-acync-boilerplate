import uuid
import json
from enum import Enum


class Users:
    class Roles(Enum):
        ADMIN = 'a64fc934-fcab-4385-ab67-92f82c805d19'
        REGULAR = '9719d7a0-2753-426d-9474-8aa452c9a0f9'

    class PreferredLanguages(Enum):
        EN = '0fdcf5ba-3250-4811-bf96-ec724dfdf5b4'
        RS = '94bc08dd-7a5c-4bb9-a37a-13de19d051b8'
        BG = '05b7562e-4378-47f7-b9af-a34b107cede8'
        HR = 'eafb312a-3380-4475-acdb-1c9874dcde46'
        SI = '84baa252-47a7-40e3-af47-75cffd35ad56'
        DE = '3eaff449-de41-40b1-83bb-83d619c619be'

    class OrganizationTypes(Enum):
        ORGANIZATION_TYPE = 'e0ff844d-3f46-48f6-8894-f29b48665c5c'
        POSITION = 'dae0969c-d684-4f2f-82ec-46401e041aa5'
        CENTRAL_PERSON = 'c87c83b7-1c00-4502-94dd-fe1566035f52'
        USER = '284bc0d5-9e24-43a3-bafc-426dd8717686'
        EMPLOYEE = 'c51227b6-c164-4a79-9680-0eb85dfbacaf'

    Roles = Roles
    PreferredLanguages = PreferredLanguages
    OrganizationTypes = OrganizationTypes


class ActivityLog:
    class MessageTypes(Enum):
        FLOW_TYPE_MESSAGE = '1a7eff26-2780-4130-9d06-f0ad73b2aa5c'
        FLOW_TYPE_USER_ACTION = '7f6f27dc-97ca-4a67-9d32-1841883c0b02'
        FLOW_TYPE_ADMIN_ACTION = '42130ae2-8a45-426e-a06f-a3d4bd53938a'
        FLOW_TYPE_SYSTEM_ACTION = '43437153-7da0-4b82-aedf-8d58eecdcfe3'

    class MessageVisibility(Enum):
        VISIBLE = '93aefd06-00ba-4cea-9b81-4d125168de88'
        HIDDEN = 'f7e0a642-c5bf-4b29-92d0-ce90e14b2b8c'

    class MessageImportance(Enum):
        REGULAR = '8321e1c8-591d-442e-8e94-b01dd277c79b'
        IMPORTANT = 'f9860886-b416-4a55-8292-131d4526c67a'

    MessageTypes = MessageTypes
    MessageVisibility = MessageVisibility
    MessageImportance = MessageImportance


class Lookups:

    Users = Users
    ActivityLog = ActivityLog


class RevLookupsSingle:
    def __init__(self, code, id):
        self.code = code
        self.id = id

    class LookupsReversed:
        _instance = None
        _instance_obj = None

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                with open("reversed_lookups.json") as file:
                    cls._instance = json.load(file)
            return cls._instance

        @classmethod
        def get_instance_obj(cls):
            if not cls._instance_obj:
                cls._instance_obj = {}
                with open("reversed_lookups.json") as file:
                    data = json.load(file)
                for k in data:
                    cls._instance_obj[k] = RevLookupsSingle(**data[k])
                    cls._instance_obj[uuid.UUID(k)] = RevLookupsSingle(**data[k])

            return cls._instance_obj
