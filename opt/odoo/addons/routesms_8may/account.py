# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv, fields
from openerp.tools.float_utils import float_round as round
from openerp.tools.translate import _
from lxml import etree
import datetime
import itertools
from lxml import etree
from num2words import num2words


class account_account(osv.osv):
     _inherit = "account.account"
     
     
     def create(self, cr, uid, vals, context=None):
        ''' Overiden method concanate account name and company naming convention'''
        user_obj=self.pool.get('res.users')
        company_obj=self.pool.get('res.company')
        account_id = super(account_account , self).create(cr, uid, vals, context)
        updated_name=vals['name'] + ' '+  company_obj.browse(cr,uid,vals['company_id']).name_convention 
        self.write(cr,uid,account_id,{'name':updated_name})    
        return account_id


        


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context is None:
            context = {}
        
        emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
        if emp_id :
            if len(emp_id) >1 :
                raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
            
            return emp_id[0]
        
        else :
            return 0


    def account_onchange_user(self, cr, uid, ids, user_id, context=None):
        ''' Inherited function to Get employee id if User manually change the Saleperson'''
        
        vals={}
        
        
        if user_id:
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0]})
                
                return {'value':vals}
        else:
            
            return {'value':vals.update({'employee_id':False})}
            
    def _amount_to_word(self,cr, uid, ids, name, args, context=None):
        ''' store amount in char format '''
        res={}
        
        for invoice in self.browse(cr, uid, ids) :
            total_amount=invoice.amount_total
            if total_amount :
                 res[invoice.id]=num2words(int(total_amount))
                
            else :
                res[invoice.id]=''
        return res    
        

    _columns = {

        'contact_id': fields.many2one('res.partner', 'Contact Person', help="This is contact person related to customer"),
        'employee_id':fields.many2one('hr.employee','Employee User'),
        'credit_type':fields.char('Credit Type'),
        'remark':fields.text('Remark'),
        'amount_to_word':fields.function(_amount_to_word,string='Lead Status', type='char',store=True),
        
        
        


    }
    
    _defaults={
               
               'employee_id':default_emp_id,
               
               
               }    


    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        ''' Make customer invoice from supplier invoice for 293 holidays'''
        res= super(account_invoice, self).copy(cr, uid, id, default, context=context)
    
        
        if self.pool.get('res.users').browse(cr,uid,uid).company_id.id == 3 and context.get('type') == 'in_invoice' :
            
            if self.browse(cr,uid,id).partner_id.customer == True :
            
                cr.execute(''' update account_invoice set type='out_invoice' where id=%s ''',(id,))
            
            else :
                
                raise osv.except_osv(_('Error!'), _('Partner is not a Customer.'))
            
        return res
        
    def invoice_validate(self,cr,uid,ids):
        ''' Method overided to restrict invoices created for RSL group'''

        if self.browse(cr,uid,ids[0]).date_invoice :
            pass
        
        else :
            raise osv.except_osv(_('Error!'),_("Invoice Date is required !"))
                
        if self.browse(cr,uid,ids[0]).company_id.id== 3 :
            return self.write(cr,uid,ids,{'state': 'open'})

        
        vals={'currency_id':self.browse(cr,uid,ids[0]).currency_id.id,'date_invoice':self.browse(cr,uid,ids[0]).date_invoice}
        currency_status=self.currency_set(cr,uid,vals,{})
        
        if currency_status :
              
            if self.browse(cr,uid,ids[0]).company_id.id== 1 :
                raise osv.except_osv(_('Error!'), _('Invoice cannot be validated for RSL (Group) Company.'))
              
            return self.write(cr,uid,ids,{'state': 'open'})
        else :
            raise osv.except_osv(_('Error!'),_("Contact Technical Team!"))
  
      
  
    def currency_set(self, cr, uid, vals, context=None):
        ''' check currency setup date'''
                 
            
                ###############OlD #####################   
#                 rate_date=curreny_rate_line.browse(cr,uid,currency_ids).name
#                 current_date=datetime.datetime.now().strftime('%Y-%m-%d')
#                 format=rate_date.rsplit(' ')
#                 format_updated=format[0].split('-')
#                 li=[format_updated[0],format_updated[1],format_updated[2]]
#                 format_current_date=current_date.split('-')
#                 li_current_date=[format_current_date[0],format_current_date[1],format_current_date[2]]                    
#                 if li== li_current_date :
#                         
#                     result.append(rate_date)
                    
