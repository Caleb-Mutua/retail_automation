from odoo import  fields, models,api   # noqa: I001
from odoo.exceptions import UserError


class RetailPayment(models.Model):
    _name = "retail.payment"
    _description = "Retail Payment"
    _order = "payment_date desc, id desc"

    name = fields.Char(
        string="Payment Reference",
        required=True,
        copy=False,
        readony= True,
        default="New",
    )
    

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
        required=True,
        ondelete="restrict",
        index=True,
    )

    partner_id = fields.Many2one(
        related="sale_order_id.partner_id",
        string="Customer",
        store=True,
        readonly=True,
    )

    payment_date = fields.Date(
        string="Payment Date",
        required=True,
        default=fields.Date.context_today,
    )

    amount = fields.Monetary(
        string="Amount",
        required=True,
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        related="sale_order_id.currency_id",
        string="Currency",
        store=True,
        readonly=True,
    )

    payment_method = fields.Selection(
        [
            ("cash", "Cash"),
            ("mpesa", "M-Pesa"),
            ("bank", "Bank Transfer"),
            ("other", "Other"),
        ],
        string="Payment Method",
        required=True,
        default="cash",
    )

    transaction_reference = fields.Char(
        string="Transaction Reference",
        help="For example, an M-Pesa transaction code.",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )

    notes = fields.Text(string="Notes")
    
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get("name","New") == "New":
                vals["name"] =(
                    self.env["ir.sequence"].next_by_code("retail.payment")
                    or "New"
                )
                  
            return super().create(vals_list)
        
    def action_confirm(self):
        for payment in self:
            if payment.state != "draft":
                raise UserError(
                    "Only draft payments can be confirmed."
                )

            if payment.amount <= 0:
                raise UserError(
                    "The payment amount must be greater than zero."
                )

            if payment.sale_order_id.state != "sale":
                raise UserError(
                    "Payments can only be recorded "
                    "against confirmed sales orders."
                )

            payment.write({"state": "confirmed"})

        return True

    def action_cancel(self):
        for payment in self:
            if payment.state != "confirmed":
                raise UserError(
                    "Only confirmed payments can be cancelled."
                )

            payment.write({"state": "cancelled"})

        return True