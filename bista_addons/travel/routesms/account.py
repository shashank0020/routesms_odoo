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
from calendar import monthrange
from dateutil import relativedelta
from num2words import num2words


# class account_move_line(osv.osv):
#     _inherit = "account.move.line"
#     
#     def onchange_partner_id(self, cr, uid, ids, move_id, partner_id, account_id=None, debit=0, credit=0, date=False, journal=False, context=None):
#         ''' overided function to put doamin'''
#         
#         
#         res = super(account_move_line, self).onchange_partner_id(cr, uid, ids, move_id, partner_id, account_id=None, debit=0, credit=0, date=False, journal=False, context=None)
#         res['value'].update({'domain':{'partner_id':[('supplier','=',True)]}})
#         #import ipdb;ipdb.set_trace()
#         return res
#         
#         
#             
#     
#     def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#         user_obj=self.pool.get('res.users')
#         
#         
#          
#         res = super(account_move_line, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
# 
# 
#          
#         try : 
#             
#             
#             if view_type == 'form':
#                 
#                 vertical_id=user_obj.browse(cr,uid,uid).company_id.vertical.id
#                 if not vertical_id :
#                     raise osv.except_osv(_('Error!'),_("No vertical defined for this Company!"))            
#                  
#                 
#                 check_domain=res['arch']
#                 if 'in_invoice' in check_domain :
#     
#                     doc = etree.XML(res['arch'])
#                     for node in doc.xpath("//field[@name='partner_id']"):
#                         # do some computations....l
#                         filter="['&',('supplier','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
#                         node.set('domain', filter)
#                     res['arch'] = etree.tostring(doc)
#                     return res 
#                     
#                     
#                 else :
#                     
#                     #if 293holiday comapny domain doesn not conatct contatc id domain
#                     
#                     if user_obj.browse(cr,uid,uid).company_id.id == 3 :
#                         doc = etree.XML(res['arch'])
#                         for node in doc.xpath("//field[@name='partner_id']"):
#                             # do some computations....l
#                             filter="['&',('customer','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
#                             node.set('domain', filter)
#                         res['arch'] = etree.tostring(doc)
#                         return res  
#                     
#                     else : 
#                                            
#                         #for rest of the companies
#                         
#                         doc = etree.XML(res['arch'])
#                         for node in doc.xpath("//field[@name='partner_id']"):
#                             # do some computations....l
#                             filter="['&',('customer','=',True),('is_company','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
#                             node.set('domain', filter)
#                         res['arch'] = etree.tostring(doc)
#                         return res            
#             
#             return res
#         
#         except Exception as E : 
#             
#             raise osv.except_osv(_('Technical Error!'), _("Contact Odoo Team"))    
class account_bank_statement_line(osv.osv):
    _inherit = "account.bank.statement.line"
    
  
    _columns={
              'name': fields.text('Communication', required=True),
              
              }

class account_move(osv.osv):
    _inherit = "account.move"
    
    def _credit_info(self,cr, uid, ids, name, args, context=None):
        ''' store credit info as per journal '''
        
        res={}
        
        
        for move in self.browse(cr, uid, ids) :
            val =[{'partner':line.partner_id.name or '/','credit_amount':str(line.credit)} for line in move.line_id if move.journal_id.default_credit_account_id.id == line.account_id.id and line.credit!=0.00]
            result=','.join([x['partner'] + ':' + x['credit_amount'] for x in  val])
            #import ipdb;ipdb;ipdb.set_trace()
            res[move.id]=result
            
        print '--------ASSIGNED credit---------'    
        return res
    
    def _debit_info(self,cr, uid, ids, name, args, context=None):
        ''' store debit info as per journal '''
        
        res={}
        
        
        for move in self.browse(cr, uid, ids) :
            val =[{'partner':line.partner_id.name or '/','debit_amount':str(line.debit)} for line in move.line_id if move.journal_id.default_debit_account_id.id == line.account_id.id and line.debit!=0.00]
            result=','.join([x['partner'] + ':' + x['debit_amount'] for x in  val])
            #import ipdb;ipdb;ipdb.set_trace()
            
            res[move.id]=result
            
        print '--------ASSIGNED debit---------'    
        return res    
    
        
    _columns={
              'credit_info':fields.function(_credit_info,type='char',store=True,string='Credit'),
              'debit_info':fields.function(_debit_info,type='char',store=True,string='Dedit')
              
              
              }              