#                         
#             if result :
#                 return True        
            
            
        curreny_rate_line=self.pool.get('res.currency')
        curreny_rate_line=self.pool.get('res.currency.rate')
        result=list()
 
        if self.pool.get('res.users').browse(cr,uid,uid).company_id.id==3 :
            return True
          
        currency_val=curreny_rate_line.search(cr,uid,[('currency_id','=',vals['currency_id'])])
        if currency_val :
                
            
            for currency_ids in currency_val :
                rate_date=curreny_rate_line.browse(cr,uid,currency_ids).name
                
                result.append(rate_date.split(' ')[0])
            
            if vals['date_invoice'] in result :
                return True

                
            else :
                raise osv.except_osv(_('Warning!'),_("Invoice cannot be created,Please set currency rate"))
                
        else:
            raise osv.except_osv(_('Error!'),_("Invoice cannot be created. No currency found!"))
              
           
    



 
#     
# #     def create(self, cr, uid, vals, context=None):
#         
#         obj_sequence=self.pool.get('ir.sequence')
#         user_obj=self.pool.get('res.users')
#         import ipdb;ipdb.set_trace()
#         try :
#             
#             if user_obj.browse(cr,uid,uid).company_id.name== '29 Three Holidays Pvt. Ltd':
#                 
#                 user_vertical_type=user_obj.browse(cr,uid,uid).holiday_vertical_list
#                 if user_vertical_type == 'air' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','AIR TICKETING')])
#                     if seq_id :
#                         seq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals['name'] =seq_no
#                         import ipdb;ipdb.set_trace()
#                         
#                         invoice_id = super(osv.osv , self).create(cr, uid, vals, context)
#                         return invoice_id
#                     
#                     else :
#                         raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
#                 
#                 elif user_vertical_type == 'tour' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','TOURS PACKAGES')])
#                     if seq_id :
#                         sreturn reseq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals['partner_sequence'] =seq_no     
#                         invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#                         return invoice_id           
#                     
#                     else :
#                         raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
#                     
#                 elif user_vertical_type == 'hotel' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','HOTEL BOOKING')])
#                     if seq_id :
#                         seq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals['partner_sequence'] =seq_no      
#                         invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#       
#                      return invoice_id          
#                     
#                     else :
#                         raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
#                         
#                                     
#     
#                 elif user_vertical_type == 'visa' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','VISA SERVICE')])
#                     if seq_id :
#                         seq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals['partner_sequence'] =seq_no 
#                         invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#                         return invoice_id               
#                     
#                     else :
#                         raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
#                                     
#                                     
#                 elif user_vertical_type == 'rent' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','RENT A CAB SERVICE')])
#                     if seq_id :
#                         seq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals['partner_sequence'] =seq_no   
#                         invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#                         return invoice_id             
#                     
#                     else :
#                         raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
#                              
#     
#                 elif user_vertical_type == 'insurance' :
#                     seq_id=obj_sequence.search(cr,uid,[('name','=','INSURANCE SERVICE')])
#                     if seq_id :
#                         seq_no = obj_sequence.next_by_id(cr, uid,seq_id[0], context=context)
#                         vals[''] =seq_no
#                         invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#                         return invoice_id                
#                     
#                     else :
#                         rais    def write(self, cr, uid, ids, vals, context=None):
                                                 
#                
#                 else:
#                     
#                     raise osv.except_osv(_('Sorry!'),_("Please choose Holiday business vertical"))     
#             
#             else :#

#                 
#                 invoice_id = super(account_invoice , self).create(cr, uid, vals, context)
#                 return invoice_id
#             
#             
#         
#         except Exception as error :
#             
#             raise osv.except_osv(_('Sorry!'),_("Invoice cannot be created !"))
#     
         
        


