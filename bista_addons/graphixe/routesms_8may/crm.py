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

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context is None:
            context = {}
        
        emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
        if emp_id :
            if len(emp_id) >1 :
                raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
            
            return emp_id[0]
        
        
    def on_change_user(self, cr, uid, ids, user_id, context=None):
        ''' Inherited function to Get employee id if User manually change the Saleperson'''
        
        vals=super(crm_lead,self).on_change_user(cr, uid, ids, user_id, context)
        
        
        if user_id:
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0]})
                
                return {'value':vals}
        else:
            
            return vals
                
                
    
    _columns={
              
              #'employee_id':fields.function(default_emp_id,string='Employee User',type='many2one',relation='hr.employee',store=True),
              'employee_id':fields.many2one('hr.employee','Employee User'),
              }

    _defaults={
               
               'employee_id':default_emp_id,
               }

    