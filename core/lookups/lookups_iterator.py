class LookupSingle:
    def __init__(self, id, code):
        self.id = id
        self.code = code


class Users:
    Roles = [
        LookupSingle('a64fc934-fcab-4385-ab67-92f82c805d19', 'ADMIN'),
        LookupSingle('9719d7a0-2753-426d-9474-8aa452c9a0f9', 'REGULAR'),
    ]
    PreferredLanguages = [
        LookupSingle('0fdcf5ba-3250-4811-bf96-ec724dfdf5b4', 'EN'),
        LookupSingle('94bc08dd-7a5c-4bb9-a37a-13de19d051b8', 'RS'),
        LookupSingle('05b7562e-4378-47f7-b9af-a34b107cede8', 'BG'),
        LookupSingle('eafb312a-3380-4475-acdb-1c9874dcde46', 'HR'),
        LookupSingle('84baa252-47a7-40e3-af47-75cffd35ad56', 'SI'),
        LookupSingle('3eaff449-de41-40b1-83bb-83d619c619be', 'DE'),
    ]
    OrganizationTypes = [
        LookupSingle('e0ff844d-3f46-48f6-8894-f29b48665c5c', 'ORGANIZATION_TYPE'),
        LookupSingle('dae0969c-d684-4f2f-82ec-46401e041aa5', 'POSITION'),
        LookupSingle('c87c83b7-1c00-4502-94dd-fe1566035f52', 'CENTRAL_PERSON'),
        LookupSingle('284bc0d5-9e24-43a3-bafc-426dd8717686', 'USER'),
        LookupSingle('c51227b6-c164-4a79-9680-0eb85dfbacaf', 'EMPLOYEE'),
    ]


class ActivityLog:
    MessageTypes = [
        LookupSingle('1a7eff26-2780-4130-9d06-f0ad73b2aa5c', 'FLOW_TYPE_MESSAGE'),
        LookupSingle('7f6f27dc-97ca-4a67-9d32-1841883c0b02', 'FLOW_TYPE_USER_ACTION'),
        LookupSingle('42130ae2-8a45-426e-a06f-a3d4bd53938a', 'FLOW_TYPE_ADMIN_ACTION'),
        LookupSingle('43437153-7da0-4b82-aedf-8d58eecdcfe3', 'FLOW_TYPE_SYSTEM_ACTION'),
    ]
    MessageVisibility = [
        LookupSingle('93aefd06-00ba-4cea-9b81-4d125168de88', 'VISIBLE'),
        LookupSingle('f7e0a642-c5bf-4b29-92d0-ce90e14b2b8c', 'HIDDEN'),
    ]
    MessageImportance = [
        LookupSingle('8321e1c8-591d-442e-8e94-b01dd277c79b', 'REGULAR'),
        LookupSingle('f9860886-b416-4a55-8292-131d4526c67a', 'IMPORTANT'),
    ]


class Lookups:
    Users = Users
    ActivityLog = ActivityLog
