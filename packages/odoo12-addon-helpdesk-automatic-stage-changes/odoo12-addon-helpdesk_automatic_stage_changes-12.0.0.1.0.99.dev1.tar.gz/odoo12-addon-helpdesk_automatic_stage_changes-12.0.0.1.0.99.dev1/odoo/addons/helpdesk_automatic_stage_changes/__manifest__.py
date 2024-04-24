# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop Odoo helpdesk automatic stage changes",
    "version": "12.0.0.1.0",
    "depends": [
        "helpdesk_mgmt",
        "web_widget_color",
        "widget_list_row_color",
        "widget_list_limit_cell",
        "helpdesk_cc_and_to_text",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": "Helpdesk automatic stage changes",
    "description": """
Allows the configuration of the stages of a ticket. Customization of colors by
stages and automatic stage changes when receiving or sending a message.
The tickets will have customized colors according to the stage in the tree view.
In the ticket view, the possibility of sending an email from the ticket and a
new tab where the email communications and notes associated with the ticket are
recorded have been added. With the ability to create new notes, reply to a note,
reply to an email without the emails in CC or with those.
Customization of colors depending on the type of communication:
-Black: Incoming message
-Green: Internal note
-Red: Outgoing message
Email sending goes through a new custom view for the helpdesk.ticket model.
    """,
    "data": [
        "data/helpdesk_data.xml",
        "views/template_view.xml",
        "views/helpdesk_ticket_stage_view.xml",
        "views/helpdesk_ticket_view.xml",
        "wizard/mail_compose_message_view.xml",
    ],
    "application": True,
    "installable": True,
    "post_init_hook": "post_install_hook",
}
