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


class account_invoice(models.Model):

    _inherit ='account.invoice'
    
#     @api.multi
#     def button_reset_taxes(self):
#         
#         account_invoice_tax = self.env['account.invoice.tax']
#         ctx = dict(self._context)
#         for invoice in self:
#             self._cr.execute("DELETE FROM account_invoice_tax WHERE invoice_id=%s AND manual is False", (invoice.id,))
#             self.invalidate_cache()
#             partner = invoice.partner_id
#             if partner.lang:
#                 ctx['lang'] = partner.lang
#             import ipdb;ipdb.set_trace()
# 
#             if self.env['res.users'].browse(self.env.uid).company_id.id == 3  and  self.env['res.users'].browse(self.env.uid).holiday_vertical_list =='air' :
#                 update_amount_list=self.cal(invoice)
#                 #a1=(self.env['account.invoice'].browse(invoice.id).basic_amount + self.env.browse(invoice.id).markup_air)
#                 count=0
#                 for taxe in account_invoice_tax.compute(invoice.with_context(ctx)).values():
#                     
#                     taxe['tax_amount']= update_amount_list[count]
#                     taxe['amount']=update_amount_list[count]
#                     account_invoice_tax.create(taxe)
#                     count+=1                        
#                         
#                         
#             else :
#                 
#                 for taxe in account_invoice_tax.compute(invoice.with_context(ctx)).values():
#                     account_invoice_tax.create(taxe)                
#             # dummy write on self to trigger recomputations
#         return self.with_context(ctx).write({'invoice_line': []}) 
#     
#     def cal(self,invoice):
#         
#         tax_ids=[]
#         tax_amount_per_line=[]
#         import ipdb;ipdb.set_trace()
#         for line in invoice.invoice_line:
#             taxed_amount=[]
#             
#             
#             for tax in line.invoice_line_tax_id:
#                 tax_ids.append(tax)
#                 #taxed_amount.append((line.basic_amount + line.markup_air ) * tax.amount)
#                 
#         print_tax=set([tax for tax in tax_ids])
#         
#         return tax_amount_per_line
        

#     def cal(self,invoice):
#         
#         
#         tax_amount_per_line=[]
#         for line in invoice.invoice_line:
#             taxed_amount=[]
#             aa=set([tax for tax in line.invoice_line_tax_id])
#             import ipdb;ipdb.set_trace()
#             for tax in line.invoice_line_tax_id:
#                 
#                 taxed_amount.append((line.basic_amount + line.markup_air ) * tax.amount)
#                 
#             tax_amount_per_line.append(sum(taxed_amount))
#         return tax_amount_per_line

        
        
    
#     @api.one
#     @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
#     def _compute_amount(self):
#     #    import ipdb;ipdb.set_trace()
#        # self.env.cr.execute(''' update account_invoice_tax set amount=%s where invoice_id=%s''',(45,359))
#         self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
#         self.amount_tax = sum(line.amount for line in self.tax_line)
#         self.amount_total = self.amount_untaxed + self.amount_tax  


# 
# class account_invoice_tax(models.Model):
#     _inherit = "account.invoice.tax"
#     
#     
#     @api.multi
#     def amount_change(self, amount, currency_id=False, company_id=False, date_invoice=False):
#         import ipdb;ipdb.set_trace()
#         res=super(account_invoice_tax,self).amount_change(amount, currency_id=False, company_id=False, date_invoice=False)
#         res.update({'value':{'amount':778.123}})
#         return res
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
