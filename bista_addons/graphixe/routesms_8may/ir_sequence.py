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



class ir_sequence(osv.osv):
     _inherit = "ir.sequence"
     
     
     def create(self, cr, uid, vals, context=None):
        ''' Overiden method concanate sequence name and company naming convention'''
        user_obj=self.pool.get('res.users')
        company_obj=self.pool.get('res.company')
        
        seq_id = super(ir_sequence , self).create(cr, uid, vals, context)
        if vals.get('company_id') :
            
            updated_name=vals['name'] + ' '+  company_obj.browse(cr,uid,vals['company_id']).name_convention 
            self.write(cr,uid,seq_id,{'name':updated_name})    
            return seq_id
        return seq_id


