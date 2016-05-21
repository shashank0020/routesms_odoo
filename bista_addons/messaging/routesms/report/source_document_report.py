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
class report_print_source(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_source, self).__init__(cr, uid, name, context)
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
        origin_report_val={}
        result=[]
        account_obj=self.pool.get('account.invoice')
        source_doc_report_obj=self.pool.get('source.document.report')	
        count=0
        
        try : 
            
            ###############fllush all data###############

            cr.execute('''delete from source_document_report''')
            
            ##############collect customer invoice source.document###################
                        
            cr.execute('''select origin from account_invoice where type='out_invoice' and company_id=3 and journal_id in (150,152,154,10,156,158)''')
            
            cust_origin_old=map(lambda x:x[0],cr.fetchall())
            if None in cust_origin_old : 
                
                cust_origin_old.remove(None)
            

              
            cust_origin_no=[x.split(',')[0] for x in cust_origin_old if x ]
              
            ##############collect supplier invoice pnr no###################
            cr.execute('''select origin from account_invoice where type='in_invoice' and company_id=3 and journal_id in (151,153,155,157,159,11) ''')
            supp_origin_no_old=map(lambda x:x[0],cr.fetchall())
            if None in supp_origin_no_old : 
                
                supp_origin_no_old.remove(None)  
            
            supp_origin_no=[x.split(',')[0] for x in supp_origin_no_old if x]          
            
            ###################intersection operaton on 2 list################
                        
            intersected_origin_no= list(Set(cust_origin_no) & Set(supp_origin_no))
            difference_origin_no = list(set(list(Set(cust_origin_no) - Set(supp_origin_no)) + list(Set(supp_origin_no) - Set(cust_origin_no))))
            
            
            ######################prepare data and insert into table###################
            
            for inter_origin_no in intersected_origin_no :

                    
                count+=1;print count
                    
                cr.execute('''select id from account_invoice where type='out_invoice' and origin=%s ''',(inter_origin_no,))
                cust_id=map(lambda x:x[0],cr.fetchall())
                
                if cust_id :
                    invoice=account_obj.browse(cr,uid,cust_id[0])
                    for inv_line in invoice.invoice_line :
                        cust_product=inv_line.product_id.name
                        cust_ref=inv_line.holiday_refernce_number
                        cust_passenger_name=inv_line.passenger_name_air
                        cust_passenger_name_others=inv_line.passenger_name
                        break

                    origin_report_val.update({'customer':invoice.partner_id.name,'tax_amount':invoice.amount_tax,\
                    'customer_subtotal':invoice.amount_untaxed,})
                    
                
                else : 
                    cust_product,cust_ref,cust_passenger_name,cust_passenger_name_others='','','',''
                    origin_report_val.update({'customer':'No Customer Found','tax_amount':0.0,\
                    'customer_subtotal':0.0})
                    
                #################insert invpoce line
                
                cr.execute('''select id from account_invoice where type='in_invoice' and origin=%s ''',(inter_origin_no,))
                supp_id=map(lambda x:x[0],cr.fetchall())
                
                
                if supp_id : 
                    invoice=account_obj.browse(cr,uid,supp_id[0])
                    origin_report_val.update({'supplier':invoice.partner_id.name,'date_invoice':invoice.date_invoice,\
                    'supplier_amount':invoice.amount_total})
                    for inv_line in invoice.invoice_line :
                        supp_product=inv_line.product_id.name
                        supp_ref=inv_line.holiday_refernce_number
                        supp_passenger_name=inv_line.passenger_name_air
                        supp_passenger_name_others=inv_line.passenger_name
                        break                    
                    
                
                else : 
                    supp_product,supp_ref,supp_passenger_name,supp_passenger_name_others='','','',''
                    origin_report_val.update({'supplier':'No Supplier Found','date_invoice':'-',\
                    'supplier_amount':0.00})
                
######################################check identical##########################                
                if cust_passenger_name : 
                    passenger=cust_passenger_name
                
                elif supp_passenger_name : 
                    passenger=supp_passenger_name

                elif cust_passenger_name_others : 
                    passenger=cust_passenger_name_others
                
                elif supp_passenger_name_others : 
                    passenger=supp_passenger_name_others
                    

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
                    
                #################update origin_report_vals############
                origin_report_val.update({'product_line':product,'passenger_name':passenger\
                                       ,'reference':ref,'source_document':inter_origin_no})
                ###################ends############################
                   