class account_move_line(osv.osv):
    _inherit = "account.move.line"
    
    def onchange_partner_id(self, cr, uid, ids, move_id, partner_id, account_id=None, debit=0, credit=0, date=False, journal=False, context=None):
        ''' Inhertited for auto partner ledger '''
        partner_obj=self.pool.get('res.partner')
        res=super(account_move_line,self).onchange_partner_id(cr, uid, ids, move_id, partner_id, account_id=None, debit=0, credit=0, date=False, journal=False, context=None)
        
        
        if partner_id :
            partner_val=partner_obj.browse(cr,uid,partner_id) 
            if partner_val.customer ==True and partner_val.supplier== False : 
                account_val=partner_val.property_account_receivable.id
                res['value'].update({'partner_type_flag':False,'partner_type':False})
            elif partner_val.customer ==False and partner_val.supplier== True : 
                account_val=partner_val.property_account_payable.id
                res['value'].update({'partner_type_flag':False,'partner_type':False})
            elif partner_val.customer ==True and partner_val.supplier== True : 
                account_val=account_id
                res['value']['partner_type_flag']=True                
            
            elif partner_val.customer ==False and partner_val.supplier== False : 
                account_val=account_id
                res['value'].update({'partner_type_flag':False,'partner_type':False})
                
            else :
                res['value'].update({'partner_type_flag':False,'partner_type':False})
                
            
            res['value']['account_id']=account_val
        
        return res
            

    def onchange_partner_type(self,cr,uid,ids,partner_type,partner_id,context):
        ''' Select account type based on partner type selection'''
        partner_obj=self.pool.get('res.partner')
        vals={}
        
        if partner_type :
            
            partner_val=partner_obj.browse(cr,uid,partner_id)
            if partner_type=='customer': 
                
                vals.update({'account_id':partner_val.property_account_receivable.id})
                
            elif partner_type=='supplier':
                 
                vals.update({'account_id':partner_val.property_account_payable.id})
                
            else : 

                raise osv.except_osv(_('Invalid Selection!'), _("Kindly select Partner Type"))
            
        
        return {'value':vals}
    

            
    _columns={
              
              'partner_type_flag':fields.boolean('Partner Type Flag'),
              'partner_type': fields.selection([('customer','Customer'), ('supplier','Supplier')], 'Partner Type'),
              
              }
    
    
    _defaults={
               'partner_type_flag':False
               }
    


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
    


    def number_to_words(self,n):
        words = ''
      
      
        number_spit=str(round(n,2)).split('.')
        n=int(number_spit[0])
        
        if number_spit[1] == '0' or number_spit[1]=='00' : 
            
            decimal_no='only'
        else :
            
            num=int(number_spit[1])
            
            decimal_no= 'and' + ' ' +str(num2words(num).replace('-', ' ')) + ' ' +'only'
        
        units = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
        tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        
        for group in ['', 'hundred', 'thousand', 'lakh', 'crore']:
        
          if group in ['', 'thousand', 'lakh']:
            n, digits = n // 100, n % 100
          elif group == 'hundred':
            n, digits = n // 10, n % 10
          else:
            digits = n
        
          if digits in range (1, 20):
            words = units [digits] + ' ' + group + ' ' + words
          elif digits in range (20, 100):
            ten_digit, unit_digit = digits // 10, digits % 10
            words = tens [ten_digit] + ' ' + units [unit_digit] + ' ' + group + ' ' + words
          elif digits >= 100:
            words = number_to_words (digits) + ' crore ' + words
        vals=words.capitalize() + decimal_no 
        
        
        return vals


    def _amount_to_word_updated(self,cr, uid, ids, name, args, context=None):
        ''' store updated amount in char format '''
        res={}
        
        for invoice in self.browse(cr, uid, ids) :
            updated_val =''
            total_amount=invoice.amount_total
            if total_amount :
                
                amount_in_word=self.number_to_words(total_amount)
                res[invoice.id]=amount_in_word

            else :
                res[invoice.id]=''
        print '--------------SSUCCESS-------'
        return res  
   
    def calculate_due_date(self,cr,uid,ids,context):
        '''calculate due date according to payment term (FOR 29T only) '''
        #import ipdb;ipdb.set_trace()
        try: 
            if not context :
                context={}
            if ids : 
                inv_vals=self.browse(cr,uid,ids[0])
                if inv_vals.company_id.id != 3 :  
                    return True
                
                
                if inv_vals.date_invoice and inv_vals.payment_term :
                    #format ['2015', '08', '03'] yyyy/mm/dd
                    date_split=inv_vals.date_invoice.split('-')
                    
                    if  inv_vals.payment_term.name == '7 Days' :
                        if  date_split[2] <='07' and date_split[2] >='01' : 
                             
                             
                            due_date=date_split[1] + '-08-' + date_split[0]
                        
                        elif date_split[2] <='14' and date_split[2] >='07' : 
                            
                            due_date=date_split[1] + '-15-' + date_split[0]
    
                        elif date_split[2] <='21' and date_split[2] >='14' : 
                            
                            due_date=date_split[1] + '-22-' + date_split[0]
    
                        elif date_split[2] <='28' and date_split[2] >='21' : 
                            
                            due_date=date_split[1] + '-29-' + date_split[0]
                            
                        else :
                            
                            next_date=datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])) + relativedelta.relativedelta(months=1)
                            formated_date=next_date.strftime('%m/%d/%Y').split('/')
                            due_date=formated_date[0] + '-01-' + formated_date[2]
                        
                        cr.execute(''' update account_invoice set date_due=%s where id=%s ''',(due_date,ids[0]))
                         
                        
                    elif inv_vals.payment_term.name == '15 Days' :
                        
                        if date_split[2] <='15' and date_split[2] >='01' : 
                            due_date=date_split[1] + '-16-' + date_split[0]
                            
                        elif date_split[2] <='30' and date_split[2] >='15' :
                             
                            no_of_days=monthrange(int(date_split[0]), int(date_split[1]))
                            if no_of_days[1] == 31 :
                                due_date=date_split[1] + '-31-' + date_split[0]
                            
                                
                            else : 
                                next_date=datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])) + relativedelta.relativedelta(months=1)
                                formated_date=next_date.strftime('%m/%d/%Y').split('/')
                                due_date=formated_date[0] + '-01-' + formated_date[2]                            
    
                        else :
    
                        
                            next_date=datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])) + relativedelta.relativedelta(months=1)
                            formated_date=next_date.strftime('%m/%d/%Y').split('/')
                            due_date=formated_date[0] + '-01-' + formated_date[2]
    
                        
                        cr.execute(''' update account_invoice set date_due=%s where id=%s ''',(due_date,ids[0]))
                        
                           
                    elif inv_vals.payment_term.name == '30 Net Days' :
                         
                        no_of_days=monthrange(int(date_split[0]), int(date_split[1]))
                        if no_of_days[1] in [28,29] :
                            due_date='03-01-' + date_split[2]
                    
                        else : 
                            next_date=datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])) + relativedelta.relativedelta(months=1)
                            formated_date=next_date.strftime('%m/%d/%Y').split('/')
                            due_date=formated_date[0] + '-01-' + formated_date[2]
                        cr.execute(''' update account_invoice set date_due=%s where id=%s ''',(due_date,ids[0]))
                                     
                    else:
                        return True
        except Exception as E : 
            return True
        
        return True
    
    def create(self, cr, uid, vals, context=None):
        if context==None : 
            context={}        
        if vals.get('responsible') : 
        
            context['responsible']=vals['responsible']
            vals['employee_id']=self.default_emp_id(cr, uid, context)
        result=super(account_invoice , self).create(cr, uid, vals, context)
        self.calculate_due_date(cr,uid,[result],context)# calculate due date for 29T only
        return result
    
    def write(self, cr, uid, ids, vals, context=None):
        
        if context==None : 
            context={}
            
        if vals.get('responsible') : 
        
            context['responsible']=vals['responsible']
            vals['employee_id']=self.default_emp_id(cr, uid, context)
        result=super(account_invoice , self).write(cr, uid,ids, vals, context)
        self.calculate_due_date(cr,uid,ids,context)# calculate due date for 29T only
        return result    
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context.get('responsible') :
            
        
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',context.get('responsible'))])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                
                return emp_id[0]
            
            else :
                return 0
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
            updated_val =''
            total_amount=invoice.amount_total
            if total_amount :
                
                numwords=num2words(int(total_amount)).split('-')

                for i in numwords:
                    b=i.split(' ')
                    for j in b:
        

                        updated_val+=j.capitalize() +' ' 

                
                #res[invoice.id]=' '.join([x.capitalize() for x in numwords])
                res[invoice.id]=updated_val

            else :
                res[invoice.id]=''
        return res    

    def _period_to_words(self,cr, uid, ids, name, args, context=None):
        ''' store amount in char format '''
        res={}
        
        for invoice in self.browse(cr, uid, ids) :

                
            period=invoice.period_id.name
            if period : 
                #import ipdb;ipdb.set_trace()
                split=period.split('/')
                date=[int(x) for x in split]
                res[invoice.id]=datetime.date(date[1],date[0],1).strftime('%B') +  ' ' + str(date[1])
                print 'DONE'
            else :
                res[invoice.id]=''
        return res        
       
    def responsible_user_id(self, cr, uid, context=None):
        '''Return current login user  '''
        
        return uid    

    def _pnr_no(self,cr, uid, ids, name, args, context=None):
       
        ''' store pnr no '''
        invoice_line_obj=self.pool.get('account.invoice.line')
        pnr_nos=[]
        res={}
        
        count=0
        for invoice in self.browse(cr, uid, ids) :
            #search inv lines data
            count+=1
            print count    
            inv_line_ids=invoice_line_obj.search(cr,uid,[('invoice_id','=',invoice.id)])
            for inv_line_id in inv_line_ids : 
                inv_line_val=invoice_line_obj.browse(cr,uid,inv_line_id)
                if inv_line_val.pnr : 
                    pnr_nos.append(inv_line_val.pnr)
        
        if pnr_nos : 
            
            #res[invoice.id]=','.join(pnr_nos)

            res[invoice.id]=pnr_nos[0]
            print 'PNR DONE'

        else :
            
            res[invoice.id]=''
        
        return res     
           
           
    def _ticket_no(self,cr, uid, ids, name, args, context=None):
        ''' store ticket no '''
        invoice_line_obj=self.pool.get('account.invoice.line')
        ticket_nos=[]
        res={}
        count=0
        
        
        for invoice in self.browse(cr, uid, ids) :
            #search inv lines data
            count+=1
            print count                 
            inv_line_ids=invoice_line_obj.search(cr,uid,[('invoice_id','=',invoice.id)])
            for inv_line_id in inv_line_ids : 
                inv_line_val=invoice_line_obj.browse(cr,uid,inv_line_id)
                if inv_line_val.ticket_number : 
                    ticket_nos.append(inv_line_val.ticket_number)
        
        if ticket_nos : 
            
