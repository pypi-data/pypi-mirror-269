# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class DataRequirementPackage(models.Model):
    _name = "data_requirement_package"
    _inherit = [
        "data_requirement_package",
        "mixin.work_object",
    ]

    _work_log_create_page = True
