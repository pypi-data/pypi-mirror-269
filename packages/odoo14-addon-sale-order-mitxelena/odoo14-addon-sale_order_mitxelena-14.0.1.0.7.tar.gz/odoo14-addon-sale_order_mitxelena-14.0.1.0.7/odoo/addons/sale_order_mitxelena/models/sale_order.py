from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dimensions = fields.Char(related="product_id.dimensions", string="Dimensions")
    materials = fields.Char(related="product_id.materials", string="Materials")
    date_order = fields.Datetime(related="order_id.date_order")
    client_order_ref = fields.Char(related='order_id.client_order_ref', string="Client ref.")
    plan = fields.Binary(string="Plan", related="product_id.plan")
    plan_fname = fields.Char(string="Plan", related="product_id.plan_fname")    
        
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    mecanization = fields.Boolean(string="Mecanization")
    welding = fields.Boolean(string="Welding")
    painting = fields.Boolean(string="Painting")
    assembly = fields.Boolean(string="Assembly")
    payed_shipping = fields.Boolean(string="Payed Shipping")
    application = fields.Selection(string="Application", selection=[('shipbuilding', _('Shipbuilding')), ('eolian', _('Eolian')), ('papermaking', _('Papermaking')), 
                                                ('energy', _('Energy')), ('aeronautic', _('Aeronautic')), ('petrochemical', _('Petrochemical')),
                                                ('press', _('Press')),('others', _('Others'))])
    urgency = fields.Boolean(string="Urgency")
    reparation = fields.Boolean(string="Reparation")
    estimated_date = fields.Char(string="Estimated date")

class Product(models.Model):
    _inherit = ["product.template"]
    dimensions = fields.Char(string="Dimensions")
    materials = fields.Char(string="Materials")
    plan = fields.Binary(string="Plan file")
    plan_fname = fields.Char(string='File name')
    special_processes_treatments = fields.Text(string='Treatments / Processes')     