#             res[invoice.id]=','.join(ticket_nos)
            res[invoice.id]=ticket_nos[0]
            print 'TICKET DONE'

        else :
            
            res[invoice.id]=''
        
        return res           


    def _passenger_names(self,cr, uid, ids, name, args, context=None):
        ''' store passenger name '''
        invoice_line_obj=self.pool.get('account.invoice.line')
        passenger_names=[]
        res={}
        count=0
        
        
        
        for invoice in self.browse(cr, uid, ids) :
            #search inv lines data
            count+=1
            print count                 
            inv_line_ids=invoice_line_obj.search(cr,uid,[('invoice_id','=',invoice.id)])
            for inv_line_id in inv_line_ids : 
                inv_line_val=invoice_line_obj.browse(cr,uid,inv_line_id)
                if inv_line_val.passenger_name_air and inv_line_val.passenger_name :
                    passenger_names.append(inv_line_val.passenger_name_air)
                    passenger_names.append(inv_line_val.passenger_name)
                    
                if inv_line_val.passenger_name_air : 
                    passenger_names.append(inv_line_val.passenger_name_air)
                    
                elif inv_line_val.passenger_name : 
                    passenger_names.append(inv_line_val.passenger_name)
                    
                else :
                    pass
                    
        if passenger_names : 
            print 'PASSENGER DONE'
            #res[invoice.id]=','.join(passenger_names)
            res[invoice.id]=passenger_names[0]

        else :
            
            res[invoice.id]=''
        
        return res   


    _columns = {

        'contact_id': fields.many2one('res.partner', 'Contact Person', help="This is contact person related to customer"),
        'employee_id':fields.many2one('hr.employee','Employee User'),
        'credit_type':fields.char('Credit Type'),
        'remark':fields.text('Remark'),
        'amount_to_word':fields.function(_amount_to_word,string='Amount In Words', type='char',store=True),
        'amount_to_word_updated':fields.function(_amount_to_word_updated,string='Amount In Words Updated', type='char',store=True),
        'period_to_words':fields.function(_period_to_words,string='Period In Words', type='char',store=True),
        'payment_term' :fields.many2one('account.payment.term', string='Payment Terms',required=True,
        readonly=True, states={'draft': [('readonly', False)]},
        help="If you use payment terms, the due date will be computed automatically at the generation "
             "of accounting entries. If you keep the payment term and the due date empty, it means direct payment. "
             "The payment term may compute several due dates, for example 50% now, 50% in one month."),
                
        'partner_bank_id':fields.many2one('res.partner.bank', string='Bank Account',
        help='Bank Account Number to which the invoice will be paid. A Company bank account if this is a Customer Invoice or Supplier Refund, otherwise a Partner bank account number.',
        readonly=True,required=False, states={'draft': [('readonly', False)]}),
        'responsible':fields.many2one('res.users','Responsible'),  
        'user_id_employee':fields.many2one('hr.employee','Salesperson Employee User'), 
        'pnr_no':fields.function(_pnr_no,string='PNR', type='char',store=True),
        'ticket_no':fields.function(_ticket_no,string='Ticket No', type='char',store=True),
        'passenger_names':fields.function(_passenger_names,string='Passenger', type='char',store=True),
        'partner_country':fields.char('Country'),
        'partner_account_type':fields.char('Account Type'),
        'use_contact_person_address':fields.boolean('Use contact person address'),
                      
    }
    
    _defaults={
               
               'employee_id':default_emp_id,
               'responsible':responsible_user_id,
               'use_contact_person_address':False,
               
               
               }    


    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        ''' Make customer invoice from supplier invoice for 293 holidays'''
        res= super(account_invoice, self).copy(cr, uid, id, default, context=context)
        #import ipdb;ipdb.set_trace()
        try :
            supplier_inv_val=self.browse(cr,uid,id)
            if self.pool.get('res.users').browse(cr,uid,uid).company_id.id == 3 and context.get('type') == 'in_invoice' and supplier_inv_val.state in ['open','paid']:
                
                if supplier_inv_val.partner_id.customer == True :
                
                    cr.execute(''' update account_invoice set comment='Supplier Duplicate Invoice' ,type='out_invoice' ,origin=%s where id=%s ''',(supplier_inv_val.number,res,))
                
                else :
                    
                    raise osv.except_osv(_('Error!'), _('Partner is not a Customer.'))
        except Exception as E :
            
            raise osv.except_osv(_('ERROR'),
                                _('Invoice Duplication Failed!\nSet Partner as a Customer Or Contact Odoo Team'))        
            
        return res
        

    def check_bank_currency(self,cr,uid,ids) : 
        '''Check Bank account & Invoice curency '''
        
        invoice_val=self.browse(cr,uid,ids[0])
        
        if invoice_val.partner_bank_id.currency_id.id == invoice_val.currency_id.id :
            #check bank curency and invoice curr 
            return True
        elif invoice_val.partner_bank_id.currency_id.id ==False and invoice_val.currency_id.id == invoice_val.company_id.currency_id.id :
            #check weather bank curency is fAlse in case of Base currency 
            return True
        else :
            
            return False
           
    

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
            if self.browse(cr,uid,ids[0]).partner_bank_id : 
                    
                check_bank_currency=self.check_bank_currency(cr,uid,ids)
                
                    
                if not check_bank_currency : 
                    raise osv.except_osv(_('Validation Error!'),_("Bank Account Currency & Invoice Currency Mismatch!"))
            
              
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
        
        if self.pool.get('res.users').browse(cr,uid,uid).company_id.currency_id.id == vals['currency_id'] :
            return True
         
        currency_val=curreny_rate_line.search(cr,uid,[('currency_id','=',vals['currency_id'])])
        if currency_val :
                
            
            for currency_ids in currency_val :
                rate_date=curreny_rate_line.browse(cr,uid,currency_ids).name
                
                result.append(rate_date.split(' ')[0])
            
            if vals['date_invoice'] in result :
                return True

                
            else :
                #raise osv.except_osv(_('Warning!'),_("Invoice cannot be created,Please set currency rate"))
                raise osv.except_osv(_('Validation Error'), _("Invoice cannot be created,Please set currency rate for %s ")%(vals['date_invoice']))
                
        else:
            raise osv.except_osv(_('Error!'),_("Invoice cannot be created. No currency found!"))
  
                        
