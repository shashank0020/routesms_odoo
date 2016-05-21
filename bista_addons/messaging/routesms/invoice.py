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


import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp


class account_invoice_tax(models.Model):
    _inherit = "account.invoice.tax"
     
     
#     @api.multi
#     def amount_change(self, amount, currency_id=False, company_id=False, date_invoice=False):
#         
#         res=super(account_invoice_tax,self).amount_change(amount, currency_id=False, company_id=False, date_invoice=False)
#         #res.update({'value':{'amount':778.123}})
#         return res

    def compute_on_base_amount(self,base,child):
        ''' calculate child tax on base amount '''
       

        return base*child.amount 


    @api.v8
    def compute__discard_due_to_mulitple_tax(self, invoice):
        tax_grouped = {}
        #############check for mulitlple taxes on same line or same invoices
        data=[]
        refer_base_amount=[]

#         if invoice.invoice_line : 
#             for x in invoice.invoice_line : 
#                 for tax_id in x.invoice_line_tax_id : 
#                     
#                     data.append(tax_id.id)
#         
#         if len(set(data)) >1 : 
# 
#             raise except_orm(_('Error!'),
#                 _("Multiple Taxes Not Allowed!"))


       ####ends##########################
                    
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
                
                
            ####custom code starts##########
            base_amount_of_parent_tax=[] 
            child_tax_names=[] 
            child_tax_id=[]
            tax_dict={}             
            if line.invoice_line_tax_id:
                for invoice_line_tax in line.invoice_line_tax_id  : 
                    ####check for applying child tax computation on base amount##########
                    
                    if not invoice_line_tax.compute_child_on_base :  
                        ####custom code ends##########

                
                        for tax in taxes:
                            val = {
                                'invoice_id': invoice.id,
                                'name': tax['name'],
                                'amount': tax['amount'],
                                'manual': False,
                                'sequence': tax['sequence'],
                                'base': currency.round(tax['price_unit'] * line['quantity']),
                            }
                            if invoice.type in ('out_invoice','in_invoice'):
                                val['base_code_id'] = tax['base_code_id']
                                val['tax_code_id'] = tax['tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_collected_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_collected_id']
                            else:
                                val['base_code_id'] = tax['ref_base_code_id']
                                val['tax_code_id'] = tax['ref_tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_paid_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_paid_id']
            
                            # If the taxes generate moves on the same financial account as the invoice line
                            # and no default analytic account is defined at the tax level, propagate the
                            # analytic account from the invoice line to the tax line. This is necessary
                            # in situations were (part of) the taxes cannot be reclaimed,
                            # to ensure the tax move is allocated to the proper analytic account.
                            if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                                val['account_analytic_id'] = line.account_analytic_id.id
            
                            key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                            if not key in tax_grouped:
                                tax_grouped[key] = val
                            else:
                                tax_grouped[key]['base'] += val['base']
                                tax_grouped[key]['amount'] += val['amount']
                                tax_grouped[key]['base_amount'] += val['base_amount']
                                tax_grouped[key]['tax_amount'] += val['tax_amount']

                    else : ##### allow to compute child tax on base amount####

                        if invoice_line_tax.child_ids : 
                            #import ipdb;ipdb.set_trace()
                            child_tax_names=[ tax_dict.update({child.name:child}) for child in invoice_line_tax.child_ids  ]
                            
#                 for child in line.child_ids : 
#                     child_tax_names.append(child.name) #append child name
#                     child_tax_id.append(child.id) #append child id                        

                        for tax in taxes:
                            if tax['name'] in tax_dict.keys() :                             
