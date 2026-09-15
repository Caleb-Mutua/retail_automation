from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_status = fields.Selection(
        [
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        string="Customer Status",
        default="active",
    )

    customer_notes = fields.Text(
        string="Customer Notes"
    )
    customer_type = fields.Selection(
    [
        ("walk_in", "Walk-in"),
        ("regular", "Regular"),
        ("vip", "VIP"),
        ("wholesale", "Wholesale"),
    ],
    string="Customer Type",
    default="walk_in",
    )
    @api.constrains("phone", "mobile", "email","customer_type")
    def _check_customer_contact(self):
        for customer in self:
            if customer.customer_status == "active":  # noqa: SIM102
                if not customer.phone and not customer.mobile and not customer.email:
                    raise ValidationError(
                     "An active customer must have a phone number, mobile number, or email address."
                )
            if customer.customer_type == "wholesale":  # noqa: SIM102
                if not customer.phone and not customer.mobile:
                    raise ValidationError(
                     "Wholesale customers must have a phone or mobile number."
                )
    