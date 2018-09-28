# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_procurement_group(self):
        res = super(SaleOrder, self)._prepare_procurement_group()
        res.update(
            {
                'move_type': self.picking_policy,
                'partner_id': self.partner_id.id,
                'partner_invoice_id': self.partner_shipping_id.id,
                'partner_shipping_id': self.partner_shipping_id.id,
             }
        )
        return res
