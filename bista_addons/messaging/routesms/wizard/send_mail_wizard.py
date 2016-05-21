# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import email_split
from openerp import SUPERUSER_ID
from openerp.routesms_email.routesms_email import *
from time import gmtime, strftime
from lxml import etree
import csv
import xlsxwriter
SUPERID=1


class partner_swap_request_wizard(osv.osv_memory):

    _name = 'partner.swap.request.wizard'
    _description = 'Send notification to Sale super user to request swap  partner'


    _columns={
              'int_user_id':fields.many2one('int.user','Salesperson'),
              'ind_user_id':fields.many2one('ind.user','Salesperson'),
              'is_int_user':fields.boolean('International User?'),
              'is_ind_user':fields.boolean('Indian User?'),

              'int_superuser_id':fields.many2one('int.user','Send Request To'),
              'ind_superuser_id':fields.many2one('ind.user','Send Request To'),
              'is_int_superuser':fields.boolean('International SuperUser?'),
              'is_ind_superuser':fields.boolean('Indian SuperUser?'),              
              
              
              }

    _defaults={
             'is_int_user':False,
             'is_ind_user':False,  
             'is_int_superuser':False,
             'is_ind_superuser':False,             
               }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        user_obj=self.pool.get('res.users')
        group_obj=self.pool.get('res.groups')
        swap_partner_group_id=89
         
        res = super(partner_swap_request_wizard, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form': 
            doc = etree.XML(res['arch'])
	    
            if user_obj.browse(cr,uid,uid).partner_type=='international' : 
                
                int_sale_superuser=[ groupuser.id for groupuser in group_obj.browse(cr,SUPERID,swap_partner_group_id).users\
                                     if groupuser.partner_type=='international']

                for node in doc.xpath("//field[@name='int_superuser_id']"):
                    
                    user_filter =  "[('name', 'in'," + str(int_sale_superuser) + " )]" 
                     
                    node.set('domain',user_filter)                
                
            elif user_obj.browse(cr,uid,uid).partner_type=='india' :
                ind_sale_superuser=[ groupuser.id for groupuser in group_obj.browse(cr,SUPERID,swap_partner_group_id).users\
                                     if groupuser.partner_type=='india']    
                
                for node in doc.xpath("//field[@name='ind_superuser_id']"):
                    
                    user_filter =  "[('name', 'in'," + str(ind_sale_superuser) + " )]" 
                     
                    node.set('domain',user_filter)        
       
            else : 
                raise osv.except_osv(_('Error!'),_("User's Partner Type Not Found !\nContact HR Department"))
              
            
            
            

            res['arch'] = etree.tostring(doc)
            return res            

                  
        return res

    def default_get(self, cr, uid, fields, context):
        
        partner_obj = self.pool.get('res.partner')
        user_obj = self.pool.get('res.users')
        res={}
        
        
        if user_obj.browse(cr,uid,uid).partner_type =='india' : 
            res.update({'is_ind_user':True,'is_ind_superuser':True})
            res.update({'is_int_user':False,'is_int_superuser':False})
        else : 
            res.update({'is_int_user':True,'is_int_superuser':True})
            res.update({'is_ind_user':False,'is_ind_superuser':False})

        return res    

    def generate_attachment(self,cr,uid,data): 
        ###generate csv file for attchment
        vals={}
        count=1
        
        vals.update({'filename':'partner_migration'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()).replace(' ','')})
        
        # Create an new Excel file and add a worksheet.
        #path='/home/bista/Downloads/shanky/testing/'
        path='/home/bista/Downloads/sales_team/swap_partner_request/'
        workbook = xlsxwriter.Workbook(path+vals.get('filename') + '.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        # set the headers
        
        # Widen the first column to make the text clearer.
        for column in ['A','B','C','D'] : 
            worksheet.set_column(column+':'+column, 15) 
            
           
             
        for headers_data in zip (['A1','B1','C1','D1'],['Partner Name','Odoo Id','Old BM','New BM']) : 
            worksheet.write(headers_data[0], headers_data[1], bold)
        
        #store the values in sheet
        for sr_no in range(len(data)) :
            count+=1
            worksheet.write(count, 0,data[sr_no][0] )
            worksheet.write(count, 1,data[sr_no][1] )
            worksheet.write(count, 2,data[sr_no][2] )
            worksheet.write(count, 3,data[sr_no][3] )
        
        workbook.close()
        with open(path+vals.get('filename') + '.xlsx','rb') as e:
            vals.update({'binary':e.read()})        

        return vals
          
    def send_swap_request_mail(self, cr, uid, ids, context):
        ''' Send mail to sale superuser about partner swap'''
        
        partner_obj=self.pool.get('res.partner')
        user_obj=self.pool.get('res.users')
        routesms_email_config_obj=self.pool.get('send.email.with.attactment')
        group_obj=self.pool.get('res.groups')
        swap_partner_group_id=89 
        #data=[['Partner Name','Odoo Id','Old BM','New BM']]
        data=[]
        
        if context.get('active_id') : 
            superuser_ids=[ groupuser.id for groupuser in group_obj.browse(cr,SUPERID,swap_partner_group_id).users] 
            swap=self.browse(cr,SUPERID,ids[0])     
            if swap.is_ind_user and not swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson TO Swap')) 

            if swap.is_ind_superuser and not swap.ind_superuser_id : 
                raise osv.except_osv(_('Error'),_('Select SuperUser')) 


             
            if swap.is_int_user and not swap.int_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson TO Swap'))

             
            if swap.is_int_superuser and not swap.int_superuser_id : 
                raise osv.except_osv(_('Error'),_('Select Select SuperUser'))
            


            if swap.is_int_user and swap.is_ind_user : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))
            
            if swap.int_user_id and swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))


            if swap.int_user_id:
                if uid not in superuser_ids : 
                    if swap.int_user_id.name.id==uid : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))


            if swap.ind_user_id: 
                if uid not in superuser_ids : 
                    if swap.ind_user_id.name.id==uid : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))

            for partner in partner_obj.browse(cr,uid,context.get('active_ids')) : 

                if not partner.country_id : 
                    raise osv.except_osv(_('Request Failed !'), _('No Country Found For Partner: {} & Odoo id : {} \nAssign Country In Partner & Try Again')\
                                         .format(partner.name,partner.partner_sequence) )
                    
                if swap.int_user_id : 
                    if partner.user_id.partner_type !=swap.int_user_id.name.partner_type : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate Partner Of Other Department'))
                
                if swap.ind_user_id :
                    if partner.user_id.partner_type !=swap.ind_user_id.name.partner_type : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate Partner Of Other Department'))            
                
                if partner.state !='confirm' : 
                    raise osv.except_osv(_('Error '),
                                        _('No Odoo Id Found For Partner: {}').format(partner.name))
    
                if partner.is_company ==False : 
                    raise osv.except_osv(_('Error'),
                                        _('You Cannot Swap/Migrate Contact Person: {} ').format(partner.name))    
                                    
                if partner.is_company and not partner.child_ids : 
                    raise osv.except_osv(_('Error'),
                                        _('Contact Person Not Found For Partner: {} & Odoo Id: {} \nAdd Contact Person & Continue ')\
                                        .format(partner.name,partner.partner_sequence))
                    
                ##collect data for excle sheet

                data.append([partner.name,partner.partner_sequence,partner.user_id.name,\
                             swap.ind_user_id.name.name if swap.ind_user_id else swap.int_user_id.name.name])
    
            
            if not swap.int_superuser_id and not swap.ind_superuser_id : 
                raise osv.except_osv(_('Error'),_('Select Sale SuperUser  '))
                
            if swap.int_superuser_id : 
                salesuperuser=swap.int_superuser_id.name
            
            elif swap.ind_superuser_id : 
                salesuperuser=swap.ind_superuser_id.name
            
            else : 
                raise osv.except_osv(_('Error'),_('Sale SuperUser Not Found '))
            
            FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
            email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
            if not email_validation :
            #if '@' and '.com' not in FROM_MAIL : 
                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 

            ##check receiver mail addres
            email_validation=partner_obj.email_validation(cr,uid,[salesuperuser.login])
            if not email_validation :
            #if '@' and '.com' not in FROM_MAIL : 
                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Receiver's Email Id \n Contact HR Team"))
                 
    
 
            SUBJECT = '''Partner Swap/Migration Sheet'''    

                             
            MESSAGE = '''Hello {} ,\n\nPFA of swap partner sheet \n\nThanks & Regards \n\n{}
            ''' .format(salesuperuser.name,self.pool.get('res.users').browse(cr,uid,uid).name) 
                                        
             
            #check internet connection 
            
