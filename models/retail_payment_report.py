from odoo import fields, models


class RetailPaymentReport(models.Model):
    _name = 'retail.payment.report'
    _description = 'Retail Payment Report'
    _auto = False
    _rec_name = 'sale_order_id'
    _order = 'sale_order_id desc'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        readonly=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        readonly=True,
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        readonly=True,
    )

    order_total = fields.Monetary(
        string='Order Total',
        currency_field='currency_id',
        readonly=True,
    )

    amount_paid = fields.Monetary(
        string='Amount Paid',
        currency_field='currency_id',
        readonly=True,
    )

    amount_outstanding = fields.Monetary(
        string='Outstanding',
        currency_field='currency_id',
        readonly=True,
    )

    payment_status = fields.Selection(
        [
            ('unpaid', 'Unpaid'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
        ],
        string='Payment Status',
        readonly=True,
    )

    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS retail_payment_report CASCADE;

            CREATE VIEW retail_payment_report AS (
                SELECT
                    so.id AS id,
                    so.id AS sale_order_id,
                    so.partner_id AS partner_id,
                    so.currency_id AS currency_id,

                    so.amount_total AS order_total,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN rp.state = 'confirmed'
                                THEN rp.amount
                                ELSE 0
                            END
                        ),
                        0.0
                    ) AS amount_paid,

                    GREATEST(
                        so.amount_total -
                        COALESCE(
                            SUM(
                                CASE
                                    WHEN rp.state = 'confirmed'
                                    THEN rp.amount
                                    ELSE 0
                                END
                            ),
                            0.0
                        ),
                        0.0
                    ) AS amount_outstanding,

                    CASE
                        WHEN COALESCE(
                            SUM(
                                CASE
                                    WHEN rp.state = 'confirmed'
                                    THEN rp.amount
                                    ELSE 0
                                END
                            ),
                            0.0
                        ) <= 0
                        THEN 'unpaid'

                        WHEN COALESCE(
                            SUM(
                                CASE
                                    WHEN rp.state = 'confirmed'
                                    THEN rp.amount
                                    ELSE 0
                                END
                            ),
                            0.0
                        ) < so.amount_total
                        THEN 'partial'

                        ELSE 'paid'
                    END AS payment_status

                FROM sale_order so

                LEFT JOIN retail_payment rp
                    ON rp.sale_order_id = so.id

                WHERE so.state IN ('sale', 'done')

                GROUP BY
                    so.id,
                    so.partner_id,
                    so.currency_id,
                    so.amount_total
            )
        """)