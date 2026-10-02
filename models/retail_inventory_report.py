from odoo import fields, models


class RetailInventoryReport(models.Model):
    _name = 'retail.inventory.report'
    _description = 'Retail Inventory Report'
    _auto = False
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True,
    )

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        readonly=True,
    )

    brand_id = fields.Many2one(
        'retail.brand',
        string='Brand',
        readonly=True,
    )

    quantity = fields.Float(
        string='Quantity On Hand',
        readonly=True,
    )

    min_stock = fields.Float(
        string='Minimum Stock',
        readonly=True,
    )

    stock_status = fields.Selection(
        selection=[
            ('out_of_stock', 'Out of Stock'),
            ('low_stock', 'Low Stock'),
            ('in_stock', 'In Stock'),
        ],
        string='Stock Status',
        readonly=True,
    )

    inventory_value = fields.Float(
        string='Inventory Value',
        readonly=True,
    )

def init(self):
    self.env.cr.execute("""
        DROP VIEW IF EXISTS retail_inventory_report CASCADE;

        CREATE VIEW retail_inventory_report AS (
            SELECT
                pp.id AS id,
                pp.id AS product_id,
                pt.id AS product_tmpl_id,
                pt.retail_brand_id AS brand_id,
                COALESCE(sq.quantity, 0.0) AS quantity,
                pp.retail_min_stock AS min_stock,
                pp.retail_stock_status AS stock_status

            FROM product_product pp

            JOIN product_template pt
                ON pt.id = pp.product_tmpl_id

            LEFT JOIN (
                SELECT
                    sq.product_id,
                    SUM(sq.quantity) AS quantity

                FROM stock_quant sq

                JOIN stock_location sl
                    ON sl.id = sq.location_id

                WHERE sl.usage = 'internal'

                GROUP BY sq.product_id
            ) sq
                ON sq.product_id = pp.id

            WHERE pt.active = TRUE
        )
    """)