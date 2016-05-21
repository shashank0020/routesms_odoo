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

class res_company(osv.osv):
    _inherit = 'res.company'

    def _cin(self, cr, uid, ids, name, args, context=None):
        
        res = {}
        for company_id in self.browse(cr, uid, ids) :
        #
            cin=company_id.partner_id.cin
            if cin :

                res[company_id.id] = str(cin)
            else :
                res[company_id.id] = ''
        
        return res
    
    def _pan(self, cr, uid, ids, name, args, context=None):
        
        res = {}
        for company_id in self.browse(cr, uid, ids) :
        #
            pan=company_id.partner_id.pan
            if pan :

                res[company_id.id] = str(pan)
            else :
                res[company_id.id] = ''
                
        return res
    
                    
    def _company_registery(self, cr, uid, ids, name, args, context=None):
        
        res = {}
        for company_id in self.browse(cr, uid, ids) :
        #
            company_registery=company_id.partner_id.company_registery
            if company_registery :

                res[company_id.id] = str(company_registery)
            else :
                res[company_id.id] = ''                    
        return res
    
    
    
    _columns={
              
              'vertical':fields.many2one('vertical.business','Vertical',ondelete='restrict'),
              'name_convention':fields.char('Convention'),
              'baner': fields.binary(string='Baner'),
              'cin':fields.function(_cin, string='CIN', type='char',store=True),
              'pan':fields.function(_pan, string='PAN', type='char',store=True),
              'company_registery':fields.function(_company_registery, string='Service Tax Reg.', type='char',store=True),
              'icici_bank_baner': fields.binary(string='ICICI Bank Baner'),
              'hdfc_bank_baner': fields.binary(string='HDFC Bank Baner'),
              

              }





    def unlink(self,cr,uid,ids,context):
        
        
        raise osv.except_osv(_('Restricted!'), _('Deleting Company not allowed. Contact Technical Team'))
