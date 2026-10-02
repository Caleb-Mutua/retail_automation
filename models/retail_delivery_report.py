from odoo import fields, models


class RetailDeliveryReport(models.Model):
    _name = "retail.delivery.report"
    _description = "Retail Delivery Analysis"
    _auto = False
    _rec_name = "picking_id"
    _order = "scheduled_date desc"

    picking_id = fields.Many2one(
        "stock.picking",
        string="Delivery",
        readonly=True,
    )

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
        readonly=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        readonly=True,
    )

    employee_id = fields.Many2one(
        "hr.employee",
        string="Delivery Employee",
        readonly=True,
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date",
        readonly=True,
    )

    date_done = fields.Datetime(
        string="Delivery Date",
        readonly=True,
    )

    picking_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("waiting", "Waiting"),
            ("confirmed", "Waiting Another Operation"),
            ("assigned", "Ready"),
            ("done", "Delivered"),
            ("cancel", "Cancelled"),
        ],
        string="Delivery Status",
        readonly=True,
    )

    retail_order_status = fields.Selection(
        [
            ("new", "New"),
            ("confirmed", "Confirmed"),
            ("processing", "Processing"),
            ("ready", "Ready"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        string="Retail Order Status",
        readonly=True,
    )

    delivery_days = fields.Float(
        string="Delivery Days",
        readonly=True,
        aggregator="avg",
    )

    

    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS retail_delivery_report CASCADE;

            CREATE VIEW retail_delivery_report AS (
                SELECT
                    sp.id AS id,
                    sp.id AS picking_id,
                    sp.sale_id AS sale_order_id,
                    sp.partner_id AS partner_id,
                    sp.delivery_employee_id AS employee_id,
                    sp.scheduled_date AS scheduled_date,
                    sp.date_done AS date_done,
                    sp.state AS picking_state,
                    so.retail_order_status AS retail_order_status,

                    CASE
                        WHEN sp.date_done IS NOT NULL
                             AND sp.scheduled_date IS NOT NULL
                        THEN
                            EXTRACT(
                                EPOCH FROM
                                (sp.date_done - sp.scheduled_date)
                            ) / 86400.0
                        ELSE 0.0
                    END AS delivery_days
           

                FROM stock_picking sp

                LEFT JOIN sale_order so
                    ON so.id = sp.sale_id

                WHERE sp.picking_type_id IN (
                    SELECT id
                    FROM stock_picking_type
                    WHERE code = 'outgoing'
                )
            )
        """)