#             connection =check_internet_connection('http://erp.routesms.com')
# 
#             if not connection : 
#                 raise osv.except_osv(_('No Internet Connection'),
#                                     _(' Contact IT Team'))              

            attachment_details=self.generate_attachment(cr,uid,data)
            
                    
            ###get server details
            server=routesms_email_config_obj.get_mailserver_details(cr,SUPERID)
            ###send mail to sale superuser

            notification=routesms_email_config_obj.send_mail(FROM_MAIL, [salesuperuser.login], [],\
                    attachment_details.get('filename'),SUBJECT,MESSAGE,'xlsx',\
                     server,attachment_details.get('binary'),'plain')
            
            
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('ERROR'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
         
        else : 
                    
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team')) 




class swap_bulk_partner(osv.osv):
    _name = 'swap.bulk.partner'
    _description = 'Bulk Swap Partner'
    
    _columns={
              'name':fields.char('Name'),
              'odoo_id':fields.char('Odoo Id'),
              'partner_id':fields.many2one('res.partner','Partner'),
              }


class partner_swap_wizard(osv.osv_memory):

    _name = 'partner.swap.wizard'
    _description = 'Send notification to Account user to swap the partner'


    _columns={
              'int_user_id':fields.many2one('int.user','New Salesperson'),
              'ind_user_id':fields.many2one('ind.user','New Salesperson'),
              'odoo_id':fields.char('Odoo Id'),
              'is_int_user':fields.boolean('International User?'),
              'is_ind_user':fields.boolean('Indian User?'),

              'old_int_user_id':fields.many2one('int.user','Old Salesperson'),
              'old_ind_user_id':fields.many2one('ind.user','Old Salesperson'),

              'old_is_int_user':fields.boolean('Old International User?'),
              'old_is_ind_user':fields.boolean('Old Indian User?'),              
              'send_bulk_request':fields.boolean('Bulk Request'),
              'disable_single_request':fields.boolean('Disable Single Request'),
              'partner_id': fields.many2many('swap.bulk.partner', 'partner_swap_bulk_rel',
                              'partner_swap_wizard_id', 'partner_id', 'Partner'),
              
              }

    _defaults={
             'is_int_user':False,
             'is_ind_user':False,  
             'old_is_int_user':False,  
             'old_is_ind_user':False,  
             'send_bulk_request':False,
             'disable_single_request':False,
               }


    def default_get(self, cr, uid, fields, context):
       
        partner_obj = self.pool.get('res.partner')
        user_obj = self.pool.get('res.users')
        res={}
        
        if user_obj.browse(cr,uid,uid).partner_type =='india' : 
            res.update({'is_ind_user':True,'is_int_user':False,'old_is_ind_user':True,'old_is_int_user':False})
            
        else : 
            res.update({'is_int_user':True,'is_ind_user':False,'old_is_int_user':True,'old_is_ind_user':False})
            

        return res    

    def onchange_bulk_request_int(self,cr,uid,ids,old_user_id,context):
        
        vals={}
        partner_obj=self.pool.get('res.partner')
        int_user_obj=self.pool.get('int.user')
        if old_user_id : 
           
            cr.execute('''delete from swap_bulk_partner ''')
            idss=partner_obj.search(cr,SUPERID,[('user_id','=',int_user_obj.browse(cr,SUPERID,old_user_id).name.id),('is_company','=',True)])
            for partner in partner_obj.browse(cr,SUPERID,idss) : 
                
                self.pool.get('swap.bulk.partner').create(cr,SUPERID,{'name':partner.name,'odoo_id':partner.partner_sequence,'partner_id':partner.id})
            
        return {'value':vals}


    def onchange_remove_partner_ids(self,cr,uid,ids,send_bulk_request,context):
        
        vals={}

        if send_bulk_request : 
            cr.execute('''delete from swap_bulk_partner ''')

        return {'value':vals}
    
    def onchange_bulk_request_ind(self,cr,uid,ids,old_user_id,context):
        
        vals={}
        partner_obj=self.pool.get('res.partner')
        ind_user_obj=self.pool.get('ind.user')
        if old_user_id : 
           
            cr.execute('''delete from swap_bulk_partner ''')
            idss=partner_obj.search(cr,SUPERID,[('user_id','=',ind_user_obj.browse(cr,SUPERID,old_user_id).name.id),('is_company','=',True)])
            for partner in partner_obj.browse(cr,SUPERID,idss) : 
                
                self.pool.get('swap.bulk.partner').create(cr,SUPERID,{'name':partner.name,'odoo_id':partner.partner_sequence,'partner_id':partner.id})
            
        return {'value':vals}
        

    def view_partner_detail(self, cr, uid, ids, context):
        ''' View Customer detail like customer name,email,old bm'''
        
        partner_obj=self.pool.get('res.partner')
        user_obj=self.pool.get('res.users')
        
        if context.get('active_id') : 
            
            swap=self.browse(cr,uid,ids[0]) 
            if not swap.odoo_id : 
                raise osv.except_osv(_('Error'),_('Odoo Id Is Required')) 

            partner_id=partner_obj.search(cr,SUPERID,[('partner_sequence','=',swap.odoo_id)])
            if not partner_id : 
                raise osv.except_osv(_('Error'),_('Odoo Id Does Not Exit\nNo Partner Found '))
            if len(partner_id) > 1 : 
                raise osv.except_osv(_('Error'),_('Duplicate Partner Found '))
            
            partner=partner_obj.browse(cr,SUPERID,partner_id[0])
            
            
            if partner.user_id.partner_type !=user_obj.browse(cr,uid,uid).partner_type : 
                raise osv.except_osv(_('Error'),_('Cannot View Partner Of Other Department'))
            
            raise osv.except_osv(_('Partner Found'),_('Name:%s \nEmail:%s \nOld BM:%s')%(partner.name,partner.email,partner.user_id.name))                       
            
            
    def send_bulk_request_email(self,cr,uid,swap): 
        
        ''' send rewquest in bulk '''
        partner_swap_request_obj=self.pool.get('partner.swap.request.wizard')
        routesms_email_config_obj=self.pool.get('send.email.with.attactment')
        partner_obj=self.pool.get('res.partner')
        data=[]
        
        if not swap.partner_id : 
            raise osv.except_osv(_('Error'),_('No Partner Selected'))
        if swap.old_int_user_id and swap.int_user_id : 
            new_bm=swap.int_user_id.name
            old_bm=swap.old_int_user_id.name
        
        elif swap.old_ind_user_id and swap.ind_user_id :
            new_bm=swap.ind_user_id.name
            old_bm=swap.old_ind_user_id.name
        else : 
            
            raise osv.except_osv(_('Error'),_('Old Salesperson & New Salesperson Are Mandatory !'))
            
        for bulk_partner_rec in swap.partner_id :
             
            data.append([bulk_partner_rec.partner_id.name,bulk_partner_rec.partner_id.partner_sequence,\
                         new_bm.name,bulk_partner_rec.partner_id.user_id.name])
            
        if not data : 
            raise osv.except_osv(_('Error'),_('No Partner Record Found !'))
        
        ###generate xls sheet
        attachment_details=partner_swap_request_obj.generate_attachment(cr,uid,data)
        
        FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
        email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
        if not email_validation :
        #if '@' and '.com' not in FROM_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
             
        
        
        SUBJECT = '''Partner Swap/Migration Bulk Request For Old BM {}'''.format(old_bm.name)    
        
                      
        MESSAGE = '''Hello Accounts Team ,\n\nPFA of partner swap bulk sheet - \n\nThanks & Regards \n\n{}
        ''' .format(self.pool.get('res.users').browse(cr,uid,uid).name) 
         
        #check internet connection 

        connection =check_internet_connection('http://erp.routesms.com')
        #connection =check_internet_connection('182.72.52.19')  
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team'))              
        
        

            
        ###get server details
        server=routesms_email_config_obj.get_mailserver_details(cr,SUPERID)
        
        if old_bm.partner_type=='india' : 
            ###send mail to indian accounting users

            notification=routesms_email_config_obj.send_mail(FROM_MAIL, ['rajendra@routesms.com','india.mis@routesms.com'], [],\
                    attachment_details.get('filename'),SUBJECT,MESSAGE,'xlsx',\
                     server,attachment_details.get('binary'),'plain')

        
            
        elif old_bm.partner_type=='international' : 
            ###send to international users

            notification=routesms_email_config_obj.send_mail(FROM_MAIL, ['asmita.s@routesms.com','sanika.wadekar@routesms.com','krupali.golapkar@routesms.com'], [],\
                    attachment_details.get('filename'),SUBJECT,MESSAGE,'xlsx',\
                     server,attachment_details.get('binary'),'plain')
        else : 
            
            raise osv.except_osv(_('Error'),_('Partner Type Not Set/nContact HR Department !'))            
        
        if notification :
            return True
        
        return False   
    
    def send_swap_mail(self, cr, uid, ids,context):
        ''' Send mail to accounting team about partner swap'''
        
        partner_obj=self.pool.get('res.partner')
        user_obj=self.pool.get('res.users')
        group_obj=self.pool.get('res.groups')
        swap_partner_group_id=89
        
        if context.get('active_id') :
            superuser_ids=[ groupuser.id for groupuser in group_obj.browse(cr,SUPERID,swap_partner_group_id).users]
            swap=self.browse(cr,SUPERID,ids[0])  
            
            ###bulk request
            if swap.send_bulk_request : 
                bulk_request_notification=self.send_bulk_request_email(cr,uid,swap)
                if not bulk_request_notification : 
                    raise osv.except_osv(_('Error'),_('Mail Sending Failed !'))
                return True
            
            ###if not bulk reuqest###
            if swap.is_ind_user and not swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson To Swap')) 
             
            if swap.is_int_user and not swap.int_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson To Swap'))

            if not swap.odoo_id : 
                raise osv.except_osv(_('Error'),_('Odoo Id Is Required'))            
            

            if swap.is_int_user and swap.is_ind_user : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))
            
            if swap.int_user_id and swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))

            if swap.int_user_id:
                if uid not in superuser_ids : 
                    if swap.int_user_id.name.id==uid : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))


            if swap.ind_user_id:
                if uid not in superuser_ids : 
                    if swap.ind_user_id.name.id==uid : 
                        raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))
                    
                
            partner_id=partner_obj.search(cr,SUPERID,[('partner_sequence','=',swap.odoo_id)])
            if not partner_id : 
                raise osv.except_osv(_('Error'),_('Odoo Id Does Not Exit\nNo Partner Found To Swap'))
            if len(partner_id) > 1 : 
                raise osv.except_osv(_('Error'),_('Duplicate Partner Found To Swap'))
            
            partner=partner_obj.browse(cr,SUPERID,partner_id[0])
            
            if swap.int_user_id : 
                if partner.user_id.partner_type !=swap.int_user_id.name.partner_type : 
                    raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate Partner Of Other Department'))
            
            if swap.ind_user_id :
                if partner.user_id.partner_type !=swap.ind_user_id.name.partner_type : 
                    raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate Partner Of Other Department'))            
            
             
                
            if partner.state !='confirm' : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('No Odoo Id Found'))

            if partner.is_company ==False or not partner.child_ids : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('You Cannot Swap/Migrate Contact Person Directly'))

            
            if swap.int_user_id : 
                
                To_Salesperson=swap.int_user_id.name.name
                To_Salesperson_Email=swap.int_user_id.name.login
                
            elif swap.ind_user_id : 
                To_Salesperson=swap.ind_user_id.name.name
                To_Salesperson_Email=swap.ind_user_id.name.login
                
            else:
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))
            
            FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
            email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
            if not email_validation :
            #if '@' and '.com' not in FROM_MAIL : 
                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 

 
            SUBJECT = '''Partner Swap/Migration for "{}" & Odoo Id {}'''.format(partner.name,partner.partner_sequence)    

                             
            MESSAGE = '''Hello Accounts Team ,\n\nKindly swap following Partner - \n\nName : {} \nFrom Salesperson : {}  Email:{} \nTo Salesperson : {}  Email:{}\nOdoo Id : {} \nCompany : {} \n\nThanks & Regards \n\n{}
            ''' .format(partner.name , partner.user_id.name,partner.user_id.login,To_Salesperson,To_Salesperson_Email,\
                        partner.partner_sequence, partner.company_id.name \
                                        ,self.pool.get('res.users').browse(cr,uid,uid).name) 
             
            #check internet connection 
            
            connection =check_internet_connection('http://erp.routesms.com')
            #connection =check_internet_connection('182.72.52.19')  
            if not connection : 
                raise osv.except_osv(_('No Internet Connection'),
                                    _(' Contact IT Team'))              
            
                                                
            
            ###get server details
            
            server=partner_obj.get_mailserver_details(cr,uid)
            if not partner.country_id : 
                raise osv.except_osv(_('Partner Swapping Failed !'), _('No Country Found In Partner \nAssign Country In Partner & Try Again')) 
                
            if partner.user_id.partner_type=='india' :
                ###send mail to indian accounting users
                notification=sendmail(
                    from_addr    = FROM_MAIL,                               
                    to_addr_list = ['rajendra@routesms.com','india.mis@routesms.com'],
                    
                    cc_addr_list = [], 
                    subject      = SUBJECT, 
                    message      = MESSAGE, 
                    login        = server.get('username'), 
                    password     = server.get('password')
                     
                    )                   
                
            elif partner.user_id.partner_type=='international': 
                ###send to international users
                notification=sendmail(
                    from_addr    = FROM_MAIL,                               
                    to_addr_list = ['asmita.s@routesms.com','sanika.wadekar@routesms.com','krupali.golapkar@routesms.com'],
                    
                    cc_addr_list = [], 
                    subject      = SUBJECT, 
                    message      = MESSAGE, 
                    login        = server.get('username'), 
                    password     = server.get('password')
                     
                    )   
            else : 

                raise osv.except_osv(_('Error'),_('Partner Type Not Set/nContact HR Department !'))                                
                
            
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('ERROR'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
         
        else : 
                    
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team')) 



    def send_swap_mail_old(self, cr, uid, ids, context=None):
        ''' Send mail to accounting team about partner swap'''
        
        partner_obj=self.pool.get('res.partner')
        
        if context.get('active_id') : 

            swap=self.browse(cr,uid,ids[0])     
            if swap.is_ind_user and not swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson TO Swap')) 
             
            if swap.is_int_user and not swap.int_user_id : 
                raise osv.except_osv(_('Error'),_('Select Salesperson TO Swap'))
        

            if swap.is_int_user and swap.is_ind_user : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))
            
            if swap.int_user_id and swap.ind_user_id : 
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))

            if swap.int_user_id:
                if swap.int_user_id.name.id==uid : 
                    raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))


            if swap.ind_user_id:
                if swap.ind_user_id.name.id==uid : 
                    raise osv.except_osv(_('Error'),_('Cannot Swap/Migrate To Own Account'))

            
            partner=self.pool.get(context.get('active_model')).browse(cr,uid,context.get('active_id'))
            if partner.state !='confirm' : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('No Odoo Id Found'))

            if partner.is_company ==False or not partner.child_ids : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('You Cannot Swap/Migrate Contact Person Directly'))

            
            if swap.int_user_id : 
                
                To_Salesperson=swap.int_user_id.name.name
                To_Salesperson_Email=swap.int_user_id.name.login
                
            elif swap.ind_user_id : 
                To_Salesperson=swap.ind_user_id.name.name
                To_Salesperson_Email=swap.ind_user_id.name.login
                
            else:
                raise osv.except_osv(_('Error'),_('Technical Issue!/nContact Odoo Team'))
            
            FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
            email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
            if not email_validation :
            #if '@' and '.com' not in FROM_MAIL : 
                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 

 
            SUBJECT = '''Partner Swap/Migration for "{}" & Odoo Id {}'''.format(partner.name,partner.partner_sequence)    

                             
            MESSAGE = '''Hello Accounts Team ,\n\nKindly swap following Partner - \n\nName : {} \nFrom Salesperson : {}  Email:{} \nTo Salesperson : {}  Email:{}\nOdoo Id : {} \nCompany : {} \n\nThanks & Regards \n\n{}
            ''' .format(partner.name , partner.user_id.name,partner.user_id.login,To_Salesperson,To_Salesperson_Email,\
                        partner.partner_sequence, partner.company_id.name \
                                        ,self.pool.get('res.users').browse(cr,uid,uid).name) 
             
            #check internet connection 
            
            connection =check_internet_connection('http://erp.routesms.com')
            #connection =check_internet_connection('182.72.52.19')  
            if not connection : 
                raise osv.except_osv(_('No Internet Connection'),
                                    _(' Contact IT Team'))              
            
                                                
            
            ###get server details
            
            server=partner_obj.get_mailserver_details(cr,uid)

            notification=sendmail(
                from_addr    = FROM_MAIL,                               
                to_addr_list = ['asmita.s@routesms.com'],
                cc_addr_list = [], 
                subject      = SUBJECT, 
                message      = MESSAGE, 
                login        = server.get('username'), 
                password     = server.get('password')
                 
                )                   
            
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('ERROR'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
         
        else : 
                    
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))            
            
               