#                                 val = {
#                                     'invoice_id': invoice.id,
#                                     'name': tax['name'],
#                                     'amount': self.compute_on_base_amount(base_amount_of_parent_tax[0],tax_dict[tax['name']]),
#                                     'manual': False,
#                                     'sequence': tax['sequence'],
#                                     'base': base_amount_of_parent_tax[0],
#                                 }
                                val = {
                                    'invoice_id': invoice.id,
                                    'name': tax['name'],
                                    'amount': self.compute_on_base_amount(invoice.amount_untaxed,tax_dict[tax['name']]),
                                    'manual': False,
                                    'sequence': tax['sequence'],
                                    'base': invoice.amount_untaxed,
                                }
                            else : 
                                
                                val = {
                                    'invoice_id': invoice.id,
                                    'name': tax['name'],
                                    'amount': tax['amount'],
                                    'manual': False,
                                    'sequence': tax['sequence'],
                                    'base': currency.round(tax['price_unit'] * line['quantity']),
                                    
                                    }       
                                base_amount_of_parent_tax.append(val['base']) ###append base amount for child taxes##########                         
                                
                            if invoice.type in ('out_invoice','in_invoice'):
                                val['base_code_id'] = tax['base_code_id']
                                val['tax_code_id'] = tax['tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_collected_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_collected_id']
                            else:
                                val['base_code_id'] = tax['ref_base_code_id']
                                val['tax_code_id'] = tax['ref_tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_paid_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_paid_id']
            
                            # If the taxes generate moves on the same financial account as the invoice line
                            # and no default analytic account is defined at the tax level, propagate the
                            # analytic account from the invoice line to the tax line. This is necessary
                            # in situations were (part of) the taxes cannot be reclaimed,
                            # to ensure the tax move is allocated to the proper analytic account.
                            if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                                val['account_analytic_id'] = line.account_analytic_id.id
            
                            key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                            if not key in tax_grouped:
                                tax_grouped[key] = val
                            else:
                                tax_grouped[key]['base'] += val['base']
                                tax_grouped[key]['amount'] += val['amount']
                                tax_grouped[key]['base_amount'] += val['base_amount']
                                tax_grouped[key]['tax_amount'] += val['tax_amount']                        
                        
                                    

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])

        return tax_grouped   




    
    @api.v8
    def compute(self, invoice):
        tax_grouped = {}
        #############check for mulitlple taxes on same line or same invoices
        data=[]
        refer_base_amount=[]
        if invoice.invoice_line : 
            for x in invoice.invoice_line : 
                for tax_id in x.invoice_line_tax_id : 
                     
                    data.append(tax_id.id)
         
        if len(set(data)) >1 : 
 
            raise except_orm(_('Error!'),
                _("Multiple Taxes Not Allowed!"))
        ####ends##########################

       ####ends##########################
                    
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
                
                
            ####custom code starts##########
            base_amount_of_parent_tax=[] 
            child_tax_names=[] 
            child_tax_id=[]
            tax_dict={}             
            if line.invoice_line_tax_id:
                for invoice_line_tax in line.invoice_line_tax_id  : 
                    ####check for applying child tax computation on base amount##########
                    
                    if not invoice_line_tax.compute_child_on_base :  
                        ####custom code ends##########

                
                        for tax in taxes:
                            val = {
                                'invoice_id': invoice.id,
                                'name': tax['name'],
                                'amount': tax['amount'],
                                'manual': False,
                                'sequence': tax['sequence'],
                                'base': currency.round(tax['price_unit'] * line['quantity']),
                            }
                            if invoice.type in ('out_invoice','in_invoice'):
                                val['base_code_id'] = tax['base_code_id']
                                val['tax_code_id'] = tax['tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_collected_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_collected_id']
                            else:
                                val['base_code_id'] = tax['ref_base_code_id']
                                val['tax_code_id'] = tax['ref_tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_paid_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_paid_id']
            
                            # If the taxes generate moves on the same financial account as the invoice line
                            # and no default analytic account is defined at the tax level, propagate the
                            # analytic account from the invoice line to the tax line. This is necessary
                            # in situations were (part of) the taxes cannot be reclaimed,
                            # to ensure the tax move is allocated to the proper analytic account.
                            if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                                val['account_analytic_id'] = line.account_analytic_id.id
            
                            key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                            if not key in tax_grouped:
                                tax_grouped[key] = val
                            else:
                                tax_grouped[key]['base'] += val['base']
                                tax_grouped[key]['amount'] += val['amount']
                                tax_grouped[key]['base_amount'] += val['base_amount']
                                tax_grouped[key]['tax_amount'] += val['tax_amount']

                    else : ##### allow to compute child tax on base amount####

                        if invoice_line_tax.child_ids : 
                            #import ipdb;ipdb.set_trace()
                            child_tax_names=[ tax_dict.update({child.name:child}) for child in invoice_line_tax.child_ids  ]
                            
#                 for child in line.child_ids : 
#                     child_tax_names.append(child.name) #append child name
#                     child_tax_id.append(child.id) #append child id                        

                        for tax in taxes:
                            if tax['name'] in tax_dict.keys() :                             
                                val = {
                                    'invoice_id': invoice.id,
                                    'name': tax['name'],
                                    'amount': self.compute_on_base_amount(base_amount_of_parent_tax[0],tax_dict[tax['name']]),
                                    'manual': False,
                                    'sequence': tax['sequence'],
                                    'base': base_amount_of_parent_tax[0],
                                }
                            else : 
                                
                                val = {
                                    'invoice_id': invoice.id,
                                    'name': tax['name'],
                                    'amount': tax['amount'],
                                    'manual': False,
                                    'sequence': tax['sequence'],
                                    'base': currency.round(tax['price_unit'] * line['quantity']),
                                    
                                    }       
                                base_amount_of_parent_tax.append(val['base']) ###append base amount for child taxes##########                         
                                
                            if invoice.type in ('out_invoice','in_invoice'):
                                val['base_code_id'] = tax['base_code_id']
                                val['tax_code_id'] = tax['tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_collected_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_collected_id']
                            else:
                                val['base_code_id'] = tax['ref_base_code_id']
                                val['tax_code_id'] = tax['ref_tax_code_id']
                                val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                                val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                                val['account_id'] = tax['account_paid_id'] or line.account_id.id
                                val['account_analytic_id'] = tax['account_analytic_paid_id']
            
                            # If the taxes generate moves on the same financial account as the invoice line
                            # and no default analytic account is defined at the tax level, propagate the
                            # analytic account from the invoice line to the tax line. This is necessary
                            # in situations were (part of) the taxes cannot be reclaimed,
                            # to ensure the tax move is allocated to the proper analytic account.
                            if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                                val['account_analytic_id'] = line.account_analytic_id.id
            
                            key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                            if not key in tax_grouped:
                                tax_grouped[key] = val
                            else:
                                tax_grouped[key]['base'] += val['base']
                                tax_grouped[key]['amount'] += val['amount']
                                tax_grouped[key]['base_amount'] += val['base_amount']
                                tax_grouped[key]['tax_amount'] += val['tax_amount']                        
                        
                                    

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])

        return tax_grouped  
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
