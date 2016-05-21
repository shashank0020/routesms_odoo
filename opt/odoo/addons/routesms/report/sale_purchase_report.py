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
from openerp.tools.translate import _

from sets import Set
class report_print_sale_purchase(report_sxw.rml_parse):
    
    
    def __init__(self, cr, uid, name, context):
        super(report_print_sale_purchase, self).__init__(cr, uid, name, context)
        self.number_lines = 0
        self.number_add = 0
        self.localcontext.update({
            'time': time,
            'get_data': self.get_data,
            'get_line':self.get_line,
            'check_report_type':self.check_report_type,
            'get_sum_subtotal':self.get_sum_subtotal,
#             'get_sum_tax':self.get_sum_tax,
#             'get_sum_total':self.get_sum_total,

        })
        

    def check_report_type(self,data):
        
        if data.get('form').get('report_type')=='sale' :
            head='Sale Invoice Report' 

        elif data.get('form').get('report_type')=='sale_refund' :
            head='Sale Refund Invoice Report' 

        elif data.get('form').get('report_type')=='purchase' :
            head='Purchase Invoice Report' 
            
        elif data.get('form').get('report_type')=='purchase_refund' :
            head='Purchase Refund Invoice Report'                         
        
        return head


                
    def get_data(self,type):
        '''prepare report data '''
        
        cr=self.cr
        uid=self.uid
        account_obj=self.pool.get('account.invoice')
        tax_obj=self.pool.get('account.tax')
        try : 
            
            ###get user login company
            company_id=self.pool.get('res.users').browse(cr,uid,uid).company_id.id
            #######sale tax################
            sale_tax_id_12_percent=tax_obj.search(cr,uid,[('name','ilike','Output Service Tax @ 12.36%'),('company_id','=',company_id)])
            sale_tax_id_14_percent=tax_obj.search(cr,uid,[('name','ilike','Output Service Tax @14% RSL'),('company_id','=',company_id)])
            #####purchase tax#############
            purchase_tax_id_12_percent=sale_tax_id_12_percent=tax_obj.search(cr,uid,[('name','ilike','Input Service Tax @ 12.36%'),('company_id','=',company_id)])
            purchase_tax_id_14_percent=sale_tax_id_12_percent=tax_obj.search(cr,uid,[('name','ilike','Input Service Tax @ 14%'),('company_id','=',company_id)])
            
#####INDIA#####################           
            
            ####case 1 ###############
            if type['report_type'] =='sale' and type['type'] =='india': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)
                
                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice' and x.partner_id\
                                  .country_id.id  in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    #import ipdb;ipdb.set_trace()
                            
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                else : 
                    
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice' and x.partner_id\
                                  .country_id.id  in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                    
                    
                     
                print '--------------Filtered Sale invocies(INDIA)----------',len(result)
                return result


            ####case 2###############
            elif type['report_type'] =='sale_refund' and type['type'] =='india': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' and x.partner_id\
                                  .country_id.id  in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                     
                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' and x.partner_id\
                                  .country_id.id  in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                                        
                    
                print '--------------Filtered Sale Refund invocies(INDIA)----------',len(result)
                return result


            ####case 3###############
            elif type['report_type'] =='purchase' and type['type'] =='india': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' and x.partner_id\
                                  .country_id.id  in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' and x.partner_id\
                                  .country_id.id  in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                                        
                print '--------------Filtered Purchase invocies(INDIA)----------',len(result)
                return result


            ####case 4###############
            elif type['report_type'] =='purchase_refund' and type['type'] =='india': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' and x.partner_id\
                                  .country_id.id  in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                                        
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' and x.partner_id\
                                  .country_id.id  in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                print '--------------Filtered Purchase Refund invocies(INDIA)----------',len(result)
                return result


########INTERNATIONAL###########################

            ####case 1 ###############not
            if type['report_type'] =='sale' and type['type'] =='int': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)
                
                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice' and x.partner_id\
                                  .country_id.id not in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)

                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice' and x.partner_id\
                                  .country_id.id not in [105,255],invoice)

                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                    
                     
                print '--------------Filtered Sale invocies(INTERNATIONAL)----------',len(result)
                return result


            ####case 2###############
            elif type['report_type'] =='sale_refund' and type['type'] =='int': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' and x.partner_id\
                                  .country_id.id not in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)

                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' and x.partner_id\
                                  .country_id.id not in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                    
                print '--------------Filtered Sale Refund invocies(INTERNATIONAL)----------',len(result)
                return result


            ####case 3###############
            elif type['report_type'] =='purchase' and type['type'] =='int': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' and x.partner_id\
                                  .country_id.id not in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' and x.partner_id\
                                  .country_id.id not in [105,255],invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]
                    
                print '--------------Filtered Purchase invocies(INTERNATIONAL)----------',len(result)
                return result


            ####case 4###############
            elif type['report_type'] =='purchase_refund' and type['type'] =='int': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' and x.partner_id\
                                  .country_id.id not in [105,255] and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]

                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' and x.partner_id\
                                  .country_id.id not in [105,255],invoice)

                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]

                    
                    
                print '--------------Filtered Purchase Refund invocies(INTERNATIONAL)----------',len(result)
                return result


