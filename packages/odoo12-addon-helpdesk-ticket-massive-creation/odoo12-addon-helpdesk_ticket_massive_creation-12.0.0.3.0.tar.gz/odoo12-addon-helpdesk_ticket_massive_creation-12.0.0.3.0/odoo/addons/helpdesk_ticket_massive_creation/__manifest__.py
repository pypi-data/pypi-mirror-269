# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "12.0.0.3.0",
    "name": "Massive ticket creation from selected partners",
    "depends": [
        "helpdesk_mgmt",
        "contacts",
        "helpdesk_ticket_contract_contract",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Create helpdesk tickets massively, from multiple preselected partners.
    """,
    "data": [
        "wizards/helpdesk_ticket_massive_creation/helpdesk_ticket_massive_creation.xml"  # noqa
    ],
    "demo": [],
    "application": True,
    "installable": True,
}
