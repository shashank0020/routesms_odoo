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
from datetime import date
import csv
from num2words import num2words

class routesms_api(osv.osv):
    _name = 'routesms.api'
    _description='API to integrate with Odoo application'


    def update_partners(self,cr,uid,vals):
        '''update  '''
        partner_obj=self.pool.get('res.partner')
        
        
        count=0
        vals={}
        vals_line={}
        
        with open('/home/routesms/graphic_partner.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                
                try :

                    partner_id=partner_obj.search(cr,uid,[('name','=',row[1])])
                    
                    partner_id=partner_obj.write(cr,uid,partner_id,{'company_id':6})
                    print 'DONE ------------NUMBER IS =',count

                
                except Exception as E :
                    print 'EXCEPTION = ',count
                    

        
        return True


    def create_partners(self,cr,uid,vals):
        '''partner creation '''
        partner_obj=self.pool.get('res.partner')
        
        
        count=0
        vals={}
        vals_line={}
        
        with open('/home/PAYPAL UK EURO NEW (TILL 15.05.2015) krupali.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                
                try :
                    vals['user_id']=row[0]
                    vals['name']=row[1]
                    vals['street']=row[3]
                    vals['email']=row[4]
                    vals['postpaid']=True
                    vals['customer']=True
                    vals['is_company']=True
                    partner_id=partner_obj.create(cr,uid,vals)
                    #import ipdb;ipdb.set_trace()
                    #create contact perosn
                    
                    vals_line['name']=row[2]
                    vals_line['parent_id']=partner_id
                    vals_line['use_parent_address']=True
                    partner_obj.create(cr,uid,vals_line)
                
                except Exception as E :
                    print count
                    
                
                
        
        return True



    
    def update_supplier_saleperson(self,cr,uid,vals):
        '''update Salesperson '''
        partner_obj=self.pool.get('res.partner')
        partner_ids=partner_obj.search(cr,uid,[('supplier','=',True),('user_id','=',False)])
        
        count=0
       # import ipdb;ipdb.set_trace()
        for part_id in partner_ids :
            count+=1
            print count
            partner_obj.write(cr,uid,[part_id],{'user_id':237})
        
        
        return True
        


    
    def import_invoices(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        #import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/krupali/PAYPAL UK EURO NEW (TILL 15.05.2015) krupali.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    
                    #search partner
#                     if count in [13,41,142] :
                        
                        #import ipdb;ipdb.set_trace()
                        
                    partner_id=partner_obj.search(cr,uid,[('name','=',row[0])])[0]
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[1]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=98#34                    
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=3385#1225
                    
                    
                    #currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',row[4])])[0]
                    vals['currency_id']=currency_id
                    
                    #company
                    company_id=comp_obj.search(cr,uid,[('name','=',row[11])])[0]
                    vals['company_id']=company_id  
                                      
                    #saleperson
                    
                    user_id=user_obj.search(cr,uid,[('name','=',row[12])])[0]
                    vals['user_id']=user_id
                    vals['credit_type']='KRUPALI PAYPAL RSLUK EUR 15may'
                    #vals['partner_bank_id']=55
                    vals['partner_bank_id']=66 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                    product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=product_id                     
                    
                    #desc
                    
                    vals_line['name']=row[6]
                    
                    #account
                    account_id=account_obj.search(cr,uid,[('name','=',row[7])])[0]
                    vals_line['account_id']=account_id                    
                                         
                    vals_line['quantity']=row[8]
                    
                    vals_line['price_unit']=row[9]
                    vals_line['invoice_id'] =invoice_id
                    
                    invoice_line_obj.create(cr,uid,vals_line)
                        
#                     else :
#                         pass
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
                            
            return True    
  
    
    def update_tax_invoice_line(self,cr,uid,vals):
        '''Update Tax amount per invoice line'''
        context={}
        
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        count=0
        for invoice_id in invoice_obj.search(cr,uid,[]) :
            count+=1

                
            if invoice_obj.browse(cr,uid,invoice_id).company_id.id == 3 :
                pass
            else :
                
                for invoice_line_id in invoice_line_obj.search(cr,uid,[('invoice_id','=',invoice_id)]) :
                    
                    res=invoice_line_obj._tax_amount(cr, uid, [invoice_line_id], 'tax_amount', None, context)
                    if res :
                        try :
                            invoice_line_obj.write(cr,uid,invoice_line_id,{'tax_amount':res.values()[0]})
                        except  Exception as E:
                            invoice_line_obj.write(cr,uid,invoice_line_id,{'tax_amount':0.00})
                        
                
        
        
        return True

    def update_period_name(self,cr,uid,vals):
        '''Update period  str value '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        
        for inv_id in inv_ids :
            name='period_to_words'
            count+=1;print count
            month=inv_obj._period_to_words(cr, uid, [inv_id], name, None, {})
            inv_obj.write(cr,uid,inv_id,{'period_to_words':month})
                
        return True    

    def update_total_name(self,cr,uid,vals):
        '''Update Total amount str value '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        
        for inv_id in inv_ids :
            updated_val=''
            amount=inv_obj.browse(cr,uid,inv_id).amount_total
            if amount : 
                numwords=num2words(int(amount)).split('-')
                for i in numwords:
                    b=i.split(' ')
                    for j in b:
        

                        updated_val+=j.capitalize() +' '            
                #updated_val=' '.join([x.capitalize() for x in numwords])
                count+=1;print count
                inv_obj.write(cr,uid,inv_id,{'amount_to_word':updated_val})
                
        return True

    def currency_rate_import(self,cr,uid,vals):
        ''' assign currency rate for INR companies'''
        comp_obj=self.pool.get('res.company')
        currency_obj=self.pool.get('res.currency')
        currency_line_obj=self.pool.get('res.currency.rate')
        comp_ids=comp_obj.search(cr,uid,[])
        counting=0
        
        with open('/home/bista/shanky/routesms/docs/currency_rate_import.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                
                for comp in comp_ids :
                    counting+=1
                    print counting

                        
                    
                    cur_name=comp_obj.browse(cr,uid,comp).currency_id.name
                    if 'GBP' in cur_name :
                        #cur_id    =currency_obj.search(cr,uid,[('company_id','=',comp)])
                        eur=currency_obj.search(cr,uid,[('company_id','=',comp),('name','like','%EUR%')])
                        usd=currency_obj.search(cr,uid,[('company_id','=',comp),('name','like','%USD%')])
                        
                        if eur :
                            
                            value_euro={'currency_id':eur[0],'rate':row[2],'name':row[0]}
                            currency_line_obj.create(cr,uid,value_euro)
                        if usd :
                            
                            value_usd={'currency_id':usd[0],'rate':row[3],'name':row[0]}
                            currency_line_obj.create(cr,uid,value_usd)
                            
            return True
                
            
        


    def create_currency_rate(self,cr,uid,vals):
        
        currency_obj=self.pool.get('res.currency')
        currency_line_obj=self.pool.get('res.currency.rate')
        
        currency_ids=currency_obj.search(cr,uid,[])
        
        count=0
        for currency in currency_ids :
            count+=1;print count
            vals={'currency_id':currency,'name':date.today().strftime('%Y-%m-%d'),'rate':1.00}
            currency_line_obj.create(cr,uid,vals)
            
        return True

    def write_currency(self,cr,uid,vals):
        currency_obj=self.pool.get('res.currency')
        comp_obj=self.pool.get('res.company')
        curr_ids=currency_obj.search(cr,uid,[])
        count=0
        
        for i in curr_ids :
            count+=1;print count
            cur_get_name=currency_obj.browse(cr,uid,i).name + ' (' + currency_obj.browse(cr,uid,i).company_id.name_convention + ')' 
            
            currency_obj.write(cr,uid,i,{'name':cur_get_name})
        
        return True
        
    
    def create_currency(self,cr,uid,vals):
        ''' Create currency for all companies'''
        currency_obj=self.pool.get('res.currency')
        comp_obj=self.pool.get('res.company')
        curr_ids=currency_obj.search(cr,uid,[])
        count=0
        comp_1=0
        
        for cur in curr_ids :
            print '-----------------------CURRENCY'
            count+=1;print count
            cur_get=currency_obj.browse(cr,uid,cur)
            cur_vals={'name':cur_get.name,'rate_silent':cur_get.rate_silent,'rounding':cur_get.rounding,\
                      'symbol':cur_get.symbol,'accuracy':cur_get.accuracy,'position':cur_get.position,\
                      'base':cur_get.base,'active':True}
            comp_ids=comp_obj.search(cr,uid,[])
            
            for comp in comp_ids :
                
                print '-----------------------CREATING NEW CURRENCY'
                comp_1+=1;print comp_1
                if comp==1:
                    pass
                else:
                   
                    name_1=cur_get.name
                    comp_name=comp_obj.browse(cr,uid,comp).name_convention
                    updated_name=name_1 + ' (' + comp_name +')'
                    cur_vals.update({'company_id':comp,'name':updated_name})
                    currency_obj.create(cr,uid,cur_vals)
                
        return True
    
    
    def assign_companies_to_bank(self,cr,uid,vals):
        '''Assign companies to bank '''
        #import ipdb;ipdb.set_trace()
        bank_obj=self.pool.get('res.partner.bank')
        comp_obj=self.pool.get('res.company')
        bank_ids=bank_obj.search(cr,uid,[])
        
        count=0
        for id in bank_ids :
            count+=1
            partner_id=bank_obj.browse(cr,uid,id).partner_id.id
            if partner_id :
                
                comp_id=comp_obj.search(cr,uid,[('partner_id','=',partner_id)])
                if comp_id :
                    bank_obj.write(cr,uid,id,{'company_id':comp_id[0]})
                    print count
                    print 'ID',id
        return True
                
            
            
    
    
    def write_sequence(self,cr,uid,vals):
        ''' Update sequence name'''
        seq_obj=self.pool.get('ir.sequence')
        seq_ids=seq_obj.search(cr,uid,[])
        
        count=0
        for seq in seq_ids :
            count+=1;print count
            if seq_obj.browse(cr,uid,seq).company_id.id :
                updated_name=seq_obj.browse(cr,uid,seq).name + ' ' + seq_obj.browse(cr,uid,seq).company_id.name_convention
                seq_obj.write(cr,uid,seq,{'name':updated_name})
                    
        return True
    
    def write_account(self,cr,uid,vals):
        ''' Update account name'''
        acc_obj=self.pool.get('account.account')
        acc_ids=acc_obj.search(cr,uid,[])
        
        count=0
        for acc in acc_ids :
            count+=1;print count
            updated_name=acc_obj.browse(cr,uid,acc).name + ' ' + acc_obj.browse(cr,uid,acc).company_id.name_convention
            acc_obj.write(cr,uid,acc,{'name':updated_name})
        return True    
    
    def write_journals(self,cr,uid,vals):
        ''' Update journals name'''
        journal_obj=self.pool.get('account.journal')
        journal_ids=journal_obj.search(cr,uid,[])
        
        count=0
        for journal in journal_ids :
            count+=1;print count
            updated_name=journal_obj.browse(cr,uid,journal).name + ' ' + journal_obj.browse(cr,uid,journal).company_id.name_convention
            journal_obj.write(cr,uid,journal,{'name':updated_name})
        return True



    def create_employee(self,cr, uid,vals):
        
        emp_li=[]
        user_obj=self.pool.get('res.users')
        employee_obj=self.pool.get('hr.employee')
        
        emp_ids=employee_obj.search(cr,uid,[])
        counting=0
        
        for emp_id in  emp_ids:
            emp_user_id=employee_obj.browse(cr,uid,emp_id).user_id.id
            emp_li.append(emp_user_id)
        
        user_ids=user_obj.search(cr,uid,[])
        for user_id in user_ids:
            if user_id ==315:
                
                emp_user_id=employee_obj.browse(cr,uid,emp_id).name
            else:
                pass
            
            if user_id in emp_li :
                pass
            else:
                
                login_name=user_obj.browse(cr,uid,user_id).login
                name_val=login_name.split('@')
                update_login_name=name_val[0]+ ' Test'
                employee_obj.create(cr,uid,{'name':update_login_name,'user_id':user_id})
                counting+=1;print counting;print login_name
        return True
        

    def password(self,cr, uid, vals):
        ''' Test XMLRPC API'''
        #import ipdb;ipdb.set_trace()
        cr.execute(''' update res_users set password=%s where id=%s''',(vals[0],vals[1]))
        
        return True
    
    
    def allowed_companies(self,cr,uid,id,allowed_comp):
        
        cr.execute(''' delete from res_company_users_rel  where user_id=%s''',(id,))
        for comp in allowed_comp :
             
             
            cr.execute(''' insert into res_company_users_rel (cid,user_id) VALUES(%s,%s)''',(comp,id))
            
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
       # vals=[ {'odoo_customer_id':'R110002','routesms_remark':'some remark','account_type':'prepaid' } ]
        
        
        obj=self.pool.get('res.partner')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            if len(vals) > 1:
                return {'result':0,'error':'Multiple user detail not accepted'}
            try:
                #import ipdb;ipdb.set_trace()
                if vals[0]['account_type']=='prepaid' :
                    cust_type=[('prepaid','=',True),('postpaid','=',False)]
                    
                elif vals[0]['account_type']=='postpaid' :
                    cust_type=[('postpaid','=',True),('prepaid','=',False),]
                    
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
        
        #import ipdb;ipdb.set_trace()
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try :
         #       import ipdb;ipdb.set_trace()
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Invoices not accepted'}
                
                for val in vals :
                    invoice.update({'credit_type':val['params']['credit_type']})
                    transaction_type=["out_invoice","out_refund","in_invoice","in_refund"]
                    if (val['params']['transaction_type'] in transaction_type): 
                        
                        invoice.update({'type':val['params']['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                        
                    
#                     #assign journal
#                     
#                     
#                     
#                     if invoice['type'] =='out_refund' :
#                         invoice.update({'journal_id':3})
#                         
#                     elif invoice['type'] =='in_invoice' :
#                         invoice.update({'journal_id':2})
#                         
#                     elif invoice['type'] =='in_refund' :
#                         invoice.update({'journal_id':4})
                        
                                        
                    #assign dates
                    
                    invoice.update({'date_invoice':val['params']['invoice_date']})
                    invoice.update({'date_due':val['params']['due_date']})
                    
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['params']['currency_id'])])
                    if currency_id :
                        invoice.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    


                    

                    
#                     #product search
#                     
#                     template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
#                     if template_id :
#                         
#                         if len(template_id) > 1:
#                             return {'result':0,'error':'Multiple products with same name found on Odoo'}
# 
#                         product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
#                         
#                         if product_id :
#                             invoice_line.update({'product_id':product_id[0]})
#                             invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
#                             invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
#                             
#                             if invoice['type'] in ['out_invoice','out_refund']:
#                                 invoice_line.update({'account_id':189})
#                                 
#                             
#                                 
#                             invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
#                         
#                         else :
#                             
#                             return {'result':0,'error':'Product not found'}
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
                        invoice.update({'remark':val['params']['routesms_remark']})
                    
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



                    #assign journal
                    company_id=company_id[0]
                    if company_id == 1 : #RSL Group
                        
                     
                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':3})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                            
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':2})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':4})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':1})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                        
                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}
                            
                                                        
#                     elif company_id == 3 : # 29 THREE HOLIDAYS PVT. LTD 
# 
#                         if invoice['type'] =='out_refund' :
#                             invoice.update({'journal_id':12})
#                             
#                         elif invoice['type'] =='in_invoice' :
#                             invoice.update({'journal_id':149})
#                             
#                         elif invoice['type'] =='in_refund' :
#                             invoice.update({'journal_id':13})
#                             
#                         elif invoice['type'] =='out_invoice' :
#                             invoice.update({'journal_id':148})                        
# 
#                         else :
#                             
#                             return {'result':0,'error':'Invalid Invoice Type format'}                        
                        
                    elif company_id == 4 : # AHANA ENTERTAINMENT PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':20})
                            invoice.update({'product_account':729})
                            invoice.update({'account_id':685})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':19})
                            invoice.update({'product_account':739})
                            invoice.update({'account_id':577})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':21})
                            invoice.update({'product_account':739})
                            invoice.update({'account_id':577})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':18})  
                            invoice.update({'product_account':729})
                            invoice.update({'account_id':685})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                        
                                                

                    elif company_id == 5 : # GRAPHIXIDE INC

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':68})
                            invoice.update({'product_account':2349}) 
                            invoice.update({'account_id':2305})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':67})
                            invoice.update({'product_account':2359})
                            invoice.update({'account_id':2197})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':69})
                            invoice.update({'product_account':2359})
                            invoice.update({'account_id':2197})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':66})       
                            invoice.update({'product_account':2349})                  
                            invoice.update({'account_id':2305})
                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                    

                    elif company_id == 6 : #  GRAPHIXIDE SERVICES PVT.LTD

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':28})
                            invoice.update({'product_account':999}) 
                            invoice.update({'account_id':955})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':27})
                            invoice.update({'product_account':1009}) 
                            invoice.update({'account_id':847})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':29})
                            invoice.update({'product_account':1009})
                            invoice.update({'account_id':847}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':26})       
                            invoice.update({'product_account':999})
                            invoice.update({'account_id':955})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                    
                    
                    elif company_id == 7 : #  REMARKABLE INNOVATIONS 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':76})
                            invoice.update({'product_account':2619}) 
                            invoice.update({'account_id':2575})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':75})
                            invoice.update({'product_account':2629}) 
                            invoice.update({'account_id':2467})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':77})
                            invoice.update({'product_account':2629}) 
                            invoice.update({'account_id':2467})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':74})       
                            invoice.update({'product_account':2619})
                            invoice.update({'account_id':2575})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                                        
                    elif company_id == 8 : #  ROUTESMS SOLUTIONS NIGERIA LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':84})
                            invoice.update({'product_account':2889}) 
                            invoice.update({'account_id':2845})  
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':83})
                            invoice.update({'product_account':2899})
                            invoice.update({'account_id':2737})  
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':85})
                            invoice.update({'product_account':2899})
                            invoice.update({'account_id':2737})  
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':82})       
                            invoice.update({'product_account':2889})  
                            invoice.update({'account_id':2845})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         


                    elif company_id == 9 : #  ROUTESMS SOLUTIONS FZE

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':92})
                            invoice.update({'product_account':3159}) 
                            invoice.update({'account_id':3115})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':91})
                            invoice.update({'product_account':3169}) 
                            invoice.update({'account_id':3007})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':93})
                            invoice.update({'product_account':3169})
                            invoice.update({'account_id':3007}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':90})       
                            invoice.update({'product_account':3159})
                            invoice.update({'account_id':3115})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                          
                                        
                    elif company_id == 10 : #  ROUTESMS SOLUTIONS LIMITED 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':36})
                            invoice.update({'product_account':1269})
                            invoice.update({'account_id':1225}) 
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':35})
                            invoice.update({'product_account':1279})
                            invoice.update({'account_id':1117}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':37})
                            invoice.update({'product_a13479ccount':1279})
                            invoice.update({'account_id':1117}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':34})       
                            invoice.update({'product_account':1269}) 
                            invoice.update({'account_id':1225})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                    
                    elif company_id == 11 : #  ROUTESMS SOLUTIONS (UK) LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':100})
                            invoice.update({'product_account':3429}) 
                            invoice.update({'account_id':3385})       
                            
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':99})
                            invoice.update({'product_account':3439})
                            invoice.update({'account_id':3277}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':101})
                            invoice.update({'product_account':3439})
                            invoice.update({'account_id':3277}) 
                            
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':98}) 
                            invoice.update({'product_account':3429})
                            invoice.update({'account_id':3385})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                    


                    elif company_id == 12 : #  ROUTEVOICE LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':108})
                            invoice.update({'product_account':3699})
                            invoice.update({'account_id':3655})      
                              
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':107})
                            invoice.update({'product_account':3709})
                            invoice.update({'account_id':3547})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':109})
                            invoice.update({'product_account':3709})
                            invoice.update({'account_id':3547})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':106}) 
                            invoice.update({'product_account':3699})
                            invoice.update({'account_id':3655})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                                        

                    elif company_id == 13 : #  SANRAJ INFRA DEVELOPERS PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':108})
                            invoice.update({'product_account':1539})
                            invoice.update({'account_id':1495})        
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':107})
                            invoice.update({'product_account':1549})
                            invoice.update({'account_id':1387})  
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':109})
                            invoice.update({'product_account':1549})
                            invoice.update({'account_id':1387})  
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':42}) 
                            invoice.update({'product_account':1539})  
                            invoice.update({'account_id':1495})                    

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                    

                    elif company_id == 14 : #  SPECTRA TELESERVICES PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':52})
                            invoice.update({'product_account':1809})  
                            invoice.update({'account_id':1765})     
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':51})
                            invoice.update({'product_account':1819})
                            invoice.update({'account_id':1657}) 
  
  
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':53})
                            invoice.update({'product_account':1819})
                            invoice.update({'account_id':1657})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':50}) 
                            invoice.update({'product_account':1809})
                            invoice.update({'account_id':1765})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}      
                                                                                          
                    elif company_id == 15 : #  SPER

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':116})
                            invoice.update({'product_account':3969})  
                            invoice.update({'account_id':3925})      
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':115})
                            invoice.update({'product_account':3979})
                            invoice.update({'account_id':3817})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':117})
                            invoice.update({'product_account':3979})
                            invoice.update({'account_id':3817})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':114}) 
                            invoice.update({'product_account':3969})
                            invoice.update({'account_id':3925})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                                                                             

                    elif company_id == 16 : #  SPHERE EDGE CONSULTING INDIA PVT. LTD

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':60})
                            invoice.update({'product_account':2079})       
                            invoice.update({'account_id':2035}) 
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':59})
                            invoice.update({'product_account':2089})
                            invoice.update({'account_id':1927}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':61})
                            invoice.update({'product_account':2089})
                            invoice.update({'account_id':1927}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':58}) 
                            invoice.update({'product_account':2079})
                            invoice.update({'account_id':2035})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'} 
                    
                    
                    else :
                        
                        return {'result':0,'error':'Company - Journal Error'}
                    
                            
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
                            invoice_line.update({'account_id':invoice['product_account']})                              
                            invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
                        
                        else :
                            
                            return {'result':0,'error':'Product not found'}


                                   
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
#     vals=[  {'transaction_type':'receipt','currency_id':'INR','partner_id':'R100001','routesms_remark':'remark','date':'2015-03-30','amount':12,
#              'reference': 'Payment Ref' ,'company_name':'RSL (Group)','saleperson_name': 'Karishma Ghaghda' } ]

        


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
                    
                    #assign journal
                    
                    if val['currency_id'] =='EUR (RG)' :
                        voucher.update({'journal_id':162})
                    
                    elif val['currency_id'] =='INR (RG)' :
                        voucher.update({'journal_id':8}) 
                        

#AHANA ENTERTAINMENT PVT. LTD

                    elif val['currency_id'] =='INR (AEP)' :
                        voucher.update({'journal_id':25}) 

#GRAPHIXIDE INC

                    elif val['currency_id'] =='USD (GRAPH INC)' :
                        voucher.update({'journal_id':73}) 


#GRAPHIXIDE SERVICES PVT.LTD

                    elif val['currency_id'] =='INR (GSPL)' :
                        voucher.update({'journal_id':33})                         
                        

#REMARKABLE INNOVATIONS

                    elif val['currency_id'] =='USD (REI)' :
                        voucher.update({'journal_id':81})                         
                                                
                        
#ROUTESMS SOLUTIONS FZE

                    elif val['currency_id'] =='AED (RFZE)' :
                        voucher.update({'journal_id':97})

                    elif val['currency_id'] =='USD (RFZE)' :
                        voucher.update({'journal_id':45})   
                                                                         
                    elif val['currency_id'] =='EUR (RFZE)' :
                        voucher.update({'journal_id':146})   
                                                                                                 
#ROUTESMS SOLUTIONS LIMITED                                     

                    elif val['currency_id'] =='INR (RSL)' :
                        voucher.update({'journal_id':41})

                    elif val['currency_id'] =='EUR (RSL)' :
                        voucher.update({'journal_id':147})   
                                                                         
                    elif val['currency_id'] =='USD (RSL)' :
                        voucher.update({'journal_id':132}) 
       
#ROUTESMS SOLUTIONS NIGERIA LIMITED
                    elif val['currency_id'] =='NGN (RSNL)' :
                        voucher.update({'journal_id':134})

# ROUTESMS SOLUTIONS (UK) LIMITED

                    elif val['currency_id'] =='GBP (RSUK)' :
                        voucher.update({'journal_id':105})

                    elif val['currency_id'] =='EUR (RSUK)' :
                        voucher.update({'journal_id':141})                        
                        
# ROUTEVOICE LIMITED
                    elif val['currency_id'] =='HKD (RVL)' :
                        voucher.update({'journal_id':113})

# SANRAJ INFRA DEVELOPERS PVT. LTD

                    elif val['currency_id'] =='INR (SAN)' :
                        voucher.update({'journal_id':49})
                        
# SPECTRA TELESERVICES PVT. LTD

                    elif val['currency_id'] =='INR (SPECTRA)' :
                        voucher.update({'journal_id':57})
                         
# SPER

                    elif val['currency_id'] =='INR (SPECTRA)' :
                        voucher.update({'journal_id':121})
                        
# SPHERE EDGE CONSULTING INDIA PVT. LTD
                        
                    elif val['currency_id'] =='INR (SPC)' :
                        voucher.update({'journal_id':65})                        
                        
           
                    else:
                        return {'result':0,'error':'Journal not set for currency'}
                        
                           
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['routesms_remark']})
                        voucher.update({'partner_id':partner_id[0]})
                        voucher.update({'remark':val['routesms_remark']})
                    
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
                                    
                         
                    #create voucher
                    try :
                        voucher['amount']=float(voucher['amount'])
                        
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




