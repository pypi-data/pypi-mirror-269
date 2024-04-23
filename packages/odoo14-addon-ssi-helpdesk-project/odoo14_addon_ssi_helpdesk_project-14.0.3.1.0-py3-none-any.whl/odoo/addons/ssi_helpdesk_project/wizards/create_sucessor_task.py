# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CreateSucessorTaskDetail(models.TransientModel):
    _name = "create_sucessor_task_detail"
    _inherit = "create_sucessor_task_detail"

    def _prepare_task_creation_value(self):
        _super = super(CreateSucessorTaskDetail, self)
        result = _super._prepare_task_creation_value()
        task = self.wizard_id.task_id
        result.update({"ticket_ids": [(6, 0, task.ticket_ids.ids)]})
        return result
