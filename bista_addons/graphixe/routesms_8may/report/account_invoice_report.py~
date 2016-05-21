# -*- coding: utf-8 -*-
##############################################################################
#
#    Bista Solutions PVT LTD.
#    Copyright (C) 2007-TODAY Bista-solutions(http://bistasolutions.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.osv import osv
from openerp.report import report_sxw
from datetime import datetime


class account_invoice(report_sxw.rml_parse):
    _name='ccount_invoice'

    def __init__(self, cr, uid, name, context):
        super(account_invoice, self).__init__(cr, uid, name, context=context)
        self.cr = cr
        self.uid = uid
        self.seq = 0;
        self.localcontext.update({
            'date': datetime.date(datetime.now()),
            'get_custom_amount':self.get_custom_amount,
        })
        
    
    def get_custom_amount(self,o):
        
        cr = self.cr
        uid = self.uid
        
#         part = o.company_id.partner_id
#         part_obj = self.pool.get('res.partner')
        return True
        #return part  
    

class report_account_invoice(osv.AbstractModel):
    _name = 'report.account.routesms_invoice'
    _inherit = 'report.abstract_report'
    _template = 'routesms.routesms_invoice'
    _wrapped_report_class = account_invoice

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
