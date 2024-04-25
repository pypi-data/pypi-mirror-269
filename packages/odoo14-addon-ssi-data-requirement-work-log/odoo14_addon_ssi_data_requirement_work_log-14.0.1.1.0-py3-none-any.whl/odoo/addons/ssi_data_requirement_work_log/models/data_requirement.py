# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class DataRequirement(models.Model):
    _name = "data_requirement"
    _inherit = [
        "data_requirement",
        "mixin.work_object",
    ]

    _work_log_create_page = True