############ALL###########################
            ####case 1 ###############not
            if type['report_type'] =='sale' and type['type'] =='all': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)
                
                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice' and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)

                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_invoice',invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                    
                     
                print '--------------Filtered Sale invocies(ALL)----------',len(result)
                return result


            ####case 2###############
            elif type['report_type'] =='sale_refund' and type['type'] =='all': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(sale_tax_id_12_percent+sale_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='out_refund' ,invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                    
                print '--------------Filtered Sale Refund invocies(ALL)----------',len(result)
                return result


            ####case 3###############
            elif type['report_type'] =='purchase' and type['type'] =='all': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_invoice' ,invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                print '--------------Filtered Purchase invocies(ALL)----------',len(result)
                return result


            ####case 4###############
            elif type['report_type'] =='purchase_refund' and type['type'] =='all': 
                
                cr.execute('''select invoice_line_id from account_invoice_line_tax where tax_id in  %s''',(tuple(purchase_tax_id_12_percent+purchase_tax_id_14_percent),))
                invoice_line_ids=map(lambda x:x[0],cr.fetchall())
                
                cr.execute('''select distinct(invoice_id) from account_invoice_line where id in  %s''',(tuple(invoice_line_ids),))
                invoice_ids=map(lambda x:x[0],cr.fetchall())

                invoice=[x for x in   account_obj.browse(cr,uid,invoice_ids) ]
                print '--------------All invocies----------',len(invoice)

                if type.get('date_from') and type.get('date_to') :
                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' and x.date_invoice>=type.get('date_from')\
                                  and x.date_invoice<=type.get('date_to'),invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                else : 

                    result=filter(lambda x:x.state in ['open','paid'] and x.type=='in_refund' ,invoice)
                    new_ids=[x.id for x in result]
                    cr.execute(''' select id from account_invoice where id in %s ORDER BY date_invoice ASC; ''',(tuple(new_ids),))
                    result=[x for x in   account_obj.browse(cr,uid,map(lambda x:x[0],cr.fetchall())) ]                    
                print '--------------Filtered Purchase Refund invocies(ALL)----------',len(result)
                return result




        except Exception as E:
            return False
    
    def get_line(self,data):
        
        #if data.get('form').get('type') and data.get('form').get('report_type') :
        data_input={'type':data.get('form').get('type'),'report_type':data.get('form').get('report_type'),\
                    'date_from':data.get('form').get('date_from'),'date_to':data.get('form').get('date_to')} 
        result=self.get_data(data_input)

        return result
    
    def get_sum_subtotal(self,data):
        result={}
        if data.get('form').get('type') and data.get('form').get('report_type') :
            data_input={'type':data.get('form').get('type'),'report_type':data.get('form').get('report_type'),\
                        'date_from':data.get('form').get('date_from'),'date_to':data.get('form').get('date_to')} 
            invoice_result=self.get_data(data_input)

            if not invoice_result : 
                result.update({'amount_untaxed':0.00,'amount_tax':0.00,'amount_total':0.00})
                 
    
            elif invoice_result : 
                
                amount_untaxed=sum( map( lambda x:x.amount_untaxed, invoice_result ) )
                amount_tax=sum( map( lambda x:x.amount_tax, invoice_result ) )
                amount_total=sum( map( lambda x:x.amount_total, invoice_result ) )
                #import ipdb;ipdb.set_trace()
                result.update({'amount_untaxed':amount_untaxed,'amount_tax':amount_tax,'amount_total':amount_total})
                
        return result    
        
            

class report_sale_purchase(osv.AbstractModel):
    _name = 'report.routesms.report_sale_purchase'
    _inherit = 'report.abstract_report'
    _template = 'routesms.report_sale_purchase'
    _wrapped_report_class = report_print_sale_purchase

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
