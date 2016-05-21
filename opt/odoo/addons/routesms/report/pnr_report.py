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

from sets import Set
class report_print_pnr(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_pnr, self).__init__(cr, uid, name, context)
        self.number_lines = 0
        self.number_add = 0
        self.localcontext.update({
            'time': time,
            'insert_lines': self.insert_into_report_print_check,
            'get_line':self.get_line

        })
        

                
    def insert_into_report_print_check(self):
        '''prepare report data '''
        
        cr=self.cr
        uid=self.uid
        dub_pnr_vals={}
        dub_pnr_list=[]
        single_pnr_vals={}
        single_pnr_list=[]	
        pnr_report_val={}
        result=[]
        account_obj=self.pool.get('account.invoice')
        pnr_report_obj=self.pool.get('pnr.report')	
        count=0
        
        try : 
            
            ###############fllush all data###############

            cr.execute('''delete from pnr_report''')
            
            ##############collect customer invoice pnr no###################
                        
            cr.execute('''select pnr_no from account_invoice where type='out_invoice' and journal_id=148 ''')
            
            cust_pnr_no_old=map(lambda x:x[0],cr.fetchall())
            if None in cust_pnr_no_old : 
                
                cust_pnr_no_old.remove(None)

            cust_pnr_no=[x.split(',')[0] for x in cust_pnr_no_old if x ]
              
            ##############collect supplier invoice pnr no###################
            cr.execute('''select pnr_no from account_invoice where type='in_invoice' and journal_id=149 ''')
            supp_pnr_no_old=map(lambda x:x[0],cr.fetchall())
            if None in supp_pnr_no_old : 
                
                supp_pnr_no_old.remove(None)  
            
            supp_pnr_no=[x.split(',')[0] for x in supp_pnr_no_old if x]          
            
            ###################intersection operaton on 2 list################
            
            intersected_pnr= list(Set(cust_pnr_no) & Set(supp_pnr_no))
            difference_pnr = list(set(list(Set(cust_pnr_no) - Set(supp_pnr_no)) + list(Set(supp_pnr_no) - Set(cust_pnr_no))))
            
            
            ######################prepare data and insert into table###################
            
            for inter_pnr in intersected_pnr : 
                count+=1;print count
                    
                cr.execute('''select id from account_invoice where type='out_invoice' and pnr_no=%s ''',(inter_pnr,))
                cust_id=map(lambda x:x[0],cr.fetchall())
                
                if cust_id :
                    invoice=account_obj.browse(cr,uid,cust_id[0])
                    for inv_line in invoice.invoice_line :
                        cust_product=inv_line.product_id.name
                        cust_ref=inv_line.holiday_refernce_number
                        cust_passenger_name=inv_line.passenger_name_air
                        break

                    pnr_report_val.update({'customer':invoice.partner_id.name,'tax_amount':invoice.amount_tax,\
                    'customer_subtotal':invoice.amount_untaxed,})
                    
                
                else : 
                    pnr_report_val.update({'customer':'No Customer Found','tax_amount':0.0,\
                    'customer_subtotal':0.0})
                    
                #################insert invpoce line
                
                cr.execute('''select id from account_invoice where type='in_invoice' and pnr_no=%s ''',(inter_pnr,))
                supp_id=map(lambda x:x[0],cr.fetchall())
                
                
                if supp_id : 
                    invoice=account_obj.browse(cr,uid,supp_id[0])
                    pnr_report_val.update({'supplier':invoice.partner_id.name,'date_invoice':invoice.date_invoice,\
                    'supplier_amount':invoice.amount_total})
                    for inv_line in invoice.invoice_line :
                        supp_product=inv_line.product_id.name
                        supp_ref=inv_line.holiday_refernce_number
                        supp_passenger_name=inv_line.passenger_name_air
                        break                    
                    
                
                else : 
                    pnr_report_val.update({'supplier':'No Supplier Found','date_invoice':'-',\
                    'supplier_amount':0.00})
                
######################################check identical##########################                
                if cust_passenger_name : 
                    passenger=cust_passenger_name
                
                elif supp_passenger_name : 
                    passenger=supp_passenger_name
                    
                else :
                    
                    passenger='No Passenger Found'

                if cust_product : 
                    product=cust_product
                
                elif supp_product : 
                    product=supp_product
                    
                else :
                    
                    product='No Product Found'


                if cust_ref : 
                    ref=cust_ref
                
                elif supp_ref : 
                    ref=supp_ref
                    
                else :
                    
                    ref='No Reference Found'
                    
                #################update pnr_report_vals############
                pnr_report_val.update({'supplier_product_line':product,'supplier_passenger_name':passenger\
                                       ,'supplier_reference':ref,'supplier_pnr':inter_pnr})
                ###################ends############################
                   
