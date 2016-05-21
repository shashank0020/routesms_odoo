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
from openerp import models, fields, api, _


class routesms_api(osv.osv):
    _name = 'routesms.api'
    _description='API to integrate with Odoo application'
    
    

    def password(self,cr, uid, vals):
        ''' Test XMLRPC API'''
        #import ipdb;ipdb.set_trace()
        cr.execute(''' update res_users set password=%s where id=%s''',(vals[0],vals[1]))
        
        return True
    
        
    def test_function(self,cr, uid, vals):
        ''' Test XMLRPC API'''
        
        if vals :
            
            return {'key':'XMLRPC api successfull!!!!'}
        
        return {'key':'XMLRPC api successfull!!!!'}
    
    
    def product_search(self,cr, uid, vals):
        ''' Return 1 if product found else 0'''
        ###############FORMAT#################
        #[ {'product_name':'product name'  } ]
#        vals=[ {'product_name':'Enterprise Messaging (Bulk SMS)'  } ]
        
        prod_tmpl_obj=self.pool.get('product.template')
        prod_obj=self.pool.get('product.product')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        if vals :
            try:
                
                if len(vals) >1:
                    return {'result':0,'error':'Multiple product detail not accepted'}
                template_id=prod_tmpl_obj.search(cr,uid,[('name','=',vals[0]['product_name'])])
                if template_id :
                    if len(template_id) > 1:
                        return {'result':0,'error':'Multiple products with same name found on Odoo'}
                    
                    prod_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])
                    if prod_id :
                        return 1
                    
                    else :
                        return 0
                    
                else :
                    return 0
            
            except Exception as e:
                return 0

        return 0
    

    def company_search(self,cr, uid, vals):
        ''' Return 1 if company found else 0'''
        ###############FORMAT#################
        #[ {'company_name':'company name'  } ] 
        #vals=[ {'company_name':'29 Three Holidays Pvt. Ltd'  } ]       
        obj=self.pool.get('res.company')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try:
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple companies detail not accepted'}
                    
                comp_id=obj.search(cr,uid,[('name','=',vals[0]['company_name'])])
                if len(comp_id) > 1 :
                    return {'result':0,'error':'Multiple company with same name found on Odoo'}
                
                if comp_id :
                    return 1

                else:
                    return 0

            except Exception as exception_log:
                return {'result':0,'error':exception_log}
        
        return 0
    
        
    def user_search(self,cr,uid,vals):
        ''' Return 1 If customer exist else 0 '''
        ###############FORMAT#################
        #[ {'odoo_customer_id':odoo_customer_id,'routesms_remark':'routesms_remark'  } ]
        #vals=[ {'odoo_customer_id':'R110085','routesms_remark':'some remark','prepaid':True,'postpaid':False  } ]
        vals=[ {'odoo_customer_id':'R110085','routesms_remark':'some remark','account_type':'postpaid' } ]
        
        obj=self.pool.get('res.partner')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            if len(vals) > 1:
                return {'result':0,'error':'Multiple user detail not accepted'}
            try:
                if vals[0]['account_type']=='prepaid' :
                    cust_type=[('prepaid','=',True),('postpaid','=',False)]
                    
                elif vals[0]['account_type']=='postpaid' :
                    cust_type=[('prepaid','=',False),('postpaid','=',True)]
                    
                else :
                    return {'result':0,'error':'Invalid account type'}
                
                partner_id=obj.search(cr,uid,[('partner_sequence','=',vals[0]['odoo_customer_id']),cust_type[0]])
                if len(partner_id) > 1 :
                    return {'result':0,'error':'Multiple partner with same ID found on Odoo'}
                if partner_id :
                    obj.write(cr,uid,partner_id,{'routesms_remark':vals[0]['routesms_remark']})
                    return 1
                else:
                    return 0
            
            except Exception as e:
                return 0
        return 0
    
    
            
    def user_invoice(self,cr,uid,vals):
        ''' return 1 if invoice created else 0 on fail'''
        
        ############FORMAT#################