#     
# #     
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
#                 rate_date        raise osv.except_osv(_('Sorry!'),_("No Sequence found ! Please create one"))
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


         
        try : 
            
         
            if view_type == 'form':
                vertical_id=user_obj.browse(cr,uid,uid).company_id.vertical.id
                if not vertical_id :
                    raise osv.except_osv(_('Error!'),_("No vertical defined for this Company!"))            
                 
                
                check_domain=res['arch']
                if 'in_invoice' in check_domain :
    
                    doc = etree.XML(res['arch'])
                    for node in doc.xpath("//field[@name='partner_id']"):
                        # do some computations....l
                        filter="['&',('supplier','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
                        node.set('domain', filter)
                    res['arch'] = etree.tostring(doc)
                    return res 
                    
                    
                else :
                    
                    #if 293holiday comapny domain doesn not conatct contatc id domain
                    
                    if user_obj.browse(cr,uid,uid).company_id.id == 3 :
                        doc = etree.XML(res['arch'])
                        for node in doc.xpath("//field[@name='partner_id']"):
                            # do some computations....l
                            filter="['&',('customer','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
                            node.set('domain', filter)
                        res['arch'] = etree.tostring(doc)
                        return res  
                    
                    else : 
                                           
                        #for rest of the companies
                        
                        doc = etree.XML(res['arch'])
                        for node in doc.xpath("//field[@name='partner_id']"):
                            # do some computations....l
                            filter="['&',('customer','=',True),('is_company','=',True),('vertical','='," + str(vertical_id) + "),('state','=','confirm')]"
                            node.set('domain', filter)
                        res['arch'] = etree.tostring(doc)
                        return res            
            
            return res
        
        except Exception as E : 
            
            raise osv.except_osv(_('Technical Error!'), _("Contact Odoo Team"))

    def onchange_journal_id(self,cr,uid,ids,journal_id,partner_id,context):
        '''VAT Validation for RSLUK '''
        partner_obj=self.pool.get('res.partner')
        country_li=[]
        
        result=super(account_invoice,self).onchange_journal_id(cr,uid,ids,journal_id,context)
        
        if journal_id : 
            if journal_id==210 : 
                if not partner_id : 
                    raise osv.except_osv(_('Validaton Error!'), _("Refresh Page & Select Partner Partner Before Jounral"))
                     
                partner=partner_obj.browse(cr,uid,partner_id)
                if not partner.vat : 
                    raise osv.except_osv(_('Warning!'), _("VAT number not Found"))
                
        return result


    def onchange_partner_id(self, cr,uid,ids,type, partner_id, date_invoice=False,
                payment_term=False, partner_bank_id=False, company_id=False,context=None):
        
        
        result=super(account_invoice,self).onchange_partner_id(cr,uid,ids,type, partner_id, date_invoice=False,payment_term=False, partner_bank_id=False, company_id=False,context=None)
        
        if partner_id :
           
            if self.pool.get('res.users').browse(cr,uid,uid).company_id.id ==3 : 
                return result
         #  
            partner=self.pool.get('res.partner').browse(cr,uid,partner_id)
            business_manager=partner.user_id
            if business_manager : 
                result['value']['user_id']=business_manager.id
                
