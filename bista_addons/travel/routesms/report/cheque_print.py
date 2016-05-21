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

import time
from openerp.osv import osv
from openerp.report import report_sxw
from num2words import num2words

class report_print_cheque(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_cheque, self).__init__(cr, uid, name, context)
        self.number_lines = 0
        self.number_add = 0
        self.localcontext.update({
            'time': time,
            'get_lines': self.get_lines,
            'fill_stars' : self.fill_stars,
            'get_partner': self.get_partner,
            'get_amount_in_words':self.get_amount_in_words,
        })





    def number_to_words(self,n):
        words = ''
      
      
        number_spit=str(round(n,2)).split('.')
        n=int(number_spit[0])
        
        if number_spit[1] == '0' or number_spit[1]=='00' : 
            
            decimal_no='only'
        else :
            
            num=int(number_spit[1])
            decimal_no= 'and' + ' ' +str(num2words(num).replace('-', ' ')) + ' ' + 'paisa' + ' ' +'only'
        
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
    
  #  number_to_words(1223456.56)


    def get_amount_in_words(self,amount):
        
        vals=''
        if amount : 
            vals=self.number_to_words(amount)
            vals=vals + len(vals) * '*' + '\n******************************************'
        
        return vals      

    def get_partner(self,partner):
        
        vals=''
        if partner :
             
            vals=partner.name.upper() 
        
        return vals
            
             
            
        

    def fill_stars(self, amount):
            
        words=[]
        
        for i in amount:
        
            if i =='(':
                
                index=amount.index(i)
                words.append(i)
                kk=i
                
                while kk !=')' :
                    index+=1
                    
                    kk=amount[index]
                    words.append(kk)

        amount=amount.replace(''.join(words),'')
        
        if len(amount) < 100:
            stars = 100 - len(amount)
            return ' '.join([amount,'*'*stars])

        else: return amount

    def get_lines(self, voucher_lines):
        result = []
        self.number_lines = len(voucher_lines)
        for i in range(0, min(10,self.number_lines)):
            if i < self.number_lines:
                res = {
                    'date_due' : voucher_lines[i].date_due,
                    'name' : voucher_lines[i].name,
                    'amount_original' : voucher_lines[i].amount_original and voucher_lines[i].amount_original or False,
                    'amount_unreconciled' : voucher_lines[i].amount_unreconciled and voucher_lines[i].amount_unreconciled or False,
                    'amount' : voucher_lines[i].amount and voucher_lines[i].amount or False,
                }
            else :
                res = {
                    'date_due' : False,
                    'name' : False,
                    'amount_original' : False,
                    'amount_due' : False,
                    'amount' : False,
                }
            result.append(res)
        return result


class report_cheque(osv.AbstractModel):
    _name = 'report.routesms.report_cheque'
    _inherit = 'report.abstract_report'
    _template = 'routesms.report_cheque'
    _wrapped_report_class = report_print_cheque

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
