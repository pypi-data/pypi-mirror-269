# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HelpdeskTypeTask(models.Model):
    _name = "helpdesk_type.task"
    _description = "Helpdesk Type - Task"

    type_id = fields.Many2one(
        string="Helpdesk Type",
        comodel_name="helpdesk_type",
        required=True,
        ondelete="cascade",
    )
    title = fields.Char(
        string="Task Summary",
        required=True,
    )
    task_type_id = fields.Many2one(
        string="Task Type",
        comodel_name="task.type",
    )
    user_id = fields.Many2one(
        string="Assigned To",
        comodel_name="res.users",
    )

    def _create_task(self, ticket):
        self.ensure_one()
        Task = self.env["project.task"]
        Task.create(self._prepare_task_data(ticket))

    def _prepare_task_data(self, ticket):
        self.ensure_one()
        return {
            "project_id": ticket.project_id.id,
            "name": self.title,
            "type_id": self.task_type_id and self.task_type_id.id or False,
            "user_id": self.user_id and self.user_id.id or False,
            "ticket_ids": [(6, 0, [ticket.id])],
        }
