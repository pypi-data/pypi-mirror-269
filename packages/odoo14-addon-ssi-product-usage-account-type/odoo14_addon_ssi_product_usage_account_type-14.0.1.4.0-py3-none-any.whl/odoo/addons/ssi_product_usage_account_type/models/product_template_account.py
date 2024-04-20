# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateAccount(models.Model):
    _name = "product.template.account"
    _description = "Product Template Accounts"

    product_template_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
        required=True,
        ondelete="cascade",
    )
    usage_id = fields.Many2one(
        string="Usage",
        comodel_name="product.usage_type",
        required=True,
        ondelete="restrict",
    )
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
        relation="rel_product_template_account_2_tax",
        column1="product_template_account_id",
        column2="tax_id",
    )

    @api.constrains(
        "usage_id",
        "product_template_id",
    )
    def constrains_no_duplicate(self):
        for record in self:
            if not record._check_no_duplicate():
                error_message = _(
                    """
                Context: Add/Update product account configuration
                Database ID: %s
                Problem: Duplicate configuration
                Solution: Remove duplicate entry
                """
                    % (record.id)
                )
                raise ValidationError(error_message)

    def _check_no_duplicate(self):
        self.ensure_one()
        result = True
        ProductAccount = self.env["product.template.account"]
        criteria = [
            ("id", "!=", self.id),
            ("product_template_id", "=", self.product_template_id.id),
            ("usage_id", "=", self.usage_id.id),
        ]
        product_accounts = ProductAccount.search(criteria)
        if len(product_accounts) > 0:
            result = False
        return result