class wizard(osv.osv_memory):

    _name = 'partner.mail.wizard'
    _description = 'Send notification to Account user to validate the partner'




    def send_mail(self, cr, uid, ids, context=None):
        ''' Send mail to accounting team about partner validation'''
	partner_obj = self.pool.get("res.partner")

        if len(context.get('active_ids'))> 1 :
            raise osv.except_osv(_('Error'),_('Odoo Id Bulk Request Not Allowed'))
         
        if context.get('active_id') :
             
            partner=self.pool.get(context.get('active_model')).browse(cr,uid,context.get('active_id'))
            if partner.state =='confirm' : 
                raise osv.except_osv(_('VALIDATION ERROR'),
                                    _('Partner Is Already Validated'))
   	    #import ipdb;ipdb.set_trace()             
            FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
	    email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
	    if not email_validation :

                raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 
            # check credit type
             
            if partner.prepaid : 
                credit='Prepaid'
             
            else : 
                credit='Postpaid'
 
            SUBJECT = '''Partner Validation "{}" '''.format(partner.name)         
                             
            MESSAGE = '''Hello Accounts Team ,\n\nKindly validate following Partner - \n\nName : {} \nSalesperson : {} \nCredit Type : {} \nCompany : {} \n\nThanks & Regards \n\n{}
            ''' .format(partner.name , partner.user_id.name, credit, partner.company_id.name \
                                        ,self.pool.get('res.users').browse(cr,uid,uid).name) 
             
            #check internet connection 
            
            #connection =check_internet_connection('http://erp.routesms.com')
            connection =check_internet_connection('http://182.72.52.19:8069')  
            if not connection : 
                raise osv.except_osv(_('No Internet Connection'),
                                    _(' Contact IT Team'))              
            
                                                
            
            if not partner.country_id : 
                raise osv.except_osv(_('Error'),_('Assign Country To Partner')) 
                
            
            if partner.country_id.id in [105,255] : 
                ###send email to indian account department
                                   
                notification=sendmail(
                    from_addr    = FROM_MAIL,                               
                    to_addr_list = ['mehrunisha@routesms.com','rajendra@routesms.com','india.mis@routesms.com'],
                    cc_addr_list = [], 
                    subject      = SUBJECT, 
                    message      = MESSAGE, 
                    login        = 'ar@routesms.com', 
                    password     = 'Routesms@05'
                     
                    ) 


            else : 
                ###send email to international account department
                notification=sendmail(
                    from_addr    = FROM_MAIL,                               
                    to_addr_list = ['krupali.golapkar@routesms.com','sanika.wadekar@routesms.com','asmita.s@routesms.com'],
                    cc_addr_list = [], 
                    subject      = SUBJECT, 
                    message      = MESSAGE, 
                    login        = 'ar@routesms.com', 
                    password     = 'Routesms@05'
                     
                    )                   
            #import ipdb;ipdb.set_trace() 
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('ERROR'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
         
        else : 
                    
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))



