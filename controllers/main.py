# -*- encoding: utf-8 -*-
from openerp import http
import openerp
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception, content_disposition
import base64
from relatorio.templates.opendocument import Template
import werkzeug.utils
import werkzeug.wrappers
import simplejson
from ..report.helper import number_to_letter
import time
from decimal import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Binary(http.Controller):

    @http.route('/web/report/download_document', type='http', auth="user")
    @serialize_exception
    def download_document(invoice, model, type_document_partner_it, inv_id, filename=None, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        invoice = request.registry[model]
        invoice = invoice.browse(cr, uid, int(inv_id), context)

        picking_name = ""

        if invoice.picking_ids:
            pickings = [i.nro_documento for i in invoice.picking_ids]
            if i.nro_documento:
                picking_name = ", ".join(pickings)

        order_name = ""
        if invoice.sale_ids:
            orders = [i.name for i in invoice.sale_ids]
            if i.name:
                order_name = ", ".join(orders)
                
        lines = []

        for item in invoice.invoice_line:
            description = ""
            codigo = ""
            if item.name:
                description = str(item.name).upper()
            if item.product_id.default_code:
                codigo =  item.product_id.default_code
            lines.append({
                "codigo": codigo,
                "product": item.product_id.name,
                "description": description,
                "qty": int(item.quantity),
                "price_unit": item.price_unit,
                "price_subtotal":  '{:,.2f}'.format(item.price_subtotal),
                "price_subtotal_igv": '{:,.2f}'.format(item.invoice_line_tax_id.amount * item.price_subtotal + item.price_subtotal)
            })

        if(invoice.tax_line != False):
            igv = 18
        else:
            igv = 0

        #Validacion de datos
        name =""
        street = ""
        nro_documento = ""
        date_invoice = ""
        day = ""
        month = ""
        month_number = ""
        year = ""
        y = ""
        payment_term = ""
        user = ""
        doc_modificado = ""
        nro_doc_modificado = ""
        fecha_doc_modificado = ""
        informacion_adicional = ""
        tipo_nd = ""
        number_invoice = ""

        if invoice.number:
            number_invoice = invoice.number
        if invoice.partner_id.name:
            name = invoice.partner_id.name
        if invoice.partner_id.street:
            street = str(invoice.partner_id.street)[:90].upper()
        if invoice.partner_id.nro_documento:
            nro_documento = invoice.partner_id.nro_documento
        if invoice.date_invoice:
            date_invoice=invoice.date_invoice
            day = time.strftime('%d', time.strptime(invoice.date_invoice,'%Y-%m-%d'))
            month = str(time.strftime('%B', time.strptime(invoice.date_invoice,'%Y-%m-%d'))).upper()
            month_number = str(time.strftime('%m', time.strptime(invoice.date_invoice,'%Y-%m-%d'))).upper()
            year = time.strftime('%y', time.strptime(invoice.date_invoice,'%Y-%m-%d'))
            y = time.strftime('%y', time.strptime(invoice.date_invoice,'%Y-%m-%d'))[1]
        if invoice.payment_term:
            payment_term = str(invoice.payment_term.name).upper()
        if invoice.user_id.name:
            user = str(invoice.user_id.name).upper()

        datas = {
            "number": number_invoice,
            "name": name,
            "street": street,
            "nro_documento": nro_documento,
            "date_invoice": date_invoice,
            "guia": "",
            "day": day,
            "month": month,
            "month_number": month_number,
            "year": year,
            "y": y,
            "picking_name": picking_name,
            "order_name": order_name,
            "lines": lines,
            "payment_term": payment_term,
            "a_untaxed": 'S/{:,.2f}'.format(invoice.amount_untaxed),
            "igv": igv,
            "a_tax": 'S/{:,.2f}'.format(invoice.amount_tax),
            "a_total": 'S/{:,.2f}'.format(invoice.amount_total),
            "user": user,
            "number2letter": number_to_letter(str('{0:.2f}'.format(invoice.amount_total))) + " SOLES",
            ##################################
            "prueba": "",
            "null": "",
        }
        if "invoice" == type_document_partner_it:
            invoice_path = openerp.modules.get_module_resource('fxo_mv_print_documents','templates', "invoice.odt")
        if "ticket" == type_document_partner_it:
            invoice_path = openerp.modules.get_module_resource('fxo_mv_print_documents','templates', "ticket.odt")
        
        if not invoice_path:
            error = {
                'code': 200,  
                'message': "Odoo Server Error",
                'data': "Not found file template in module!."
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))

        try:
            basic = Template(source="", filepath=invoice_path)
        except:
            error = {
                'code': 200,  
                'message': "Odoo Server Error",
                'data': "You do not have permission to read\nfile template!."
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))

        basic_generated = basic.generate(o=datas).render()
        filecontent = basic_generated.getvalue()

        if not filecontent:
            return request.not_found()
        else:
            if not filename:
                filename = '%s_%s' % (model.replace('.', '_'), wid)
            return request.make_response(filecontent,
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition', content_disposition(filename))])


