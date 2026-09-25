from odoo import fields, models  # noqa: I001
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
            "view_mode": "list, form",
            "domain":[("origin","=",self.name)],
        }
    def action_cancel(self):
        result = super().action_cancel()

        self.write({
            "retail_order_status": "cancelled",
         })

        return result
    
    