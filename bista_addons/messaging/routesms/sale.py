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
from openerp.routesms_email.routesms_email import *
class sale_order(osv.osv):
    _inherit = 'sale.order'



    def check_multiple_taxes(self,cr,uid,ids): 
        ''' raise error if muliple taxes'''


        #############check for mulitlple taxes on same line or same invoices
        data=[]
        refer_base_amount=[]
        sale=self.browse(cr,uid,ids[0])
        if sale.order_line : 
            for x in sale.order_line : 
                for sale_tax_id in x.tax_id : 
                     
                    data.append(sale_tax_id.id)
         
        if len(set(data)) >1 : 
 
            raise osv.except_osv(_('Error!'),
                _("Multiple Taxes Not Allowed!"))
        ####ends##########################        

    def button_dummy(self, cr, uid, ids, context=None):
        
        self.check_multiple_taxes(cr,uid,ids)
        return True


    def create(self, cr, uid, vals, context=None):
        res = super(sale_order, self).create(cr, uid, vals, context=None)
        
        self._bank_charge_total(cr, uid, [res], context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(sale_order, self).write(cr, uid, ids, vals, context)
        
        self._bank_charge_total(cr, uid, ids, context)
        return res    
    
    def _bank_charge_total(self, cr, uid, ids, context):
         
        res = {}
       # import ipdb;ipdb.set_trace()
        for sale_id in self.browse(cr, uid, ids) :
        #
            total_amount=sale_id.amount_total
            if total_amount :
                 
                 
                amount = total_amount + sale_id.bank_charges 
            else :
                amount =0
        cr.execute(''' update sale_order set total_with_bank_charges=%s where id=%s''',(amount,ids[0])) 
        return True
    

    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines, context=None):
        ''' Overidden funciton to add bank charges'''
            
                    
        res = super(sale_order, self).onchange_pricelist_id(cr, uid, ids, pricelist_id, order_lines, context=None)
        
        
        if pricelist_id : 
            if self.pool.get('product.pricelist').browse(cr,uid,pricelist_id).currency_id.name.split(' ')[0] == 'EUR' : 
                bank_charges=20
                
            
            elif self.pool.get('product.pricelist').browse(cr,uid,pricelist_id).currency_id.name.split(' ')[0] == 'USD' :
                bank_charges=25
                
            else: 
                bank_charges=0
            
            #import ipdb;ipdb.set_trace()
            res['value'].update({'bank_charges':bank_charges})
            
        return res

    def send_mail(self, cr, uid, ids, context=None):
        ''' Send mail to Odoo users to notify order is generated'''
         
 
        
        sale_val=self.browse(cr,uid,ids[0])
        FROM_MAIL=sale_val.user_id.login
        To_MAIL=['shailesh@routesms.com','india.mis@routesms.com','mehrunisha@routesms.com']
        if '@' and '.com' not in FROM_MAIL and To_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
  
 
        SUBJECT = '''Proforma "{}" generated  '''.format(sale_val.name)         
                         
        MESSAGE = '''Hello Accounts Team ,\n\nProforma Details - \n\nNumber : {} \nOrder Date : {} \nCompany : {}\n\nThanks & Regards \n\n{}
        ''' .format(sale_val.name , sale_val.date_order \
                                    ,sale_val.company_id.name,sale_val.user_id.name)  
         
        #check internet connection
       # connection =check_internet_connection('http://erp.routesms.com')  
        connection =check_internet_connection('http://192.168.0.12:8069')	
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team')) 
        
        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = To_MAIL,
            cc_addr_list = ['sushma.gedam@routesms.com','internalauditor@routesms.com',FROM_MAIL], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = 'ar@routesms.com', 
            password     = 'Routesms@05'
             
            ) 
        
        if notification :
              
            return True
         
        else :
            ''' Sending fail'''
             
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))
# #     
#          ##################FOR TESTING PURPOESE#############
    def send_mail1(self, cr, uid, ids, context=None):
        ''' Send mail to Odoo users to notify Proforma is generated'''
        if context==None : 
             context={}
  

          
        sale_val=self.browse(cr,uid,ids[0])
        #import ipdb;ipdb.set_trace()
        FROM_MAIL=sale_val.user_id.login
        To_MAIL=['shazzwazz20@gmail.com','shazz0020@gmail.com']
        if '@' and '.com' not in FROM_MAIL and To_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
  
  
        SUBJECT = '''Proforma "{}" generated'''.format(sale_val.name)         
                          
        MESSAGE = '''Hello Accounts Team ,\n\nProforma Details - \n\nNumber : {} \nOrder Date : {} \nCompany : {}\n\nThanks & Regards \n\n{}
        ''' .format(sale_val.name , sale_val.date_order \
                                    ,sale_val.company_id.name,sale_val.user_id.name) 
          
        #check internet connection
        #connection =check_internet_connection('http://erp.routesms.com')  

        connection =check_internet_connection('http://192.168.0.12:8069')
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team')) 
         
        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = To_MAIL,
            cc_addr_list = ['shashank.verma@bistacloud.com','shashank_verma0020@outlook.com',FROM_MAIL], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = 'ar@routesms.com', 
            password     = 'Routesms@05'
              
            ) 
          
        if notification :
               
            return True
          
        else :
            ''' Sending fail'''
              
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))
     
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        ''' Overidden Function to send mail to Odoo Users'''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.check_multiple_taxes(cr,uid,ids)        
        self.send_mail(cr, uid, ids, context)
        self.signal_workflow(cr, uid, ids, 'order_confirm')
        return True

    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context is None:
            context = {}
        
        emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
        if emp_id :
            if len(emp_id) >1 :
                raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
            
            return emp_id[0]
        
    def sale_onchange_user(self, cr, uid, ids, user_id, context=None):
        ''' Inherited function to Get employee id if User manually change the Saleperson'''
        
        vals={}
        
       
        if user_id:
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0]})
                
                return {'value':vals}
           
    
    _columns={
              
              #'employee_id':fields.function(default_emp_id,string='Employee User',type='many2one',relation='hr.employee',store=True),
              'employee_id':fields.many2one('hr.employee','Employee User'),
              'partner_bank_id': fields.many2one('res.partner.bank', 'Bank Account',readonly=True,states={'draft': [('readonly', False)]}),
              'bank_charges':fields.float('Bank Charges'),
              #'total_with_bank_charges':fields.function(_bank_charge_total, string='Bank Total', type='char',store=True),
              'total_with_bank_charges':fields.float('Bank Total'),
              'contact_id': fields.many2one('res.partner', 'Contact Person', help="This is contact person related to customer"),
              'use_contact_person_address':fields.boolean('Use contact person address',help="If this box is marked then conatact person address will be printed on report"),

              }

    _defaults={
               
               'employee_id':default_emp_id,
               'use_contact_person_address':False,
               }

