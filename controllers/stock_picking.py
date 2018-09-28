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
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Binary(http.Controller):

    @http.route('/web/report/download_stock_picking', type='http', auth="user")
    @serialize_exception
    def download_stock_picking(stock_picking, model, type_document_partner_it, stock_picking_id, filename=None, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        stock_picking = request.registry[model]
        stock_picking = stock_picking.browse(cr, uid, int(stock_picking_id), context)
        lines = []
        i = 0
        for item in stock_picking.move_lines:
            codigo = ""
            description = ""
            unidad_de_medida = ""
            i = i + 1 

            if item.product_id.default_code:
                codigo =  item.product_id.default_code
            if item.name:
                description = str(item.name).upper()
            if item.product_uom.name:
                unidad_de_medida = item.product_uom.name

            lines.append({
                "item": i,
                "codigo": codigo,
                "description": description,
                "qty": int(item.product_qty),
                "unit_uom": unidad_de_medida,
                "peso": "",
            })

        #verificar si existen datos y poner "- -" para que no salga False
        date = ""
        min_date = ""
        origin_address = ""
        delivery_address_id = ""
        name = ""
        nro_documento = ""
        vehicle_transport = ""
        name_transport = ""
        addres_transport = ""
        ruc_transport = ""
        type_document_partner_it = ""
        delivery_address = ""

        if stock_picking.date:
            date = str(stock_picking.date)[0:11]
        if stock_picking.min_date:
            min_date = str(stock_picking.min_date)[0:11]
        if stock_picking.origin_address_id.street:
            origin_address =  str(stock_picking.origin_address_id.street)[0:92]
        if stock_picking.delivery_address_id.street:
            delivery_address =  str(stock_picking.delivery_address_id.street)[0:92]
        if stock_picking.partner_id.name:
            name = str(stock_picking.partner_id.name)
        if stock_picking.partner_id.nro_documento:
            nro_documento = stock_picking.partner_id.nro_documento
        if stock_picking.driver_id.vehicle_id.model_id.brand_id.name != False and stock_picking.driver_id.vehicle_id.license_plate != False:
            vehicle_transport = str(stock_picking.driver_id.vehicle_id.model_id.brand_id.name) + " - " + str(stock_picking.driver_id.vehicle_id.license_plate)
        if stock_picking.carrier_id.partner_id.name:
            name_transport = stock_picking.carrier_id.partner_id.name
        if stock_picking.carrier_id.partner_id.street:
            addres_transport = str(stock_picking.carrier_id.partner_id.street)
        if stock_picking.carrier_id.partner_id.nro_documento:
            ruc_transport = stock_picking.carrier_id.partner_id.nro_documento
        if stock_picking.picking_type_id.name:
            type_document_partner_it = stock_picking.picking_type_id.name
        datas = {
            "date": date,
            "min_date": min_date,
            "origin_address": origin_address,
            "delivery_address": delivery_address,
            "name": name,
            "nro_documento": nro_documento,
            "vehicle_transport": vehicle_transport,
            "name_transport": name_transport,
            "addres_transport": addres_transport,
            "constancia": "",
            "ruc_transport": ruc_transport, 
            "nro_licencia": "",
            "nro_constancia": "",
            "lines": lines,
            #"type_document_partner_it": type_document_partner_it,
            "null": ""
        }

        stock_picking_path = openerp.modules.get_module_resource('fxo_mv_print_documents','templates', "stock_picking.odt")

        if not stock_picking_path:
            error = {
                'code': 200,  
                'message': "Odoo Server Error",
                'data': "Not found file template in module!."
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))

        try:
            basic = Template(source="", filepath=stock_picking_path)
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
