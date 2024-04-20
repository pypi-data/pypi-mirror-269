# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = [
        "product.category",
    ]

    account_ids = fields.One2many(
        string="Account(s)",
        comodel_name="product.category.account",
        inverse_name="product_category_id",
    )

    def _get_account(self, usage_code, local_dict=False):
        self.ensure_one()
        ProductAccount = self.env["product.category.account"]
        result = False

        criteria = [
            ("product_category_id", "=", self.id),
            ("usage_id.code", "=", usage_code),
        ]

        product_accounts = ProductAccount.search(criteria)

        if len(product_accounts) > 0:
            result = product_accounts[0].account_id
        return result

    def _get_tax(self, usage_code, local_dict=False):
        self.ensure_one()
        ProductAccount = self.env["product.category.account"]
        result = []

        criteria = [
            ("product_category_id", "=", self.id),
            ("usage_id.code", "=", usage_code),
        ]

        product_accounts = ProductAccount.search(criteria)

        if len(product_accounts) > 0:
            result = product_accounts[0].tax_ids.ids
        return result
