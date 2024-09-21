{
    "name": "Hospital App System",
    "summary": "",
    "description": """This Hospital App System for managing doctors, patients and departments.""",
    "author": "Stephania Ehab",
    "category": "",
    "version": "17.0.0.1.0",
    "depends": ['base'],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'wizard/add_history_wizard_view.xml',

    ]
}