##################################ends#############################################

                    
                ###########calculate profit###################
                
                origin_report_val['profit']=origin_report_val['customer_subtotal'] - origin_report_val['supplier_amount'] - origin_report_val['tax_amount']
                
                ###################insert into pnr table###############
                 
                origin_id=source_doc_report_obj.create(cr,uid,origin_report_val)           
                
                
                
                #####################prepare data from single pnr list############
            for diff_origin_no in difference_origin_no :
                count+=1;print count 
               
                cr.execute('''select id from account_invoice where type='out_invoice' and origin=%s ''',(diff_origin_no,))
                cust_id=map(lambda x:x[0],cr.fetchall())
                
                if cust_id : 
                    invoice=account_obj.browse(cr,uid,cust_id[0])
                    for inv_line in invoice.invoice_line :
                        cust_product=inv_line.product_id.name
                        cust_ref=inv_line.holiday_refernce_number
                        cust_passenger_name=inv_line.passenger_name_air
                        cust_passenger_other=inv_line.passenger_name
                        break
                    
                    origin_report_val.update({'customer':invoice.partner_id.name,'tax_amount':invoice.amount_tax,\
                    'customer_subtotal':invoice.amount_untaxed})
                else : 
                    cust_product,cust_ref,cust_passenger_name,cust_passenger_other='','','',''
                    origin_report_val.update({'customer':'No Customer Found','tax_amount':0.0,\
                    'customer_subtotal':0.0})
                    
    
    
                cr.execute('''select id from account_invoice where type='in_invoice' and origin=%s ''',(diff_origin_no,))
                supp_id=map(lambda x:x[0],cr.fetchall())
                if supp_id : 
                    invoice=account_obj.browse(cr,uid,supp_id[0])
                    for inv_line in invoice.invoice_line :
                        supp_product=inv_line.product_id.name
                        supp_ref=inv_line.holiday_refernce_number
                        supp_passenger_name=inv_line.passenger_name_air
                        supp_passenger_name_other=inv_line.passenger_name
                        
                        break  
                                        
                    origin_report_val.update({'supplier':invoice.partner_id.name,'date_invoice':invoice.date_invoice,\
                    'supplier_amount':invoice.amount_total})
                else :
                    supp_product,supp_ref,supp_passenger_name,supp_passenger_name_other='','','',''
                    origin_report_val.update({'supplier':'No Supplier Found','date_invoice':'-',\
                    'supplier_amount':0.00})

                
######################################check identical##########################                
                if cust_passenger_name : 
                    passenger=cust_passenger_name
                
                elif supp_passenger_name : 
                    passenger=supp_passenger_name

                elif cust_passenger_other : 
                    passenger=cust_passenger_other                   
                    
                elif supp_passenger_name_other : 
                    passenger=supp_passenger_name_other                     
                    
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



                #################update origin_report_vals############
                origin_report_val.update({'product_line':product,'passenger_name':passenger\
                                       ,'reference':ref,'source_document':diff_origin_no})
                ###################ends############################
                
                ###########calculate profit###################
    
                origin_report_val['profit']=origin_report_val['customer_subtotal'] - origin_report_val['supplier_amount'] - origin_report_val['tax_amount']
                ###################insert into pnr table###############
                
                origin_id=source_doc_report_obj.create(cr,uid,origin_report_val)
                
                
                #########################################
        #################collect all data in list###########
            origin_report_ids=source_doc_report_obj.search(cr,uid,[])

            result=[pnr_obj_id for pnr_obj_id in  source_doc_report_obj.browse(cr,uid,origin_report_ids)]
            return result
            
        
            
        except Exception as E : 
            
            print '-----------ERROR {}----',E
            print count
            raise osv.except_osv(_('Error !'), _("Report Cannot Be Printed!!\nContact Odoo Team"))

            
        return result
    
    def get_line(self):
        
        result=self.insert_into_report_print_check()
        
        
        return result

class report_source(osv.AbstractModel):
    _name = 'report.routesms.report_source'
    _inherit = 'report.abstract_report'
    _template = 'routesms.report_source'
    _wrapped_report_class = report_print_source

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
