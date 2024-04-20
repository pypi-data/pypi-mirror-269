# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = [
        "product.product",
    ]

    account_ids = fields.One2many(
        string="Product Account(s)",
        comodel_name="product.account",
        inverse_name="product_id",
    )

    def _get_product_account(self, usage_code, local_dict=False):
        self.ensure_one()
        result = False

        result = self._get_account(usage_code=usage_code)

        if not result:
            result = self.product_tmpl_id._get_account(
                usage_code=usage_code, local_dict=local_dict
            )

        if not result:
            result = self.categ_id._get_account(
                usage_code=usage_code, local_dict=local_dict
            )

        if not result:
            criteria = [("code", "=", usage_code)]
            usage_types = self.env["product.usage_type"].search(criteria)

            if len(usage_types) > 0:
                usage_type = usage_types[0]
                result = usage_type._get_account(local_dict=local_dict)

        return result

    def _get_product_tax(self, usage_code, local_dict=False):
        self.ensure_one()
        result = False

        result = self._get_tax(usage_code=usage_code)

        if not result:
            result = self.product_tmpl_id._get_tax(
                usage_code=usage_code, local_dict=local_dict
            )

        if not result:
            result = self.categ_id._get_tax(
                usage_code=usage_code, local_dict=local_dict
            )

        if not result:
            criteria = [("code", "=", usage_code)]
            usage_types = self.env["product.usage_type"].search(criteria)

            if len(usage_types) > 0:
                usage_type = usage_types[0]
                result = usage_type._get_tax(local_dict=local_dict)

        return result

    def _get_account(self, usage_code, local_dict=False):
        self.ensure_one()
        ProductAccount = self.env["product.account"]
        result = False

        criteria = [("product_id", "=", self.id), ("usage_id.code", "=", usage_code)]

        product_accounts = ProductAccount.search(criteria)

        if len(product_accounts) > 0:
            result = product_accounts[0].account_id
        return result

    def _get_tax(self, usage_code, local_dict=False):
        self.ensure_one()
        ProductAccount = self.env["product.account"]
        result = []

        criteria = [("product_id", "=", self.id), ("usage_id.code", "=", usage_code)]

        product_accounts = ProductAccount.search(criteria)

        if len(product_accounts) > 0:
            result = product_accounts[0].tax_ids.ids
        return result
