from odoo import models,fields  # noqa: I001
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    delivery_employee_id= fields.Many2one(
        "hr.employee",
        string="Delivery Employee",
        help="Employee responsible for handing over the delivery.",
    )
    delivery_notes=fields.Text(
        string="Delivery Notes",
        help="Notes about the delivery of customer handover.",
    )
    customer_signature = fields.Binary(
        string="Customer Signature",
        attachment=True,
        help="Customer's signature confirming receipt of goods."
    )

    def button_validate(self):
        result = super().button_validate()

        for picking in self:
            if (
                picking.state == "done"
                and picking.picking_type_code == "outgoing"
                and picking.sale_id
                and picking.sale_id.retail_order_status != "ready"
            ):
                raise UserError(
                    "You can only validate a delivery "
                    "when the retail order is ready."
                )
                result = super().button_validate()
                
                for picking in self:
                    if (
                        picking.state == "done"
                        and picking.picking_type_code == "outgoing"
                        and picking.sale_id
                    ):
                        sale_order = picking.sale_id

                
                        outgoing_pickings = sale_order.picking_ids.filtered(
                            lambda p: (
                                p.picking_type_code == "outgoing"
                                and p.state != "cancel"
                            )
                        )
                    if outgoing_pickings and all(
                        p.state == "done"
                        for p in outgoing_pickings
                    ):
                        sale_order.write({
                           "retail_order_status": "delivered",
                    })

        return result
           