#                 emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',business_manager.id)])
#                 if emp_id :
#                     if len(emp_id) >1 :
#                         raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))                
#                     result['value']['user_id_employee']=emp_id[0]
                
            else :
                
                raise osv.except_osv(_('Validation Error!'), _("No saleperson defined For Partner! \nContact Accounts Team"))
            
            if partner.country_id :
                result['value']['partner_country']=partner.country_id.name
            else : 
                 result['value']['partner_country']="Country Not Assigned"

            if partner.prepaid : 
                account_type='prepaid'
                
            elif partner.postpaid : 
                account_type='postpaid'
                
            else : 
                account_type=''            

            result['value']['partner_account_type']=account_type

                                
        return result
                        
        
            

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
    


#     def _tax_amount(self,cr, uid, ids, name, args, context=None):
#         ''' store tax amount per line '''
#         res={}
#         total_amount=[]
#         child_tax_list=[]
#         
# #         import ipdb;ipdb.set_trace()
#         for invoice_line in self.browse(cr, uid, ids) :
#             
#             cr.execute('select tax_id from account_invoice_line_tax where invoice_line_id=%s',(invoice_line.id,))
#             taxes_on_line = cr.fetchall()
#             
#             if taxes_on_line :
#                 print 'INTO    TAXES----'
# 
#                     
#                 for tax_id in taxes_on_line :
#                     #get parent tax amount
#                     cr.execute('select amount from account_tax where id=%s',(tax_id[0],))
#                     try :
#                         
#                         parent_tax_amount = cr.fetchall()[0][0]
#                     except Exception as E :
#                         
#                         parent_tax_amount=0.00
#                         
#                     # get child taxes
#                     #import ipdb;ipdb.set_trace()
#                     cr.execute('select id from account_tax where parent_id=%s',(tax_id[0],))
#                     child_taxes = cr.fetchall()
#                     if child_taxes :
#                         
#                         for child_tax_id in child_taxes :
# 
#                             cr.execute('select amount from account_tax where id=%s',(child_tax_id[0],))
#                             try :
#                                 
#                                 child_tax_amount = cr.fetchall()[0][0]
#                             except Exception as E :
#                                 
#                                 child_tax_amount=0.00                            
#                             
#                             child_tax_list.append(child_tax_amount)
#                             
#                         total_amount.append(parent_tax_amount * invoice_line.price_subtotal + parent_tax_amount * invoice_line.price_subtotal * sum(child_tax_list))
#                         
#                     else :
#                         # if not tax child exist
#                         
#                         total_amount.append(parent_tax_amount * invoice_line.price_subtotal)
#                         
#                     
#                     #total_amount.append(tax_amount)
#                     
#                 res[invoice_line.id]=sum(total_amount)
#        
#         return res
                    
    def _tax_amount(self,cr, uid, ids, name, args, context=None):
        ''' store tax amount per line '''
        res={}
        total_amount=[]
        child_tax_list=[]
        
