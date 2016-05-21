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

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns={
              
              'partner_sequence':fields.char('Customer ID',size=15),
              'prepaid':fields.boolean('Prepaid'),
              'postpaid':fields.boolean('Postpaid'),
              'tan':fields.char('TAN',size=10),
              'pan':fields.char('PAN',size=10),
              'vat': fields.char('VAT', help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
              'vertical':fields.many2one('vertical.business','Vertical',ondelete='restrict'),
            'email_1':fields.char('Email 1'),
            'email_2':fields.char('Email 2'),
              
              
              }

    #@api.model
    def create(self,cr,uid, vals,context=None):
        
        if vals.get('partner_sequence',False) == False:
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
        
        partner = super(res_partner, self).create(cr,uid, vals,context)
        
        
        return partner

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

