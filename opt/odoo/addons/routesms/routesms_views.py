# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP SA (<http://openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
from lxml import etree
import math
import pytz
import urlparse

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _



class pnr_report(osv.osv):
    _name = 'pnr.report'
    _description='PNR Report for AIR 29T'

    
    _columns={
              
            'name':fields.char('Sr.No'),
            'supplier':fields.char('Supplier Name'),
            'date_invoice':fields.char('Invoice Date'),
            'supplier_product_line':fields.char('Product'),
            'supplier_passenger_name':fields.char('Passenger Name'),
            'supplier_reference':fields.char('Reference'),
            'supplier_pnr':fields.char('PNR'),
            'supplier_amount':fields.float('Amount'),
            'customer':fields.char('Customer Name'),
            'tax_amount':fields.float('Tax Amount'),
            'customer_subtotal':fields.char('Subtotal'),
            'profit':fields.float('Profit'),
            'status':fields.char('Remark')
            }

    def print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        context={}
        if context is None:
            
            context = {}
        
        
        #import ipdb;ipdb.set_trace()
        datas= {
                  'model':'pnr.report',
                  'id': ids and ids[0] or False,
                 
                  
                 },
        
        return {'type': 'ir.actions.report.xml', 'report_name': 'routesms.report_pnr', 'datas': datas,'nodestroy': True}

           
    
pnr_report()



class source_document_report(osv.osv):
    _name = 'source.document.report'
    _description='Source document Report for 29T'

    
    _columns={
              
            'name':fields.char('Sr.No'),
            'supplier':fields.char('Supplier Name'),
            'date_invoice':fields.char('Invoice Date'),
            'product_line':fields.char('Product'),
            'passenger_name':fields.char('Passenger Name'),
            'reference':fields.char('Reference'),
            'source_document':fields.char('Source'),
            'supplier_amount':fields.float('Amount'),
            'customer':fields.char('Customer Name'),
            'tax_amount':fields.float('Tax Amount'),
            'customer_subtotal':fields.char('Subtotal'),
            'profit':fields.float('Profit'),
            'status':fields.char('Remark')
            }

    def print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        context={}
        if context is None:
            
            context = {}
        
        
        #import ipdb;ipdb.set_trace()
        datas= {
                  'model':'source.document.report',
                  'id': ids and ids[0] or False,
                 },
        
        return {'type': 'ir.actions.report.xml', 'report_name': 'routesms.report_source', 'datas': datas,'nodestroy': True}

           
    
pnr_report()



