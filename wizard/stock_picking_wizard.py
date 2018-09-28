# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import time

_logger = logging.getLogger(__name__)


class stock_picking_wizard(models.TransientModel):

    _name = 'stock.picking.wizard'

    warehouse_id = fields.Many2one("stock.warehouse", string="Almacen")
    date_from = fields.Date('Fecha desde', required=True, default=time.strftime('%Y-%m-01'))
    to_date = fields.Date('Fecha hasta', required=True, default=time.strftime('%Y-%m-%d'))

    def action_calculate(self):
        print True
        domain = [
            ('min_date', '<=', self.to_date),
            ('min_date', '>=', self.date_from),
            ('warehouse_id', '=', self.warehouse_id.id),
        ]

        return {
            'name': _('Consumos por tipo de Movimiento'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'report.stock.picking.move',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'domain': domain,
        }

    def report_print(self):
        return self.env['report.stock.picking.move'].report_print()
        #return self.env['report'].get_action(self, 'fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento')
        """ids2 = self.env['report.stock.picking.move'].search([])
        print "############## READ ###############3"
        print self.env['report.stock.picking.move'].read()
        print "################################### "
        data = {
            'ids': ids2.ids,
            'model': 'report.stock.picking.move',
            'form': '_-_'
        }
        #return self.env['report'].get_action(self, 'fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento',
        #                                 data=data)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento',
                'report_type': 'q-web',
                'datas': data,
                'name': 'reporte.pdf'
                }
        """

        """data = self.env['report.stock.picking.move'].search([])
        # data = self.env['report.stock.picking.move'].search([])
        #
        datas = {
            'ids': [],
            'model': 'report.stock.picking.move',
            'form': data
        }
        #
        #
        # datas = {}
        # datas['model'] = 'report.stock.picking.move'
        # datas['warehouse_id'] = self.warehouse_id.id
        return {'type': 'ir.actions.report.xml',
                'report_name': 'fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento',
                'report_type': 'q-web',
                'datas': datas,
                'name': 'reporte.pdf'
                }

        #return self.env['report'].render('fxo_serlimut_print_documents.reporte_consumo_tipo_movimiento', data)

        """ 