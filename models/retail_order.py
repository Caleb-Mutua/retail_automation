from odoo import  api,fields, models  # noqa: I001
from odoo.exceptions import UserError  # noqa: F401

class SaleOrder(models.Model):
    _inherit = "sale.order"

    retail_order_status = fields.Selection(
        [
            ("new", "New"),
            ("confirmed", "Confirmed"),
            ("processing", "Processing"),
            ("ready", "Ready for Delivery"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        string="Retail Order Status",
        default="new",
        tracking=True,
    )

    retail_notes = fields.Text(
        string="Retail Order Notes"
    )
    
    payment_ids = fields.One2many(
       "retail.payment",
       "sale_order_id",
       string="Retail Payments",
    )

    retail_amount_paid = fields.Monetary(
       string="Amount Paid",
       compute="_compute_retail_payment",
       store=True,
       currency_field="currency_id",
    )

    retail_balance = fields.Monetary(
       string="Outstanding Balance",
       compute="_compute_retail_payment",
       store=True,
       currency_field="currency_id",
    )

    retail_payment_status = fields.Selection(
       [
           ("unpaid", "Unpaid"),
           ("partial", "Partially Paid"),
           ("paid", "Paid"),
       ],
       
       string="Payment Status",
       compute="_compute_retail_payment",
       store=True,
    )
    deliverey_ids = fields.One2many(
        "stock.picking",
        "sale_id",
        string= "Deliveries",
    )

    @api.depends(
       "amount_total",
       "payment_ids.amount",
       "payment_ids.state",
       "currency_id",
    )
    def _compute_retail_payment(self):
        for order in self:
            paid = sum(
            order.payment_ids.filtered(
                lambda payment: payment.state == "confirmed"
               ).mapped("amount")
            )

            order.retail_amount_paid = paid
            order.retail_balance = max(
            order.amount_total - paid, 0.0
            )

        if order.currency_id.compare_amounts(
            paid, order.amount_total
        ) >= 0:
            order.retail_payment_status = "paid"
        elif order.currency_id.compare_amounts(
            paid, 0.0
        ) > 0:
            order.retail_payment_status = "partial"
        else:
            order.retail_payment_status = "unpaid"
    def action_confirm(self):
        result = super().action_confirm()
        
        self.write({
            "retail_order_status":"confirmed",
        })
        return result
    
    def action_start_processing(self):
         self.write({
             "retail_order_status": "processing",
         })

         return True
    def action_mark_ready(self):
         self.write({
             "retail_order_status": "ready",
         })

         return True
    
     
    def action_view_delivery(self):
        self.ensure_one()
        
        return {
            "type": "ir.actions.act_window",
            "name": "Delivery",
            "res_model": "stock.picking",
            "view_mode": "list,form",
            "domain":[("origin","=",self.name)],
        }
    def action_cancel(self):
        result = super().action_cancel()

        self.write({
            "retail_order_status": "cancelled",
         })

        return result
    
    