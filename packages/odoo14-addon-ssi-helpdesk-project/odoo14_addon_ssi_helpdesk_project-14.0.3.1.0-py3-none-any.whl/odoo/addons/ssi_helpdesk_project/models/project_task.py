# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = [
        "project.task",
    ]

    ticket_ids = fields.Many2many(
        string="Tickets",
        comodel_name="helpdesk_ticket",
        relation="rel_helpdesk_ticket_2_task",
        column1="task_id",
        column2="ticket_id",
    )

    @api.depends(
        "ticket_ids",
        "ticket_ids.date_deadline",
        "ticket_ids.state",
    )
    def _compute_ticket_deadline(self):
        for record in self:
            if record.ticket_ids:
                ticket_deadline = (
                    record.ticket_ids.filtered(
                        lambda x: x.date_deadline is not False
                        and x.state not in ["cancel", "done", "rejected"]
                    )
                    .sorted("date_deadline")
                    .mapped("date_deadline")
                )
                if ticket_deadline:
                    record.ticket_deadline = ticket_deadline[0]
                else:
                    record.ticket_deadline = False
            else:
                record.ticket_deadline = False

    ticket_deadline = fields.Date(
        string="Ticket Deadline",
        compute="_compute_ticket_deadline",
        store=True,
    )

    def action_open_ticket(self):
        self.ensure_one()
        return self.sudo()._open_ticket()

    def _open_ticket(self):
        waction = self.env.ref("ssi_helpdesk.helpdesk_ticket_action").read()[0]
        waction.update(
            {
                "view_mode": "tree,form",
                "domain": [("id", "in", self.ticket_ids.ids)],
                "context": {
                    "default_project_id": self.project_id.id,
                    "default_task_ids": self.ids,
                },
            }
        )
        return waction
