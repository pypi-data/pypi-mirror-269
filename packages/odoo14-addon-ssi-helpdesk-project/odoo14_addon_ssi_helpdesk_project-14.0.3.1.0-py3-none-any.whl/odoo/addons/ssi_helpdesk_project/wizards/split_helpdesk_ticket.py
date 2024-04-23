# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SplitHelpdeskTicket(models.TransientModel):
    _name = "split_helpdesk_ticket"
    _inherit = "split_helpdesk_ticket"

    def _run_ticket_onchange(self):
        self.ensure_one()
        _super = super(SplitHelpdeskTicket, self)
        _super._run_ticket_onchange()
        self.result_ticket_id.onchange_need_task()
