from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    retail_notes = fields.Char(
        string="Retail Notes"
    )