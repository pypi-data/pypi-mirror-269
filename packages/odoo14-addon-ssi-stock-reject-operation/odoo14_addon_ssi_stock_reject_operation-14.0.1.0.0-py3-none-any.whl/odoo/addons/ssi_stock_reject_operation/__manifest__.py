# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Reject Inventory Operation",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_stock",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "data/stock_picking_type_category_data.xml",
        "views/customer_reject_in_views.xml",
        "views/supplier_reject_out_views.xml",
    ],
    "demo": [],
}
