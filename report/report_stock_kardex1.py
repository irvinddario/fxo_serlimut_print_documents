# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools
from odoo.addons import decimal_precision as dp


class report_stock_picking(models.Model):

    _name = 'report.stock.picking.move'
    _auto = False

    @api.one
    @api.depends('product_id')
    def _compute_product_price(self):
        for item in self:
            if item.product_id:
                item.price_unit = item.product_id.standard_price
                item.price_total = item.price_unit * item.product_qty

    product_id = fields.Many2one("product.product", string="Producto")
    name = fields.Char('Nombre')
    min_date = fields.Datetime('Fecha', help="")
    picking_type_id = fields.Many2one('stock.picking.type', 'Tip. Operacion',)
    product_uom_id = fields.Many2one('product.uom', 'UM')
    product_qty = fields.Float('Cantidad', default=0.0, digits=dp.get_precision('Product Unit of Measure'), required=True)
    price_unit = fields.Float('C.Unit', compute='_compute_product_price', digits=dp.get_precision('Product Price'))
    price_total = fields.Float('Total', compute='_compute_product_price', digits=dp.get_precision('Product Price'))
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    company_id = fields.Many2one('res.company')
    partner_id = fields.Many2one('res.partner')

    _order = 'name, picking_type_id,min_date desc'

    def report_print(self):

        ids2 = self.env['report.stock.picking.move'].search([])
        datas = {
            'ids': ids2.ids,
            'model': 'report.stock.picking.move',
            'form': ids2.ids
        }

        return self.env['report'].get_action(ids2, 'fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento')

    @api.model_cr
    def init(self):
        print "INIT_________________"
        tools.drop_view_if_exists(self._cr, 'report_stock_picking_move')
        self._cr.execute("""
            create view report_stock_picking_move as (
                select 
                sp.partner_id, sp.company_id, spo.id, sp.name, sp.min_date, spt.id as picking_type_id, spo.product_id, 
                spo.product_uom as product_uom_id, spo.product_qty, spt.warehouse_id
                from stock_picking sp 
                left join stock_picking_type spt on (sp.picking_type_id=spt.id) 
                left join stock_move spo on (sp.id=spo.picking_id)
                where spo.product_id is not null order by name,picking_type_id,min_date desc
            )""")
