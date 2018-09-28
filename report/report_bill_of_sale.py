# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.report import report_sxw


class report_bill_of_sale(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_bill_of_sale, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total': self._get_total,
        })

    def _get_total(self, lines):
        total = 0.0
        for line in lines :
            total += line.price_subtotal or 0.0
        return total


class report_saleorderqweb(osv.AbstractModel):
    _name = 'report.fxo_mv_print_documents.report_bill_of_sale_monvertical'
    _inherit = 'report.abstract_report'
    _template = 'fxo_mv_print_documents.report_bill_of_sale_monvertical'
    _wrapped_report_class = report_bill_of_sale 