# [ {'params': {'currency_id': 'INR', 'due_date': 'yy-mm-dd', 'user_id': 'Saleperson', 'product_detail': [{'price_unit': 0.0, 'product_id': 'product name', 'quantity': 1}], 'partner_bank_id': 'Account Number', 'invoice_date': 'yy-mm-dd', 'partner_id': 'your_customer_id','routesms_remark':'Remark', 'company_id': 'Company Name'}} ]
#
#         vals=[ {'params': {'credit_type':'credit_type','transaction_type':'out_invoice','currency_id': 'INR', 'due_date': '2015-01-10', 'saleperson_name': 'Karishma Ghaghda',\
#                             
#             'product_detail': [{'price_unit': 2000.0, 'product_name': 'Enterprise Messaging (Bulk SMS)', \
#             'quantity': 1}], 'invoice_date': '2015-03-30', 'partner_id': 'R110054','routesms_remark':'some remark', 'company_id': \
#             'RSL (Group)'}} ]
        
        currency_obj=self.pool.get('res.currency')
        users_obj=self.pool.get('res.users')
        bank_obj=self.pool.get('res.partner.bank')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        prod_tmpl_obj=self.pool.get('product.template')
        prod_obj=self.pool.get('product.product')
        
        invoice={}
        invoice_line={}
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try :
                
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Invoices not accepted'}
                
                for val in vals :
                    invoice.update({'credit_type':val['params']['credit_type']})
                    transaction_type=["out_invoice","out_refund","in_invoice","in_refund"]
                    if (val['params']['transaction_type'] in transaction_type): 
                        
                        invoice.update({'type':val['params']['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                        
                    
                    #assign journal
                    if invoice['type'] =='out_refund' :
                        invoice.update({'journal_id':3})
                        
                    elif invoice['type'] =='in_invoice' :
                        invoice.update({'journal_id':2})
                        
                    elif invoice['type'] =='in_refund' :
                        invoice.update({'journal_id':4})
                        
                                        
                    #assign dates
                    
                    invoice.update({'date_invoice':val['params']['invoice_date']})
                    invoice.update({'date_due':val['params']['due_date']})
                    
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['params']['currency_id'])])
                    if currency_id :
                        invoice.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    


                    

                    
                    #product search
                    
                    template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
                    if template_id :
                        
                        if len(template_id) > 1:
                            return {'result':0,'error':'Multiple products with same name found on Odoo'}

                        product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
                        
                        if product_id :
                            invoice_line.update({'product_id':product_id[0]})
                            invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
                            invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
                            
                            if invoice['type'] in ['out_invoice','out_refund']:
                                invoice_line.update({'account_id':189})
                                
                            
                                
                            invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
                        
                        else :
                            
                            return {'result':0,'error':'Product not found'}
#                     #search bank
#                     
#                     bank_id=bank_obj.search(cr,uid,[('acc_number','=',val['params']['partner_bank_id'])])
#                     if bank_id :
#                         
#                         invoice.update({'partner_bank_id':bank_id[0]})
#                         
#                     else :
#                         
#                         return {'result':0,'error':'Bank Account number found'}
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['params']['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['params']['routesms_remark']})
                        invoice.update({'partner_id':partner_id[0]})
                    
                    else :
                        return {'result':0,'error':'Customer not found'}
                    

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['params']['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             invoice.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
# 
#                     
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        invoice.update({'user_id':saleperson_id})
                        
                    else:
                        invoice.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    

                    #emloyee id search
                                        
                    emp_id=invoice_obj.default_emp_id(cr,invoice['user_id'],context=None)
                    if isinstance(emp_id,(int)):
                        invoice.update({'employee_id':emp_id})
                        
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}
                                         
                    #assign partner account id
                    
                    if invoice['type'] in ['out_invoice','out_refund' ] :
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_receivable.id
                        
                        
                    elif invoice['type'] in ['in_invoice','in_refund' ]:
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_payable.id
                        
                    else :
                        return {'result':0,'error':'Account not assigned to user'}
                    
                    invoice.update({'account_id':account_id})
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['params']['company_id'])])
                    if company_id:
                        invoice.update({'company_id':company_id[0]})
                    
                    else :
                        return {'result':0,'error':'Company not found'}
                    
                                    
                    #create invoice
                    try :
                        
                        
                        new_invoice_id=invoice_obj.create(cr,uid,invoice)
                        
                    except Exception as invoice_create_exception :
                        return {'result':0,'error':invoice_create_exception}
                    
                    
                    #create invoice line
                    try :
                        
                        invoice_obj.write(cr, uid, [new_invoice_id], {'invoice_line': [(0, 0, invoice_line)]})
                        return 1
                        
                    except Exception as invoice_line_create_exception :
                        return {'result':0,'error':invoice_line_create_exception}
                
                    
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0     



    def customer_register_payment(self,cr,uid,vals):
        ''' return 1 if voucher created else 0 on fail'''
        ############FORMAT#################
