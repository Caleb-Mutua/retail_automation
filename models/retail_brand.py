from odoo import fields, models


class RetailBrand(models.Model):
    _name = "retail.brand"
    _description = "Retail Brand"
    _order = "name"

    name = fields.Char(
        string="Brand Name",
        required=True,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _sql_constraints = [  # noqa: RUF012
        (
            "unique_brand_name",
            "UNIQUE(name)",
            "Brand name must be unique.",
        ),
    ]