#     group_routesms_293holiday
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        user_obj=self.pool.get('res.users')
         
        res = super(account_invoice, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
         
         
        if view_type == 'form':
            vertical_id=user_obj.browse(cr,uid,uid).company_id.vertical.id
            if not vertical_id :
                raise osv.except_osv(_('Error!'),_("No vertical defined for this Company!"))            
             
            
            check_domain=res['arch']
            if 'in_invoice' in check_domain :

                doc = etree.XML(res['arch'])
                for node in doc.xpath("//field[@name='partner_id']"):
                    # do some computations....l
                    filter="['&',('supplier','=',True),('vertical','='," + str(vertical_id) + ")]"
                    node.set('domain', filter)
                res['arch'] = etree.tostring(doc)
                return res 
                
                
            else :
                
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//field[@name='partner_id']"):
                    # do some computations....l
                    filter="['|',('customer','=',True),('is_company','=',True),('vertical','='," + str(vertical_id) + ")]"
                    node.set('domain', filter)
                res['arch'] = etree.tostring(doc)
                return res            
        
        return res

#     def _compute_amount(self, cr, uid, ids, context=None) :
#         import ipdb;ipdb.set_trace()
#         self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
#         self.amount_tax = sum(line.amount for line in self.tax_line)
#         self.amount_total = self.amount_untaxed + self.amount_tax
 
# 
#     def onchange_journal_id(self,cr,uid,ids,journal_id=False):
#         import ipdb;ipdb.set_trace()
#         res=super(account_invoice,self).onchange_journal_id(cr,uid,ids,journal_id)
# #         if res['value']['company_id']==3:
# #             cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users',))
# #             group_id=cr.fetchall()
# #             if group_id:
# #                  
# #                 cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(group_id[0],uid))
#         if not ids :
#             mod_obj = self.pool.get('ir.model.data')
#             
#             form_id = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
#             
#             form_res = form_id and form_id[1] or False  
#             return {
#                 'name':_("Doctor Profile"),
#                 'view_mode': 'form',
#                 'res_id': ids[0],
#                 'view_type': 'form',
#                 'res_model': 'account.invoice',
#                 'type': 'ir.actions.act_window',
#                 'nodestroy':False,
#                 'view_id': (form_res,'View'),
#                 'views': [(form_res, 'form')],
#                 'context': {},
#                 'target':'current'
#                     }
#         else:
#                                 
#             return res
                 
               



class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"
    

    
    _columns={
               
              'passenger_name':fields.char('Passenger'),
              'passenger_name_air':fields.char('Passenger'),
              'ticket_number':fields.char('Ticket'),
              'flight_number':fields.char('Flight'),
              'travel_date':fields.datetime('Date'),
              'holiday_refernce_number':fields.char('Ref'),
              'from':fields.many2one('city.code','From'),
              'to':fields.many2one('city.code','To'),
              'pnr':fields.char('PNR Number'),
              'sub_total_amount':fields.float('Amount'),
              'sub_total_amount_air':fields.float('Amount'),
              'basic_amount':fields.float('Basic Amount'),
              'gross_amount':fields.float('Gross Amount'),
              'markup_air':fields.float('Markup'),
              'markup':fields.float('Markup'),
              
              
              }

#     def onchange_subtotal_amount_air(self,cr,uid,ids,amount,context):
#         
#         vals={}
#         if amount :
#             
#             vals.update({'sub_total_amount_air':amount,'price_unit':amount})
#             
#         return {'value':vals}

    
    
    def onchange_subtotal_amount(self,cr,uid,ids,amount,context):
        
        vals={}
        if amount :
            
            vals.update({'sub_total_amount':amount,'price_unit':amount})
            
        return {'value':vals}
    

#     def fields_view_get(self, cr, uid, view_id=None, view_type='tree', context=None, toolbar=False, submenu=False):
#         if context is None:
#             context = {}

#         res = super(account_invoice_line,self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
#         if context.get('type', False):
#             doc = etree.XML(res['arch'])
#             for node in doc.xpath("//field[@name='product_id']"):
#                 if context['type'] in ('in_invoice', 'in_refund'):
#                     node.set('domain', "[('purchase_ok', '=', True)]")
#                 else:
#                     node.set('domain', "[('sale_ok', '=', True)]")
#             res['arch'] = etree.tostring(doc)
#         return res

    
class account_voucher(osv.osv):
    _inherit='account.voucher'

    def current_user_id(self, cr, uid, context=None):
        '''Return current login user  '''
        
        
        return uid
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context is None:
            context = {}
        
        emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
        if emp_id :
            if len(emp_id) >1 :
                raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
            
            return emp_id[0]
        
        else :
            return 0 


    def account_onchange_user(self, cr, uid, ids, user_id, context=None):
        ''' Inherited function to Get employee id if User manually change the Saleperson'''
        
        vals={}
        
        
        if user_id:
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0]})
                
                return {'value':vals}
        else:
            
            return {'value':vals}
            
            
           
    
    
    _columns = {

        'contact_id': fields.many2one('res.partner', 'Contact Person', help="This is contact person related to customer"),
        'user_id':fields.many2one('res.users','Saleperson'),
        'employee_id':fields.many2one('hr.employee','Employee User'),
        'credit_type':fields.char('Credit Type'),
        'remark':fields.text('Remark'), 
        'voucher_seq_number':fields.char('Voucher Number'),       
    }
    
    _defaults={
                 
               'user_id':current_user_id,
               'employee_id':default_emp_id,
               }    
    
    
    def create(self, cr, uid, vals, context=None):
        ''' Overide create method to for sequencing'''
        
        obj_sequence=self.pool.get('ir.sequence')
        #obj_sequence.search(cr,uid,[('name','=',name)])
        #seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
        if vals.get('voucher_seq_number', False) == False:
            vals['voucher_seq_number'] = self.pool.get('ir.sequence').get(cr, uid, 'account.voucher') or '/'

            
        voucher = super(account_voucher, self).create(cr, uid, vals, context)
        return voucher             

