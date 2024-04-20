# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Type Selection for Product",
    "version": "14.0.1.4.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_product",
        "account",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/product_usage_type_data.xml",
        "templates/product_usage_m2_configurator_templates.xml",
        "views/product_usage_type_views.xml",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "demo": [],
}
