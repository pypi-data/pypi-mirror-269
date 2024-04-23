# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _name = "helpdesk_ticket"
    _inherit = [
        "helpdesk_ticket",
    ]

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )
    need_task = fields.Boolean(
        string="Need Task",
        default=False,
    )
    task_block = fields.Boolean(
        string="Task Block",
        compute="_compute_task",
        store=True,
    )
    task_ids = fields.Many2many(
        string="Tasks",
        comodel_name="project.task",
        relation="rel_helpdesk_ticket_2_task",
        column1="ticket_id",
        column2="task_id",
        copy=False,
    )
    total_task = fields.Integer(
        string="Total Task",
        compute="_compute_task",
        store=True,
    )
    task_draft_count = fields.Integer(
        string="Task Draft Count",
        compute="_compute_task",
        store=True,
    )
    task_open_count = fields.Integer(
        string="Task Open Count",
        compute="_compute_task",
        store=True,
    )
    task_done_count = fields.Integer(
        string="Task Done Count",
        compute="_compute_task",
        store=True,
    )
    task_pending_count = fields.Integer(
        string="Task Pending Count",
        compute="_compute_task",
        store=True,
    )
    task_no_state_count = fields.Integer(
        string="Task No State Count",
        compute="_compute_task",
        store=True,
    )
    task_done = fields.Boolean(
        string="Task Done",
        compute="_compute_task",
        store=True,
    )
    timebox_latest_id = fields.Many2one(
        string="Letest Timebox",
        comodel_name="task.timebox",
        compute="_compute_timebox",
        store=True,
    )
    timebox_latest_date_start = fields.Date(
        string="Latest Timebox Date Start",
        compute="_compute_timebox",
        store=True,
    )
    timebox_latest_date_end = fields.Date(
        string="Lates Timebox Date End",
        compute="_compute_timebox",
        store=True,
    )
    timebox_initial_id = fields.Many2one(
        string="Timebox Initial",
        comodel_name="task.timebox",
        compute="_compute_timebox",
        store=True,
    )
    timebox_initial_date_start = fields.Date(
        string="Timebox Initial Date Start",
        compute="_compute_timebox",
        store=True,
    )
    timebox_initial_date_end = fields.Date(
        string="Timebox Initial Date End",
        compute="_compute_timebox",
        store=True,
    )

    @api.depends(
        "task_ids",
        "task_ids.stage_id",
        "task_ids.state",
        "task_ids.kanban_state",
    )
    def _compute_task(self):
        for record in self:
            total_task = (
                task_no_state_count
            ) = (
                task_draft_count
            ) = task_open_count = task_done_count = task_pending_count = 0
            task_done = False
            task_block = False
            if record.task_ids:
                for task in record.task_ids:
                    total_task += 1
                    if task.state == "draft":
                        task_draft_count += 1
                    elif task.state == "open":
                        task_open_count += 1
                    elif task.state == "done":
                        task_done_count += 1
                    elif task.state == "pending":
                        task_pending_count += 1
                    else:
                        task_no_state_count += 1

                    if task.kanban_state == "blocked":
                        task_block = True
                if total_task == task_done_count:
                    task_done = True
            record.total_task = total_task
            record.task_draft_count = task_draft_count
            record.task_open_count = task_open_count
            record.task_done_count = task_done_count
            record.task_no_state_count = task_no_state_count
            record.task_pending_count = task_pending_count
            record.task_done = task_done
            record.task_block = task_block

    @api.depends(
        "task_ids",
        "task_ids.timebox_latest_id",
        "task_ids.timebox_date_start",
        "task_ids.timebox_date_end",
        "task_ids.timebox_initial_id",
        "task_ids.timebox_initial_date_start",
        "task_ids.timebox_initial_date_end",
        "task_ids.timebox_upcoming_id",
        "task_ids.timebox_upcoming_date_start",
        "task_ids.timebox_upcoming_date_end",
    )
    def _compute_timebox(self):
        for document in self:
            timebox_latest_id = (
                timebox_latest_date_start
            ) = (
                timebox_latest_date_end
            ) = (
                timebox_initial_id
            ) = timebox_initial_date_start = timebox_initial_date_end = False

            if document.task_ids:
                tasks = document.task_ids
                latest_sorted = tasks.sorted(key=lambda r: r.timebox_latest_id)
                timebox_latest_id = latest_sorted[0].timebox_latest_id
                timebox_latest_date_start = timebox_latest_id.date_start
                timebox_latest_date_end = timebox_latest_id.date_end
                initial_sorted = tasks.sorted(key=lambda r: r.timebox_initial_id)
                timebox_initial_id = initial_sorted[-1].timebox_initial_id
                timebox_initial_date_start = timebox_initial_id.date_start
                timebox_initial_date_end = timebox_initial_id.date_end

            document.timebox_latest_id = timebox_latest_id
            document.timebox_latest_date_start = timebox_latest_date_start
            document.timebox_latest_date_end = timebox_latest_date_end
            document.timebox_initial_id = timebox_initial_id
            document.timebox_initial_date_start = timebox_initial_date_start
            document.timebox_initial_date_end = timebox_initial_date_end

    def action_open_task(self):
        for record in self.sudo():
            result = record._open_task()
        return result

    def action_create_task(self):
        for record in self.sudo():
            record._create_task()

    def _create_task(self):
        self.ensure_one()

        if not self.project_id:
            return True

        for task_template in self.type_id.task_ids:
            task_template._create_task(self)

    def _open_task(self):
        waction = self.env.ref("project.action_view_all_task").read()[0]
        waction.update(
            {
                "view_mode": "tree,form",
                "domain": [("id", "in", self.task_ids.ids)],
                "context": {},
            }
        )
        return waction

    @api.onchange(
        "type_id",
    )
    def onchange_need_task(self):
        if self.type_id:
            self.need_task = self.type_id.need_task
