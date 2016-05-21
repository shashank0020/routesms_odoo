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



class city_code(osv.osv):
    _name = 'city.code'
    _description='Add city codes'

    
    _columns={
              
            'name':fields.char('Code',size=30),
            'code':fields.char('Name',size=10),
            'active':fields.boolean('Active'),
            }

           
    
city_code()

class routsms_partner_filter(osv.osv):
    _name = 'routsms.partner.filter'
    _description='Tree view for partner filter'

    
    _columns={
              
            'name':fields.char('Name',size=300),
            'user_id':fields.many2one('res.users','Saleperson'),
	    'lead_status':fields.char('Lead Status',size=300),
            'is_active':fields.char('Partner Is Active?'),
            'creation_date':fields.char('Creation Date'),
            }

           
    
routsms_partner_filter()

