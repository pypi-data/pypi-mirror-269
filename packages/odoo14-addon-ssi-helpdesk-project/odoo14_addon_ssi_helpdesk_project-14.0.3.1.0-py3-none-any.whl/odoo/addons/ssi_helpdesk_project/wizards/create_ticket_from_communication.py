# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CreateTicketFromCommunication(models.TransientModel):
    _name = "create_ticket_from_communication"
    _inherit = "create_ticket_from_communication"
    _description = "Create Ticket From Communication"

    def _run_ticket_onchange(self):
        self.ensure_one()
        _super = super(CreateTicketFromCommunication, self)
        _super._run_ticket_onchange()
        self.communication_id.ticket_id.onchange_need_task()