# 
# class sale_order_line(osv.osv):
#     _inherit = 'sale.order.line'
# 	
# 
# 
#     def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#             uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#             lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
#         context = context or {}
#         lang = lang or context.get('lang', False)
#         
#         
#         if not partner_id:
#             raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
#         warning = False
#         product_uom_obj = self.pool.get('product.uom')
#         partner_obj = self.pool.get('res.partner')
#         product_obj = self.pool.get('product.product')
#         context = {'lang': lang, 'partner_id': partner_id}
#         partner = partner_obj.browse(cr, uid, partner_id)
#         lang = partner.lang
#         context_partner = {'lang': lang, 'partner_id': partner_id}
# 
#         if not product:
#             return {'value': {'th_weight': 0,
#                 'product_uos_qty': qty}, 'domain': {'product_uom': [],
#                    'product_uos': []}}
#         if not date_order:
#             date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
# 
#         result = {}
#         warning_msgs = ''
#         product_obj = product_obj.browse(cr, uid, product, context=context_partner)
# 
#         uom2 = False
#         if uom:
#             uom2 = product_uom_obj.browse(cr, uid, uom)
#             if product_obj.uom_id.category_id.id != uom2.category_id.id:
#                 uom = False
#         if uos:
#             if product_obj.uos_id:
#                 uos2 = product_uom_obj.browse(cr, uid, uos)
#                 if product_obj.uos_id.category_id.id != uos2.category_id.id:
#                     uos = False
#             else:
#                 uos = False
# 
#         fpos = False
#         if not fiscal_position:
#             fpos = partner.property_account_position or False
#         else:
#             fpos = self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position)
#         if update_tax: #The quantity only have changed
#             result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
# 
#         if not flag:
#             result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
#             if product_obj.description_sale:
#                 result['name'] += '\n'+product_obj.description_sale
#         domain = {}
#         if (not uom) and (not uos):
#             result['product_uom'] = product_obj.uom_id.id
#             if product_obj.uos_id:
#                 result['product_uos'] = product_obj.uos_id.id
#                 result['product_uos_qty'] = qty * product_obj.uos_coeff
#                 uos_category_id = product_obj.uos_id.category_id.id
#             else:
#                 result['product_uos'] = False
#                 result['product_uos_qty'] = qty
#                 uos_category_id = False
#             result['th_weight'] = qty * product_obj.weight
#             domain = {'product_uom':
#                         [('category_id', '=', product_obj.uom_id.category_id.id)],
#                         'product_uos':
#                         [('category_id', '=', uos_category_id)]}
#         elif uos and not uom: # only happens if uom is False
#             result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
#             result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
#             result['th_weight'] = result['product_uom_qty'] * product_obj.weight
#         elif uom: # whether uos is set or not
#             default_uom = product_obj.uom_id and product_obj.uom_id.id
#             q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
#             if product_obj.uos_id:
#                 result['product_uos'] = product_obj.uos_id.id
#                 result['product_uos_qty'] = qty * product_obj.uos_coeff
#             else:
#                 result['product_uos'] = False
#                 result['product_uos_qty'] = qty
#             result['th_weight'] = q * product_obj.weight        # Round the quantity up
# 
#         if not uom2:
#             uom2 = product_obj.uom_id
#         # get unit price
# 
#         if not pricelist:
#             warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
#                     'Please set one before choosing a product.')
#             warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
#         else:
#             #####Adding uid=1 (superuser) to avoid currency acess issue#######
# 
#             price = self.pool.get('product.pricelist').price_get(cr, 1, [pricelist],
#                     product, qty or 1.0, partner_id, {
#                         'uom': uom or result.get('product_uom'),
#                         'date': date_order,
#                         })[pricelist]
#             if price is False:
#                 warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
#                         "You have to change either the product, the quantity or the pricelist.")
# 
#                 warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
#             else:
#                 result.update({'price_unit': price})
#         if warning_msgs:
#             warning = {
#                        'title': _('Configuration Error!'),
#                        'message' : warning_msgs
#                     }
#         return {'value': result, 'domain': domain, 'warning': warning}
#     