#     def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None):
#         
#         res=super(account_voucher,self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None)
#         
# #         for i in res['value']['line_cr_ids'] : 
# #             move_id=self.pool.get('account.move.line').browse(cr,uid,i['move_line_id']).move_id.id
# #             if move_id :
# #                 
# #                 invoice_id=self.pool.get('account.invoice').search(cr,uid,[('move_id','=',move_id)])
# #                 if invoice_id :
# #                     
# #                     amount=self.pool.get('account.invoice').browse(cr,uid,invoice_id[0]).amount_total
# #                     i['invoice_amount']=amount
# #         
#         

#         res=a={'value': {'line_cr_ids': [{'invoice_amount':900,'currency_id': 21, 'amount': 110.0, 'date_due': '2015-07-12', 'name': u'SAJ/2015/0002ffff', 'date_original': '2015-04-12', 'move_line_id': 4, 'amount_unreconciled':1453111115000.0, 'type': 'cr', 'amount_original': 1000.0, 'account_id': 145}], 'account_id': 270, 'paid_amount_in_company_currency': 0.0, 'line_dr_ids': [], 'writeoff_amount': 0.0, 'currency_help_label': u'At the operation date, the exchange rate was\n1.00 \u20b9 = 1.00 \u20b9', 'currency_id': 21, 'pre_line': 1, 'payment_rate': 1.0, 'payment_rate_currency_id': 21}}        
#         return res



    
class account_voucher_line(osv.osv):
    _inherit='account.voucher.line'
    
    _columns = {
    
        'invoice_amount':fields.float('Invoice Amount'),        
    }
    


class account_journal(osv.osv):
    _inherit='account.journal'


    def create(self, cr, uid, vals, context=None):
        
        ''' Overiden method concanate journal name and company naming convention'''
        user_obj=self.pool.get('res.users')
        company_obj=self.pool.get('res.company')
        journal_id=super(account_journal, self).create(cr, uid, vals, context)
        updated_name=vals['name'] + ' '+  company_obj.browse(cr,uid,vals['company_id']).name_convention 
        self.write(cr,uid,journal_id,{'name':updated_name})    
        return journal_id
    
    
#################################API''s############################    
    
#     def search_partner_api(self,cr,uid,partner_id,context):
#         #check weather partner exist in Odoo
#         partner_obj=self.pool.get('res.partner')
#         # Format:
#         #    val=[{'partner_id':''}]
#         partner_ids=partner_obj.search(cr,uid,[('cust_id','=',partner_id['partner_id'])])
#         return partner_ids
#     
#     def create_partner_api(self,cr,uid,partner_vals,context):
#         pass
#     
#     
#     
#     def search_product_api(self,cr,uid,product_name,context):
#         
#         product_obj=self.pool.get('product.product')        
#         product_name_val=product_obj.search(cr,uid,[('','=',product_name)])
#         return product_name_val
#     
#     def create_product_api(self,cr,uid,product_name,context):
#         pass
#     
#     
#     def invoice_api(self,cr,uid,vals,context):

#         partner_obj=self.pool.get('res.partner')
#         product_obj=self.pool.get('product.product')
#         
#         # Format:
#             #val=[{'partner_id':'','p[roduct_id':'','company_id':'','created_date':''}]
#         
#         for val in vals :
#             res={}
#             partner_id=partner_obj.search(cr,uid,[('cust_id','=',val['partner_id'])])
#             if partner_id:
#                 #append into dict
#                 res.update({'partner_id':partner_id[0]})
#             else:
#                 # create new partner in Odoo

#################################API''s ENDS############################  


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
