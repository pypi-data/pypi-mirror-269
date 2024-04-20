# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductUsage(models.Model):
    _name = "product.usage_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Product Usage Type"

    selection_method = fields.Selection(
        string="Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        required=True,
        default="fixed",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        company_dependent=True,
    )
    tax_selection_method = fields.Selection(
        string="Tax Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        required=True,
        default="fixed",
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_usage_type_2_tax",
        column1="usage_type_id",
        column2="tax_id",
    )

    def _get_account(self, local_dict=False):
        self.ensure_one()
        return self.account_id

    def _get_tax(self, local_dict=False):
        self.ensure_one()
        return self.tax_ids.ids
