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



class vertical_business(osv.osv):
    _name = 'vertical.business'
    _description='Add verticals of your business'

    
    _columns={
              
            'name':fields.char('Name',size=30),
            'code':fields.char('Code',size=10),
            'active':fields.boolean('Active'),
            'company_id': fields.many2many('res.company', 'vertical_company_rel',
                      'vertical_id', 'company_id', 'Companies',readonly=True),
                                    
            }


    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False):
        
        company_obj=self.pool.get('res.company')
        
        result = super(vertical_business, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar)
        
        if result['view_id'] :
            
            vertical_ids=self.search(cr,uid,[])
            for active_id in vertical_ids :
                 company_vertical_ids=company_obj.search(cr,uid,[('vertical','=',active_id)])
                 
                 self.write(cr, uid, active_id, {'company_id': [(6, 0, company_vertical_ids)]})
        
        return result

           
    
vertical_business()