#         import ipdb;ipdb.set_trace()
        for invoice_line in self.browse(cr, uid, ids) :
            
            cr.execute('select tax_id from account_invoice_line_tax where invoice_line_id=%s',(invoice_line.id,))
            taxes_on_line = cr.fetchall()
            
            if taxes_on_line :
                print 'INTO    TAXES----'

                    
                for tax_id in taxes_on_line :
                    #get parent tax amount
                    cr.execute('select amount from account_tax where id=%s',(tax_id[0],))
                    try :
                        
                        parent_tax_amount = cr.fetchall()[0][0]
                    except Exception as E :
                        
                        parent_tax_amount=0.00

                        
                    total_amount.append(parent_tax_amount)
                        
                    
                    #total_amount.append(tax_amount)
                    
                res[invoice_line.id]=sum(total_amount) * invoice_line.price_subtotal
       
        return res                    
                        
                    
            
        
#         for invoice in self.browse(cr, uid, ids) :
#             updated_val =''
#             total_amount=invoice.amount_total
#             if total_amount :
#                 
#                 numwords=num2words(int(total_amount)).split('-')
# 
#                 for i in numwords:
#                     b=i.split(' ')
#                     for j in b:
#         
# 
#                         updated_val+=j.capitalize() +' ' 
# 
#                 
#                 #res[invoice.id]=' '.join([x.capitalize() for x in numwords])
#                 res[invoice.id]=updated_val
#                 if ids[0]==1387 :
#                     
#                     
#                 print 'included'
#             else :
#                 res[invoice.id]=''
        return res        

    
    _columns={
               
              'passenger_name':fields.char('Passenger'),
              'passenger_name_air':fields.char('Passenger'),
              'ticket_number':fields.char('Ticket'),
              'flight_number':fields.char('Flight'),
              'travel_date':fields.date('Date'),
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
              'tax_amount':fields.function(_tax_amount,string='Tax Amount', type='float',store=True,digits=(16,5)),

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


#     def create(self, cr, uid, vals, context=None):
#         
# 
#         result=super(account_voucher , self).create(cr, uid, vals, context)
#         return result
    
    

    def button_proforma_voucher(self, cr, uid, ids, context=None):
        
        invoice=self.pool.get('account.invoice').browse(cr,uid,context.get('invoice_id'))
        vals={'currency_id': invoice.currency_id.id, 'date_invoice': self.browse(cr,uid,ids[0]).date}
        status=self.pool.get('account.invoice').currency_set(cr, uid, vals, context=None)
        if status : 
            return super(account_voucher,self).button_proforma_voucher(cr, uid, ids, context)
        
        raise osv.except_osv(_('Warning!'),_("Invoice cannot be created,Please set currency rate"))        

    def _get_date(self, cr, uid,context):
        '''Return Open Invoice date '''
        
        return self.pool.get('account.invoice').browse(cr,uid,context.get('invoice_id')).date_invoice
        
    def _get_period(self, cr, uid, context=None):
        if context is None: context = {}
        
        if context.get('period_id', False):
            return context.get('period_id')
        periods = self.pool.get('account.period').find(cr, uid, context=context)
        return periods and periods[0] or False
    
    
    def _get_journal(self, cr, uid, context=None):
        
        if context is None: context = {}
        invoice_pool = self.pool.get('account.invoice')
        journal_pool = self.pool.get('account.journal')
        
        if context.get('invoice_id', False):
            invoice = invoice_pool.browse(cr, uid, context['invoice_id'], context=context)
            if invoice.partner_bank_id : 
                if invoice.partner_bank_id.journal_id: 
                    return invoice.partner_bank_id.journal_id.id
                
            journal_id = journal_pool.search(cr, uid, [
                ('currency', '=', invoice.currency_id.id), ('company_id', '=', invoice.company_id.id)
            ], limit=1, context=context)
            return journal_id and journal_id[0] or False
        if context.get('journal_id', False):
            return context.get('journal_id')
        if not context.get('journal_id', False) and context.get('search_default_journal_id', False):
            return context.get('search_default_journal_id')

        ttype = context.get('type', 'bank')
        if ttype in ('payment', 'receipt'):
            ttype = 'bank'
        res = self._make_journal_search(cr, uid, ttype, context=context)
        return res and res[0] or False



    def current_user_id(self, cr, uid, context=None):
        '''Return current login user  '''
        
        
        return uid

 
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context.get('responsible') :
            
        
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',context.get('responsible'))])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                
                return emp_id[0]
            
            else :
                return 0
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
            
            
    def responsible_user_id(self, cr, uid, context=None):
        '''Return current login user  '''
      
        
        return uid           


    def payment_option_onchange(self, cr, uid, ids, option, context=None):
        ''' Payment Method Option'''
        vals={}
        if option :
            if option == 'online' : 
                vals.update({'online_transfer_flag':True,'cheque_number_flag':False})
            else :
                vals.update({'cheque_number_flag':True,'online_transfer_flag':False})
                
        return {'value':vals}
     
        
    
    _columns = {

        'contact_id': fields.many2one('res.partner', 'Contact Person', help="This is contact person related to customer"),
        'user_id':fields.many2one('res.users','Saleperson'),
        'employee_id':fields.many2one('hr.employee','Employee User'),
        'credit_type':fields.char('Credit Type'),
        'remark':fields.text('Remark'), 
        'voucher_seq_number':fields.char('Voucher Number'),  
        'responsible':fields.many2one('res.users','Responsible'),
        'remove_line':fields.boolean('Remove Line'),
        'payment_method': fields.selection([('online','Online Transfer'), ('cheque','Cheque')], 'Payment Option'),
        'online_transfer':fields.char('Online Transfer'),
        'online_transfer_flag':fields.boolean('Online Transfer Flag'),
        'cheque_number':fields.char('Cheque Number',size=6),
        'cheque_number_flag':fields.boolean('Cheque Number Flag'),
        'reconcile_uncheck':fields.boolean('Remove Reconcile'),

    }
    
    _defaults={
                 
               #'user_id':current_user_id,
               'employee_id':default_emp_id,
               'journal_id':_get_journal,
               'period_id': _get_period,
               'date': _get_date,
               'responsible':responsible_user_id,
               'online_transfer_flag':False,
               'cheque_number_flag':False,
               'reconcile_uncheck':False,

               }    
    
    
    def create(self, cr, uid, vals, context=None):
        ''' Overide create method to for sequencing'''
        
        obj_sequence=self.pool.get('ir.sequence')
            
        if vals.has_key('payment_method') : 
            if vals['payment_method'] =='cheque' : 
                if vals.has_key('cheque_number') :
                    if vals['cheque_number'] ==False: 
                        raise osv.except_osv(_('Validation Error'),
                                            _("Cheque Number is Required"))        
            
        if vals.get('responsible') : 
        
            context['responsible']=vals['responsible']
            vals['employee_id']=self.default_emp_id(cr, uid, context)        
        #obj_sequence.search(cr,uid,[('name','=',name)])
        #seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
        if vals.get('voucher_seq_number', False) == False:
            vals['voucher_seq_number'] = self.pool.get('ir.sequence').get(cr, uid, 'account.voucher') or '/'

            
        voucher = super(account_voucher, self).create(cr, uid, vals, context)
        return voucher      
           
    def write(self, cr, uid, ids, vals, context=None):
	#### SPECIAL RIGHTS FOR Asmita Sigwan,  Neha Kadam,Rakesh Nayak, Rency Dsouza
        #if uid in [521,453,435,454]  :
         #   SUPERID,uid=1,1
        
        if vals.has_key('payment_method') : 
            if vals['payment_method']=='online' : 
                pass
            else:
                if vals['cheque_number'] ==False : 
                    raise osv.except_osv(_('Validation Error'),
                                        _("Cheque Number is Required"))        
                                
        elif vals.has_key('cheque_number')  :
            if vals['cheque_number'] ==False : 
                raise osv.except_osv(_('Validation Error'),
                                    _("Cheque Number is Required"))        
        else : 
            pass
        
        if vals.get('responsible') : 
        
            context['responsible']=vals['responsible']
            vals['employee_id']=self.default_emp_id(cr, uid, context)
        result=super(account_voucher , self).write(cr, uid,ids, vals, context)
        return result              


    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context):
        
        result=super(account_voucher,self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None)
        if result : 
            
            if context.get('reconcile_uncheck') :  
                #remove credit line reconcile check
                if result.get('value').get('line_cr_ids') : 
                    for cr_line in result.get('value').get('line_cr_ids') : 
                        if isinstance(cr_line,dict): 
                                
                            if cr_line.get('reconcile') : 
                                cr_line['reconcile']=False  
                                cr_line['amount']=0.00    

                #remove debit line reconcile check
                if result.get('value').get('line_dr_ids') : 
                   
                    for dr_line in result.get('value').get('line_dr_ids') : 
                       # import ipdb;ipdb.set_trace()
                        if isinstance(dr_line,dict): 
                            if dr_line.get('reconcile') : 
                                dr_line['reconcile']=False 
                                dr_line['amount']=0.00
                            else : 
                                dr_line['amount']=0.00
