from odoo import _,models,fields,api
import logging

_logger = logging.getLogger(__name__)

class SaleOrderReportWizard(models.TransientModel):
    _name = "sale_order.report.wizard"           

    langs = fields.Many2many("res.lang", string=_("Language"), default=lambda self:self.env['sale_order.report.wizard'].langs_default())
    template = fields.Selection(string=_("Template"), selection=[('normal', _('Normal')), ('no_delivery_times', _('No delivery times'))], default='normal')
    zipped = fields.Boolean(string=_("Zip"), default=False)
    
    def action_print_report(self):        
        data = {
            "form_data": self.read()[0],
            "active_id": self.env.context.get('active_id'),
            "active_ids": self.env.context.get('active_ids'),
        }
        
        report_action = self.env.ref("sale_order_mitxelena.action_report_sale_order").report_action(self, data=data)
        report_action['close_on_report_download']=True
        
        if len(self.langs) == 0:
            return
        
        return report_action
    
    def langs_default(self):
        active_ids = self.env.context.get('active_ids')
        
        if len(active_ids) == 1:            
            order = self.env['sale.order'].search([('id', '=', int(active_ids[0]))])            
            _logger.info(order)
            return self.env['res.lang'].search([('code', '=', order.partner_id.lang)]).ids
        else:
            return self.env['res.lang'].search([]).ids
            


    @api.onchange('langs')
    def _change_langs(self):
        
        if len(self.langs) > 1:
            self.zipped = True
        else:
            self.zipped = False
        
        

            
            