#         vals=[  {'transaction_type':'receipt','currency_id':'currency code','partner_id':'customer odoo id','routesms_remark':'remark','date':'yyyy-mm-dd','amount':0.0,
#             'reference': 'Payment Ref' ,'company_name':'company name','saleperson_name': 'saleperson name' } ]

# 
#     
        
#         vals=[  {'transaction_type':'receipt','currency_id':'INR','partner_id':'R110054','routesms_remark':'remark','date':'2015-03-30','amount':12.22,
#             'reference': 'Payment Ref' ,'company_name':'RSL (Group)','saleperson_name': 'Karishma Ghaghda' } ]


        currency_obj=self.pool.get('res.currency')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        voucher_obj=self.pool.get('account.voucher')
        journal_obj=self.pool.get('account.journal')
        users_obj=self.pool.get('res.users')
        
        voucher={}
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}


        if vals :
            try :
                
                
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Payments not accepted'}
                
                for val in vals :
                    
                    transaction_type=["receipt","purchase"]
                    if (val['transaction_type'] in transaction_type): 
                        
                        voucher.update({'type':val['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                    
                    #assign account
                    if val['transaction_type']=="receipt":
                         voucher.update({'account_id':270})
                    
                    else:
                        return {'result':0,'error':'Invalid attempt '}
                    
                        
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['currency_id'])])
                    if currency_id :
                        voucher.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['routesms_remark']})
                        voucher.update({'partner_id':partner_id[0]})
                    
                    else :
                        return {'result':0,'error':'Customer not found'}
                    
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['company_name'])])
                    if company_id:
                        voucher.update({'company_id':company_id[0]})
                        
                    else :
                        return {'result':0,'error':'Company not found'}

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             voucher.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        voucher.update({'user_id':saleperson_id})
                            
                    else :
                        voucher.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    
                   
                    
                    
                    #emloyee id search
                    
                    emp_id=voucher_obj.default_emp_id(cr,voucher['user_id'],context=None)
                    if isinstance(emp_id,(int)):
                        voucher.update({'employee_id':emp_id})
                        
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}

                    
                    #assign remaining values
                    voucher.update({'date':val['date']})
                    voucher.update({'amount':val['amount']})
                    voucher.update({'journal_id':8})                    
                         
                    #create voucher
                    try :
                        
                        voucher_obj.create(cr,uid,voucher)
                        
                    except Exception as voucher_create_exception :
                        return {'result':0,'error':voucher_create_exception}
                    
                
                    return 1
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0     



#     def customer_insert_script(self,cr,uid,vals):
#         

#
#         values=(vals['is_company'],vals['name'],vals['routesms_cust_id'],vals['street'],vals['country_id']/
#                 vals['email'],vals['vat'],vals['fax'],vals['user_id'],vals['vertical'],vals['customer'])
#         
#         values=(vals['is_company'],vals['name'],vals['routesms_cust_id'],vals['street'].encode('ascii','ignore')
#                 ,vals['country_id'],vals['email'],vals['vat'],vals['fax'],vals['user_id'],vals['vertical'],vals['customer'])
#         
#         
#         cr.execute(''' insert into res_partner (is_company,name,routesms_cust_id,street,country_id,email,\
#                      vat,phone,fax,user_id,vertical,customer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''\
#                      ,values)
# 
#         
#     
#         master_partner_id=map(lambda x:x[0], cr.fetchall())
#         return master_partner_id
# 
#     def contact_insert_script(self,cr,uid,vals):
#         
#         
#         values=(vals['parent_id'],vals['name'],vals['use_parent_address'],vals['type'],vals['customer'])
#         
# 
#         
#         cr.execute(''' insert into res_partner (parent_id,name,use_parent_address,type,customer) /
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',values)
#                 
# 
#         
#     
#         contact_partner_id=map(lambda x:x[0], cr.fetchall())
#         return contact_partner_id
#                 
#         
#         
        
        
            
routesms_api()