#                     
            if partner_id :
                 
                if self.pool.get('res.users').browse(cr,uid,uid).company_id.id ==3 : 
                    return result                
                 
                business_manager=self.pool.get('res.partner').browse(cr,uid,partner_id).user_id
                if business_manager : 
                    result['value']['user_id']=business_manager.id
                    result['value']['remove_line']=False
                    
    #                 emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',business_manager.id)])
    #                 if emp_id :
    #                     if len(emp_id) >1 :
    #                         raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))                
    #                     result['value']['user_id_employee']=emp_id[0]
                    
                else :
                    
                    raise osv.except_osv(_('Validation Error!'), _("No saleperson defined For Partner! \nContact Accounts Team"))
        
        
                        
        return result


   
    def remove_voucher_lines_onchange(self, cr, uid, ids, selection, context=None):
        ''' Option to remove voucher lines'''
        
        if selection :
            vals={'line_cr_ids': [], 'line_dr_ids': []}
            return {'value':vals} 
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0]})
                
                
        else:
            vals={}
            return {'value':vals}
            
    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id,context):
        

        result=super(account_voucher,self).onchange_journal(cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id,context=None)
        
        
        if result : 
            
            if context.get('reconcile_uncheck') :  
                #remove credit line reconcile check
                if result.get('value').get('line_cr_ids') : 
                    for cr_line in result.get('value').get('line_cr_ids') : 
                        if isinstance(cr_line,dict): 
                                
                            if cr_line.get('reconcile') : 
                                cr_line['reconcile']=False  
                                cr_line['amount']=0.00   

                #remove debit line reconcile check
                if result.get('value').get('line_dr_ids') : 
                    for dr_line in result.get('value').get('line_dr_ids') : 
                        if isinstance(dr_line,dict): 
                            if dr_line.get('reconcile') : 
                                dr_line['reconcile']=False 
                                dr_line['amount']=0.00  
                                
                            else : 
                                dr_line['amount']=0.00                                                                 
            
            result['value']['remove_line']=False
        return result

    def onchange_amount(self, cr, uid, ids, amount, rate, partner_id, journal_id, \
                        currency_id, ttype, date, payment_rate_currency_id, company_id, context):
        
        result=super(account_voucher,self).onchange_amount(cr, uid, ids, amount, rate, partner_id, journal_id, \
                        currency_id, ttype, date, payment_rate_currency_id, company_id, context=None)
        
        if result : 
          
            if context.get('reconcile_uncheck') : 
                if result.get('value').get('line_cr_ids') : 
                    for cr_line in result.get('value').get('line_cr_ids') : 
                        if isinstance(cr_line,dict) : 
                                if cr_line.get('reconcile') : 
                                    cr_line['reconcile']=False  
                                    cr_line['amount']=0.00 
                                    
                                    
                if result.get('value').get('line_dr_ids') : 
                    for dr_line in result.get('value').get('line_dr_ids') : 
                        if isinstance(dr_line,dict): 
                            if dr_line.get('reconcile') : 
                                dr_line['reconcile']=False 
                                dr_line['amount']=0.00   
                                 
                            else : 
                                dr_line['amount']=0.00                                                                                  
        
        return result


    
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
