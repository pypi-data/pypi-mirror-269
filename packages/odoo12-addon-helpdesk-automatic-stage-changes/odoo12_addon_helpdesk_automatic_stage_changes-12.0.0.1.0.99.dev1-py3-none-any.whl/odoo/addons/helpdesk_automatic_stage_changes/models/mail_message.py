# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields, _
import base64


class Message(models.Model):
    """Messages model: system notification (replacing res.log notifications),
    comments (OpenChatter discussion) and incoming emails."""

    _inherit = "mail.message"

    color_row = fields.Char("Color Row", default="#000000")

    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")

    date_subject = fields.Text("Date/Subject", compute="_compute_date_subject")

    message_type_mail = fields.Selection(
        selection=[
            ("email_sent", _("Mail sent")),
            ("email_received", _("Email received")),
            ("note", _("Note")),
        ],
        string="Message type",
    )

    @api.one
    @api.depends("date", "subject")
    def _compute_date_subject(self):
        self.date_subject = (
            f" {self.date.strftime('%Y-%m-%d %H:%M:%S')} \n" f" {self.subject}"
        )

    # New actions and updates when creating a new message
    @api.model
    def create(self, values):
        if values.get("model") and values.get("res_id"):
            if values.get("model") == "helpdesk.ticket":
                ticket = self.env["helpdesk.ticket"].browse(values.get("res_id"))
                if ticket:
                    if values.get("message_type") == "email":
                        if (
                            values.get("email_from")
                            and ticket.partner_email
                            and ticket.partner_email in values.get("email_from")
                        ):
                            values["message_type_mail"] = "email_received"
                            values["color_row"] = "#FFFFFF"
                            values["color_background_row"] = "#000000"
                        else:
                            values["message_type_mail"] = "email_sent"
                            values["color_row"] = "#FFFFFF"
                            values["color_background_row"] = "#FF0000"
                    elif values.get("message_type") == "comment":
                        values["message_type_mail"] = "note"
                        values["color_row"] = "#000000"
                        values["color_background_row"] = "#23FF00"
                    if (
                        values.get("email_from")
                        and ticket.partner_email
                        and ticket.partner_email in values.get("email_from")
                        and values.get("message_type") == "email"
                    ):
                        if ticket.action_user_odoo == "0":
                            vals = {
                                "partner_name": ticket.partner_name,
                                "company_id": ticket.company_id.id,
                                "category_id": ticket.category_id.id,
                                "partner_email": ticket.partner_email,
                                "description": values.get("body"),
                                "name": ticket.name,
                                "attachment_ids": False,
                                "channel_id": ticket.channel_id.id,
                                "partner_id": ticket.partner_id.id,
                            }
                            new_ticket = self.env["helpdesk.ticket"].sudo().create(vals)
                            new_ticket.message_subscribe(
                                partner_ids=self.env.user.partner_id.ids
                            )
                            if values.get("attachment_ids"):
                                for c_file in values.get("attachment_ids"):
                                    data = c_file.read()
                                    if c_file.filename:
                                        self.env["ir.attachment"].sudo().create(
                                            {
                                                "name": c_file.filename,
                                                "datas": base64.b64encode(data),
                                                "datas_fname": c_file.filename,
                                                "res_model": "helpdesk.ticket",
                                                "res_id": new_ticket.id,
                                            }
                                        )
                        elif (
                            ticket.action_user_odoo == "1" and ticket.change_stage_to_id
                        ):
                            ticket.write({"stage_id": ticket.change_stage_to_id.id})
        return super(Message, self).create(values)

    def mail_compose_action(self):
        if self.message_type == "email":
            return self.mail_compose_message_action()
        elif self.message_type == "comment":
            return self.mail_compose_message_action_note()
        else:
            return False

    # Open new communication sales according to requirements
    def mail_compose_message_action(self):
        action = self.env.ref(
            "helpdesk_automatic_stage_changes."
            "action_email_compose_message_automatic_stage_changes_wizard"
        ).read()[0]
        action.update({"src_model": "helpdesk.ticket"})
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_email_from": self.env.user.company_id.email,
                "default_email_to": self.email_from,
                "default_no_atuto_thread": True,
                "default_reply_to": self.email_from,
                "default_parent_id": self.id,
                "default_body": f"\n\n\n---- [{self.date}] {self.email_from} :\n"
                + self.body,
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
            }
        )
        if self.model == "helpdesk.ticket":
            ticket = self.env["helpdesk.ticket"].browse(self.res_id)
            ctx.update(
                {
                    "default_when_odoo_responds_change_stage_to_id": ticket.when_odoo_responds_change_stage_to_id  # noqa: E501
                    and ticket.when_odoo_responds_change_stage_to_id.id
                    or False,
                    "default_subject": self.subject
                    if "Re:" in self.subject
                    else f"Re:[{ticket.number}] {self.subject}",  # noqa: E501
                }
            )

        action["context"] = ctx
        return action

    # Open new communication sales according to requirements
    def mail_compose_message_action_all(self):
        action = self.env.ref(
            "helpdesk_automatic_stage_changes."
            "action_email_compose_message_automatic_stage_changes_wizard"
        ).read()[0]
        action.update({"src_model": "helpdesk.ticket"})
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_email_cc": self.origin_email_cc,
                "default_email_from": self.env.user.company_id.email,
                "default_email_to": self.email_from,
                "default_no_atuto_thread": True,
                "default_reply_to": self.email_from,
                "default_parent_id": self.id,
                "default_body": f"\n\n\n---- [{self.date}] {self.email_from} :\n"
                + self.body,
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
            }
        )
        if self.model == "helpdesk.ticket":
            ticket = self.env["helpdesk.ticket"].browse(self.res_id)
            ctx.update(
                {
                    "default_when_odoo_responds_change_stage_to_id": ticket.when_odoo_responds_change_stage_to_id  # noqa: E501
                    and ticket.when_odoo_responds_change_stage_to_id.id
                    or False,
                    "default_subject": self.subject
                    if "Re:" in self.subject
                    else f"Re:[{ticket.number}] {self.subject}",  # noqa: E501
                }
            )
        action["context"] = ctx
        return action

    # Open new communication sales according to requirements
    def mail_compose_message_action_resend(self):
        action = self.env.ref(
            "helpdesk_automatic_stage_changes."
            "action_email_compose_message_automatic_stage_changes_wizard"
        ).read()[0]
        action.update({"src_model": "helpdesk.ticket"})
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_email_from": self.env.user.company_id.email,
                "default_no_atuto_thread": True,
                "default_parent_id": self.id,
                "default_body": f"\n\n\n---- [{self.date}] {self.email_from} :\n"
                + self.body,
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
            }
        )
        if self.model == "helpdesk.ticket":
            ticket = self.env["helpdesk.ticket"].browse(self.res_id)
            ctx.update(
                {
                    "default_when_odoo_responds_change_stage_to_id": ticket.when_odoo_responds_change_stage_to_id  # noqa: E501
                    and ticket.when_odoo_responds_change_stage_to_id.id
                    or False,
                    "default_subject": self.subject
                    if "Re:" in self.subject
                    else f"Re:[{ticket.number}] {self.subject}",
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
                "default_body": f"\n\n\n---- [{self.date}] {self.email_from} :\n"
                + self.body,
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
                "default_subject": self.subject,
            }
        )
        action["context"] = ctx
        return action