#            #####################TESTING  PURPOSE##################
#     def send_mail(self, cr, uid, ids, context=None):
#         ''' Send mail to accounting team about partner validation'''
#         
#         if context.get('active_id') :
#             
#             partner=self.pool.get(context.get('active_model')).browse(cr,uid,context.get('active_id'))
#             if partner.state =='confirm' : 
#                 raise osv.except_osv(_('VALIDATION ERROR'),
#                                     _('Partner Is Already Validated'))
#             
#             FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
#             if '@' and '.com' not in FROM_MAIL : 
#                 raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
#                                     _("Invalid Sender's Email Id \n Contact HR Team"))
#                 
#             # check credit type
#             
#             if partner.prepaid : 
#                 credit='Prepaid'
#             
#             else : 
#                 credit='Postpaid'
# 
#             SUBJECT = '''Partner Validation "{}" '''.format(partner.name)         
#                             
#             MESSAGE = '''Hello Accounts Team ,\n\nKindly validate following Partner - \n\nName : {} \nSalesperson : {} \nCredit Type : {} \nCompany : {} \n\nThanks & Regards \n\n{}
#             ''' .format(partner.name , partner.user_id.name, credit, partner.company_id.name \
#                                         ,self.pool.get('res.users').browse(cr,uid,uid).name) 
#             
#             
#             
#             #check internet connection 
#             
#             connection =check_internet_connection('http://erp.routesms.com')  
#             if not connection : 
#                 raise osv.except_osv(_('No Internet Connection'),
#                                     _(' Contact IT Team'))                     
#             notification=sendmail(
#                 from_addr    = 'shazz0020@gmail.com',                               
#                 to_addr_list = ['shazzwazz20@gmail.com'],
#                 cc_addr_list = ['shashank.verma@bistacloud.com'], 
#                 subject      = SUBJECT, 
#                 message      = MESSAGE, 
#                 login        = 'ar@routesms.com', 
#                 password     = 'Rsl@2015'
#                 
#                 ) 
#             
#             if notification :
#                  
#                 return {'type': 'ir.actions.act_window_close'}
#             
#             else :
#                 ''' Sending fail'''
#                 
#                 raise osv.except_osv(_('ERROR'),
#                                     _('Email Sending Failed! \n Contact Odoo Team'))
#         
#         else : 
#                    
#             raise osv.except_osv(_('ERROR'),
#                                 _('Email Sending Failed! \n Contact Odoo Team'))                        
# 
#            
            
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
