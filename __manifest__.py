# -*- coding: utf-8 -*-
{
    'name' : 'Print report documents',
    'version': '1.0',
    "author": "Flexxoone",
    'summary': 'Impresión de documentos MonVertical',
    'category': 'Tools',
    'description': """""",
    'depends': [
        'account',
        'l10n_pe_vat',
        'fxo_invoice_stock_picking',
        'nanotec_stock_account_extend',
        'stock',
        #'bi_professional_reports_templates'
    ],
    'data': [
        "data/report_paperformat.xml",
        'view/vale_devolucion_uniforme.xml',
        'view/reporte_bienes_distribuidos.xml',

        'view/reporte_consumo_tipo_movimiento.xml',

        #'view/report_picking.xml',


        "report.xml",
        "view/report_bill_of_sale.xml",
        "view/report_invoice.xml",
        "view/report_guia_rem.xml",
        #"view/view_invoice.xml",
        "view/view_stock_picking.xml",

        'wizard/salida_por_movimiento_view.xml'


    ],
    'application': True,
}
