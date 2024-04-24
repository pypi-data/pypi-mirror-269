# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    action_user_odoo = fields.Selection(
        selection=[
            ("0", _("Open new ticket")),
            ("1", _("Change stage")),
        ],
        string="Action when a user responds",
    )

    change_stage_to_id = fields.Many2one(
        "helpdesk.ticket.stage", string="Change stage to"
    )

    when_odoo_responds_change_stage_to_id = fields.Many2one(
        "helpdesk.ticket.stage", string="Change stage to (When Som Connection responds)"
    )

    color_row = fields.Char("Color Row", default="#000000")

    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")

    message_emails_ids = fields.One2many(
        "mail.message", compute="_compute_emails", string="Messages"
    )

    # Load certain types of messages
    @api.one
    @api.depends("message_ids")
    def _compute_emails(self):
        self.message_emails_ids = [
            msg_id.id
            for msg_id in self.message_ids
            if msg_id.message_type in ("email", "comment")
        ]

    # Update stage values when creating the ticket
    @api.model
    def create(self, vals):
        ticket = super().create(vals)
        if ticket.stage_id:
            stage_obj = self.env["helpdesk.ticket.stage"].browse([ticket.stage_id.id])
            ticket.write(
                {
                    "action_user_odoo": stage_obj.action_user_odoo,
                    "change_stage_to_id": stage_obj.change_stage_to_id.id,
                    "when_odoo_responds_change_stage_to_id": stage_obj.when_odoo_responds_change_stage_to_id.id,  # noqa: E501
                    "color_row": stage_obj.color_row,
                    "color_background_row": stage_obj.color_background_row,
                }
            )
        return ticket

    # Update stage values when updating the ticket
    @api.multi
    def write(self, vals):
        for ticket in self:
            if vals.get("stage_id"):
                stage_obj = self.env["helpdesk.ticket.stage"].browse([vals["stage_id"]])
                vals["action_user_odoo"] = stage_obj.action_user_odoo
                vals["change_stage_to_id"] = stage_obj.change_stage_to_id.id
                vals[
                    "when_odoo_responds_change_stage_to_id"
                ] = stage_obj.when_odoo_responds_change_stage_to_id.id
                vals["color_row"] = stage_obj.color_row
                vals["color_background_row"] = stage_obj.color_background_row
        return super().write(vals)

    # Open new communication sales according to requirements
    def mail_compose_message_action(self):
        action = self.env.ref(
            "helpdesk_automatic_stage_changes."
            "action_email_compose_message_automatic_stage_changes_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_when_odoo_responds_change_stage_to_id": self.when_odoo_responds_change_stage_to_id  # noqa: E501
                and self.when_odoo_responds_change_stage_to_id.id
                or False,
                "default_template_id": self.env.ref(
                    "helpdesk_automatic_stage_changes.created_response_ticket_template"
                ).id
                or False,
                "default_email_cc": self.email_cc,
                "default_email_to": self.partner_email,
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
            }
        )
        action["context"] = ctx
        return action

    # Open new communication sales according to requirements
    def mail_compose_message_action_note(self):
        action = self.env.ref(
            "helpdesk_automatic_stage_changes."
            "action_email_compose_message_automatic_stage_changes_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "comment",
                "default_is_log": True,
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "default_subject": self.name,
            }
        )
        action["context"] = ctx
        return action
