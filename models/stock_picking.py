from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super().button_validate()

        for picking in self:
            if (
                picking.state == "done"
                and picking.picking_type_code == "outgoing"
                and picking.origin
            ):
                sale_orders = self.env["sale.order"].search([
                    ("name", "=", picking.origin),
                    ("state", "=","sale"),
                ])

                for sale_order in sale_orders:
                    sale_order.write({
                        "retail_order_status": "delivered",
                    })

        return result
           