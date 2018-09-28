# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.report import report_sxw
from helper import number_to_letter


class report_credit_note(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_credit_note, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'to_word': self._to_word,
        })

    def _to_word(self, number):
        return number_to_letter(str(number)) + "NUEVOS SOLES"


class report_credit_note_qweb(osv.AbstractModel):
    _name = 'report.fxo_mv_print_documents.report_credit_note_monvertical'
    _inherit = 'report.abstract_report'
    _template = 'fxo_mv_print_documents.report_credit_note_monvertical'
    _wrapped_report_class = report_credit_note 