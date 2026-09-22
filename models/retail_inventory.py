from odoo import models , fields , api  # noqa: I001


class productProduct(models.Model):
    _inherit = 'product.product'
    
    retail_min_stock =fields.Float(
        string='Minimun Stock Level',
        default= 0.0,
        help='Minimun quantity that should normally be available.'
    )
    
    retail_stock_status = fields.Selection(
        selection=[
            ('out_of_stock', 'Out of Stock'),
            ('low_stock', 'Low Stock'),
            ('in_stock', 'In Stock'),
        ],
        string= 'Retail Stock Status',
        compute= '_compute_retail_stock_status',
        store=True,
    )
    
    @api.depends('qty_available', 'retail_min_stock')
    def _compute_retail_stock_status(self):
        for product in self:
            if product.qty_available <= 0:  
               product.retail_stock_status = 'out_of_stock' 
            
            elif product.qty_available <= product.retail_min_stock: 
               product.retail_stock_status= 'low_stock' 
            else:
             product.retail_stock_status = 'in_stock'  
            