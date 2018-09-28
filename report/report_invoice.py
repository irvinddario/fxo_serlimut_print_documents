# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.report import report_sxw
from helper import number_to_letter


class report_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(report_invoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'to_word': self._to_word,
        })

    def _to_word(self, number):
        return number_to_letter(str(number)) + "NUEVOS SOLES"


class report_saleorderqweb(osv.AbstractModel):
    _name = 'report.fxo_mv_print_documents.report_invoice_monvertical'
    _inherit = 'report.abstract_report'
    _template = 'fxo_mv_print_documents.report_invoice_monvertical'
    _wrapped_report_class = report_invoice 