##################################ends#############################################

                    
                ###########calculate profit###################
                
                pnr_report_val['profit']=pnr_report_val['customer_subtotal'] - pnr_report_val['supplier_amount'] - pnr_report_val['tax_amount']
                
                ###################insert into pnr table###############
                 
                pnr_id=pnr_report_obj.create(cr,uid,pnr_report_val)           
               
                
                
                #####################prepare data from single pnr list############
            for diff_pnr in difference_pnr : 
                count+=1;print count 
               
                cr.execute('''select id from account_invoice where type='out_invoice' and pnr_no=%s ''',(diff_pnr,))
                cust_id=map(lambda x:x[0],cr.fetchall())
                
                if cust_id : 
                    invoice=account_obj.browse(cr,uid,cust_id[0])
                    for inv_line in invoice.invoice_line :
                        cust_product=inv_line.product_id.name
                        cust_ref=inv_line.holiday_refernce_number
                        cust_passenger_name=inv_line.passenger_name_air
                        break
                    
                    pnr_report_val.update({'customer':invoice.partner_id.name,'tax_amount':invoice.amount_tax,\
                    'customer_subtotal':invoice.amount_untaxed})
                else : 
                    pnr_report_val.update({'customer':'No Customer Found','tax_amount':0.0,\
                    'customer_subtotal':0.0})
                    
    
    
                cr.execute('''select id from account_invoice where type='in_invoice' and pnr_no=%s ''',(inter_pnr,))
                supp_id=map(lambda x:x[0],cr.fetchall())
                if supp_id : 
                    invoice=account_obj.browse(cr,uid,supp_id[0])
                    for inv_line in invoice.invoice_line :
                        supp_product=inv_line.product_id.name
                        supp_ref=inv_line.holiday_refernce_number
                        supp_passenger_name=inv_line.passenger_name_air
                        break  
                                        
                    pnr_report_val.update({'supplier':invoice.partner_id.name,'date_invoice':invoice.date_invoice,\
                    'supplier_amount':invoice.amount_total})
                else : 
                    pnr_report_val.update({'supplier':'No Supplier Found','date_invoice':'-',\
                    'supplier_amount':0.00})


######################################check identical##########################                
                if cust_passenger_name : 
                    passenger=cust_passenger_name
                
                elif supp_passenger_name : 
                    passenger=supp_passenger_name
                    
                else :
                    
                    passenger='No Passenger Found'

                if cust_product : 
                    product=cust_product
                
                elif supp_product : 
                    product=supp_product
                    
                else :
                    
                    product='No Product Found'


                if cust_ref : 
                    ref=cust_ref
                
                elif supp_ref : 
                    ref=supp_ref
                    
                else :
                    
                    ref='No Reference Found'
                    
                    
##################################ends#############################################



                #################update pnr_report_vals############
                pnr_report_val.update({'supplier_product_line':product,'supplier_passenger_name':passenger\
                                       ,'supplier_reference':ref,'supplier_pnr':diff_pnr})
                ###################ends############################
                
                ###########calculate profit###################
    
                pnr_report_val['profit']=pnr_report_val['customer_subtotal'] - pnr_report_val['supplier_amount'] - pnr_report_val['tax_amount']
                ###################insert into pnr table###############
                
                pnr_id=pnr_report_obj.create(cr,uid,pnr_report_val)
                
                
                #########################################
        #################collect all data in list###########
            pnr_ids=pnr_report_obj.search(cr,uid,[])

            result=[pnr_obj_id for pnr_obj_id in  pnr_report_obj.browse(cr,uid,pnr_ids)]
            return result
            
        
            
        except Exception as E : 
            print '-----------ERROR {}----',E
            print count
            raise osv.except_osv(_('Error!'),_("Report Cannot be Printed\nContact Odoo Team"))

            
        return result
    
    def get_line(self):
        
        result=self.insert_into_report_print_check()
        
        
        return result

class report_check(osv.AbstractModel):
    _name = 'report.routesms.report_pnr'
    _inherit = 'report.abstract_report'
    _template = 'routesms.report_pnr'
    _wrapped_report_class = report_print_pnr

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
