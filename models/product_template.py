from odoo import fields, models  # noqa: I001

class ProductTemplate(models.Model):
    _inherit = "product.template"

    retail_brand_id = fields.Many2one(
        "retail.brand",
        string="Brand",
        ondelete="restrict",
    )