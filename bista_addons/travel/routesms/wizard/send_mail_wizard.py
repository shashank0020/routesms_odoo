# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import email_split
from openerp import SUPERUSER_ID
from openerp.routesms_email.routesms_email import *
class wizard(osv.osv_memory):

    _name = 'partner.mail.wizard'
    _description = 'Send notification to Account user to validate the partner'



    def send_mail(self, cr, uid, ids, context=None):
        ''' Send mail to accounting team about partner validation'''
         
        if context.get('active_id') :
             
            partner=self.pool.get(context.get('active_model')).browse(cr,uid,context.get('active_id'))
            if partner.state =='confirm' : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('Partner Is Already Validated'))
             
            FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
            if '@' and '.com' not in FROM_MAIL : 
                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 
            # check credit type
             
            if partner.prepaid : 
                credit='Prepaid'
             
            else : 
                credit='Postpaid'
 
            SUBJECT = '''Partner Validation "{}" '''.format(partner.name)         
                             
            MESSAGE = '''Hello Accounts Team ,\n\nKindly validate following Partner - \n\nName : {} \nSalesperson : {} \nCredit Type : {} \nCompany : {} \n\nThanks & Regards \n\n{}
            ''' .format(partner.name , partner.user_id.name, credit, partner.company_id.name \
                                        ,self.pool.get('res.users').browse(cr,uid,uid).name) 
             
            #check internet connection 
            
            #connection =check_internet_connection('http://erp.routesms.com')  
            connection =check_internet_connection('http://192.168.0.12:8069')
            if not connection : 
                raise osv.except_osv(_('No Internet Connection'),
                                    _(' Contact IT Team'))              
             
            
            notification=sendmail(
                from_addr    = FROM_MAIL,                               
                to_addr_list = ['krupali.golapkar@routesms.com','neha.kadam@routesms.com','sanika.wadekar@routesms.com','shailesh@routesms.com'],
                cc_addr_list = ['sushma.gedam@routesms.com'], 
                subject      = SUBJECT, 
                message      = MESSAGE, 
                login        = 'ar@routesms.com', 
                password     = 'Routesms@05'
                 
                ) 
             
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('ERROR'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
         
        else : 
                    
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))                        
# 
#            #####################TESTING  PURPOSE##################
#     def send_mail(self, cr, uid, ids, context=None):
#         ''' Send mail to accounting team about partner validation'''
#         
#         if context.get('active_id') :
#             
#             partner=self.pool.get(context.get('active_model')).browse(cr,uid,context.get('active_id'))
#             if partner.state =='confirm' : 
#                 raise osv.except_osv(_('VALIDATION ERROR'),
#                                     _('Partner Is Already Validated'))
#             
#             FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
#             if '@' and '.com' not in FROM_MAIL : 
#                 raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
#                                     _("Invalid Sender's Email Id \n Contact HR Team"))
#                 
#             # check credit type
#             
#             if partner.prepaid : 
#                 credit='Prepaid'
#             
#             else : 
#                 credit='Postpaid'
# 
#             SUBJECT = '''Partner Validation "{}" '''.format(partner.name)         
#                             
#             MESSAGE = '''Hello Accounts Team ,\n\nKindly validate following Partner - \n\nName : {} \nSalesperson : {} \nCredit Type : {} \nCompany : {} \n\nThanks & Regards \n\n{}
#             ''' .format(partner.name , partner.user_id.name, credit, partner.company_id.name \
#                                         ,self.pool.get('res.users').browse(cr,uid,uid).name) 
#             
#             
#             
#             #check internet connection 
#             
#             connection =check_internet_connection('http://erp.routesms.com')  
#             if not connection : 
#                 raise osv.except_osv(_('No Internet Connection'),
#                                     _(' Contact IT Team'))                     
#             notification=sendmail(
#                 from_addr    = 'shazz0020@gmail.com',                               
#                 to_addr_list = ['shazzwazz20@gmail.com'],
#                 cc_addr_list = ['shashank.verma@bistacloud.com'], 
#                 subject      = SUBJECT, 
#                 message      = MESSAGE, 
#                 login        = 'ar@routesms.com', 
#                 password     = 'Rsl@2015'
#                 
#                 ) 
#             
#             if notification :
#                  
#                 return {'type': 'ir.actions.act_window_close'}
#             
#             else :
#                 ''' Sending fail'''
#                 
#                 raise osv.except_osv(_('ERROR'),
#                                     _('Email Sending Failed! \n Contact Odoo Team'))
#         
#         else : 
#                    
#             raise osv.except_osv(_('ERROR'),
#                                 _('Email Sending Failed! \n Contact Odoo Team'))                        
# 
#            
            
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
