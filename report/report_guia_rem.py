# -*- coding: utf-8 -*-

import time
from openerp.osv import osv
from openerp.report import report_sxw


class report_guia_rem(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_guia_rem, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time
        })


class report_saleorderqweb(osv.AbstractModel):
    _name = 'report.fxo_mv_print_documents.report_guia_rem_monvertical'
    _inherit = 'report.abstract_report'
    _template = 'fxo_mv_print_documents.report_guia_rem_monvertical'
    _wrapped_report_class = report_guia_rem 