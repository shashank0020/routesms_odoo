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
from openerp.routesms_email.routesms_email import *
import re
import requests
import string
import phonenumbers

SUPERUSERID=1
SUPERACCOUNTUSER=[327,321]#sushma & shailesh##

class res_partner(osv.osv):
    _inherit = 'res.partner'


    def browse_list(self):
        '''holds list of all browse objects for resuse code purpose ''' 
        def get_browse_obj(self,func):
            
            ''' get browse object on demand'''
            func.authenticate_obj=self.pool.get('authenticate.users')
            func.hr_obj=self.pool.get('hr.employee')
            func.user_obj=self.pool.get('res.users')
            func.server_obj=self.pool.get('server')
            return func
        
        return get_browse_obj(self,get_browse_obj)

####################API 3 USER CREATION / UPDATING FEATURE STARTS FROM HERE #######################    

    def on_change_server(self, cr, uid, ids, server_id, context=None):
        ''' Allow Add Local Price if server is local'''
        try :
            vals=dict() 
            obj=self.browse_list()
            assert server_id,'Select Server'
            server=obj.server_obj.browse(cr,SUPERUSERID,server_id)
            

#             if server.locality=='local':
#                 vals.update( {'is_local_server': True} )
            
            if server.type=='general' and server.locality =='local':
                vals.update( {'is_manage_subroute' : False,'is_distributor_server': False,'is_local_server':True,'is_reseller_server':False,\
                              'is_route_type':True} )
            if server.type=='general' and server.locality =='international':
                vals.update( {'is_manage_subroute' : False,'is_distributor_server': False,'is_local_server':True,'is_reseller_server':False,\
                              'is_route_type':False} )


            if server.type=='reseller' and server.locality =='international':
                vals.update( {'is_manage_subroute' : False,'is_reseller_server': True,'is_local_server':True,'is_distributor_server':False,\
                              'is_route_type':False} )
            if server.type=='reseller' and server.locality =='local':
                vals.update( {'is_manage_subroute' : True,'is_reseller_server': True,'is_local_server':False,'is_distributor_server':False,\
                              'is_route_type':False} )
            if server.type=='distributor' and server.locality =='international':
                vals.update( {'is_manage_subroute' : False,'is_distributor_server': True,'is_local_server':True,'is_reseller_server':False,\
                              'is_route_type':False} )
            if server.type=='distributor' and server.locality =='local':
                vals.update( {'is_manage_subroute' : True,'is_distributor_server': True,'is_local_server':False,'is_reseller_server':False,\
                              'is_route_type':False} )
            
            return {'value': vals }
        except Exception as E : 
            raise osv.except_osv(_('Error'), _("{}").format(E))


    def user_account_email_notifications(self, cr, uid, user_account_id ,context):
        '''send email notifications for users for user account creation feature '''
        # GET EMAIL SERVER 
         
        routesms_email_config_obj = self.pool.get('send.email.with.attactment')
        server = routesms_email_config_obj.get_mailserver_details(cr, SUPERUSERID)
        
        def notify_user_account_creation(self, cr, uid,): 
            ''' Phase 1 -> Send email to support team |keeping BM in CC when user account created'''
            
            
            
            # GET EMAIL DETAILS 
            FROM_MAIL = user_account_id.partner_id.user_id.login
            email_validation = self.email_validation(cr,uid,[FROM_MAIL])
            assert email_validation,"Invalid Sender's Email Id \n Contact HR Team"
            # TO EMAIL ON BASIS OF USER TYPE - INDIA /INTERNATIONAL
            # IF USER TYPE INTERNATIONAL
            if user_account_id.partner_id.user_id.partner_type == "international" :
                TO_EMAIL = "support@routesms.com"#SUPPORT EMAIL
            # IF USER TYPE INTERNATIONAL
            else : 
                TO_EMAIL = "service.desk@routesms.com"#SUPPORT EMAIL
            
            #TO_EMAIL = "support@routesms.com"#SUPPORT EMAIL
            email_validation = self.email_validation(cr,uid,[TO_EMAIL])
            assert email_validation,"Invalid Sender's Email Id \n Contact HR Team"

            # SET CONTENT FOR EMAIL
            SUBJECT = '''Update Routing For User {}'''.format (user_account_id.username)
            MESSAGE = '''Dear Support Team ,\n\nPlease update routing for following user:\nUsername : {}\nServername : {}\nBM Name : {}\nOdoo Id : {}\nComments : {} \n\nThanks & Regards \n\n{}\n\nNOTE : Email sent via Odoo
            ''' .format(user_account_id.username, user_account_id.server_domain.server, \
                        user_account_id.partner_id.user_id.name, user_account_id.partner_id.partner_sequence,\
                        user_account_id.routesms_notes,user_account_id.partner_id.user_id.name )            
               
            notification=routesms_email_config_obj.send_mail(FROM_MAIL, [TO_EMAIL], [FROM_MAIL],\
                    '',SUBJECT, MESSAGE, '', server, '', 'plain')
            
            assert notification, "Email Sending Failed! \n Contact Odoo Team"
            return "PHASE 1 Email Successfully Sent To Support Team"

        def notifiy_test_to_live(self, cr, uid,): 
            ''' Phase 2 -> Send email to BM when user account pushed from TEST to LIVE'''
            
            # GET EMAIL DETAILS
            FROM_MAIL = "support@routesms.com"#SUPPORT EMAIL
            email_validation = self.email_validation(cr,uid,[FROM_MAIL])
            assert email_validation,"Invalid Sender's Email Id \n Contact HR Team"
            
            TO_EMAIL = user_account_id.partner_id.user_id.login
            email_validation = self.email_validation(cr,uid,[TO_EMAIL])
            assert email_validation,"Invalid Sender's Email Id \n Contact HR Team"
            
            # SET CONTENT FOR EMAIL
            SUBJECT = '''TEST To LIVE For User {}'''.format (user_account_id.username)
            MESSAGE = '''Dear {} ,\n\nYour user account successfuly created:\n\Username : {}\nServername : {}\nBM Name : {}\nOdoo Id : {} \n\nThanks & Regards \n\nSupport Team\\nNOTE : Email sent via Odoo
            ''' .format(user_account_id.partner_id.user_id.name, user_account_id.username, user_account_id.server_domain.server, \
                        user_account_id.partner_id.user_id.name, user_account_id.partner_id.partner_sequence )            
               
            notification=routesms_email_config_obj.send_mail(FROM_MAIL, [TO_EMAIL], [],\
                    '',SUBJECT, MESSAGE, '', server, '', 'plain')
            
            assert notification, "Email Sending Failed! \n Contact Odoo Team"
            return "PHASE 2 Email Successfully Sent To BM"        
                     
        if "user_creation" in context: 
            notify_user_account_creation (self, cr, uid)
             
        elif "test_to_live" in context:   
            notifiy_test_to_live (self, cr, uid )      
            
        return True

        
    def check_employee_hierarchy(self,cr,user_id):
        ''' check manager of log in employee'''
        obj=self.browse_list()
        BM,TL,DS,CEO,BOD='Business Manager','Team Leader','Director Sales','CEO','BOD'
        
        emp= [ emp_record for  emp_record in obj.hr_obj.browse(cr,SUPERUSERID,\
                    obj.hr_obj.search(cr,SUPERUSERID,[('user_id','=',user_id.id)])  )    ]
        
        assert emp,'No Employee Record Found\nContact HR Department'
        assert len(emp)==1,'Multiple Employee Record Found\nContact HR Department'
        
        uid_user_type=user_id.type
        assert uid_user_type,'Login User Type Not Found\nContact HR Department\nLog In User Type Should \
        Be Either India or International'
        
        employee=emp[0]
        ''' check Login User Manager. Mangager is Mandatory'''
        if employee.job_id.name != BOD : 
            assert employee.parent_id,'User Creation Failed\nNo Manager Found For {}\nContact HR Department'\
            .format(user_id.name)


        assert employee.job_id,'User Creation Failed\nJob Title Not Found For {}\nContact HR Department'\
        .format(user_id.name)
        
        '''Case 1: If Login User is  Business Manager'''
        
        if employee.job_id.name==BM : 
            ###Validate TL######

            assert employee.parent_id.job_id,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            Job Title Not Assigned To Your TL: {} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: Team Leader'\
            .format(employee.parent_id.name)

            
            assert employee.parent_id.job_id.name==TL,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            \nYour Job Title: {}\n \
            Your Manager"s Job Title: {} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: Team Leader'\
            .format(employee.job_id.name,employee.parent_id.job_id.name)

            TL_login_type=employee.parent_id.user_id.type
            assert TL_login_type,'Your Manager"s :{} Login User Type Not Found\nContact HR Department\nLog In User Type Should \
        Be Either India or International'.format(employee.parent_id.user_id.name)
        
            assert TL_login_type==uid_user_type,'Your Login Type:{}\n \
            Your TL Login Type: {}\n \
            Contact HR Department\nLogin Type Must Be Equivalent'\
            .format(uid_user_type,TL_login_type)
            
            
            ####Validate DOS####
            assert employee.parent_id.parent_id,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            \n Director Sales Not Found For Your TL: {}\n \
            \nContact HR Department'.format(employee.parent_id.name)

            assert employee.parent_id.parent_id.job_id,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            Job Title Not Assigned To Your TL"s Manager: {} \nContact HR Department\n \
            Your TL"s Manager Job Title Must Be: Director Sales'\
            .format(employee.parent_id.parent_id.name)

            
            assert employee.parent_id.parent_id.job_id.name==DS,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            \nYour TL Job Title: {}\n \
            Your TL"s Manager Job Title: {} \nContact HR Department\n \
            TL"s Manager Job Title Must Be: Director Sales'\
            .format(employee.parent_id.job_id.name,employee.parent_id.parent_id.job_id.name)

            DS_login_type=employee.parent_id.parent_id.user_id.type
            assert DS_login_type,'Your DS  :{} Login User Type Not Found\nContact HR Department\nLog In User Type Should \
        Be Either India or International'.format(employee.parent_id.parent_id.user_id.name)
        
            assert DS_login_type==uid_user_type,'Your Login Type:{}\n \
            Your TL Login Type: {}\n \
            Your DS Login Type: {}\n \
            Contact HR Department\nLogin Type Must Be Equivalent'\
            .format(uid_user_type,TL_login_type,DS_login_type)
            
        
        elif employee.job_id.name==TL : 
            ###Validate DOS######
            assert employee.parent_id.job_id,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            Job Title Not Assigned To Your Manager : {} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: Director Sales'\
            .format(employee.parent_id.name)

            
            assert employee.parent_id.job_id.name==DS,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            \nYour Job Title: {}\n \
            Your Manager"s Job Title: {} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: Director Sales'\
            .format(employee.job_id.name,employee.parent_id.job_id.name)

            DS_login_type=employee.parent_id.user_id.type
            assert DS_login_type,'Your DS :{} Login User Type Not Found\nContact HR Department\nLog In User Type Should \
        Be Either India or International'.format(employee.parent_id.user_id.name)
        
            assert DS_login_type==uid_user_type,'Your Login Type:{}\n \
            Your DS {} Login Type: {}\n \
            Contact HR Department\nLogin Type Must Be Equivalent'\
            .format(uid_user_type,employee.parent_id.user_id.name,DS_login_type)
            

        elif employee.job_id.name==DS : 
            ###Validate BOD######
            assert employee.parent_id.job_id,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            Job Title Not Assigned To Your Manager :{} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: BOD'\
            .format(employee.parent_id.name)

            
            assert employee.parent_id.job_id.name==BOD,\
            'User Creation Failed Due Invalid Employee Hierarchy\n \
            \nYour Job Title: {}\n \
            Your Manager"s Job Title: {} \nContact HR Department\n \
            Your Manager"s Job Title Must Be: BOD'\
            .format(employee.job_id.name,employee.parent_id.job_id.name)

            BOD_login_type=employee.parent_id.user_id.type
            assert BOD_login_type,'Your Manager"s :{} Login User Type Not Found\nContact HR Department\nLog In User Type Should \
        Be Either India or International'.format(employee.parent_id.user_id.name)
        
            assert BOD_login_type==uid_user_type,'Your Login Type:{}\n \
            Your Manager"s {} Login Type: {}\n \
            Contact HR Department\nLogin Type Must Be Equivalent'\
            .format(uid_user_type,employee.parent_id.user_id.name,BOD_login_type)

        elif employee.job_id.name==BOD : 
            assert not employee.parent_id, "No Manager Should Be Assigned To BOD"

        else :
            raise osv.except_osv(_("Error!"), _("You Do Not Have Authority To\nYour Job Title Must Be Under\
            Following:\n{}\nContact HR Department ").format(str ( [BM,TL,DS] ) ) )
            
        return employee
    
    def onchange_od_limit(self,cr,uid,ids ,od_limit,postpaid,context):
        ''' od limit and credit limit will be same if account is postpaid'''
        try :
            
            res={'credit_limit':0.0}
            
            assert od_limit and od_limit>0,'Invalid OD Limit'
            
            if postpaid :
                res.update({'credit_limit':od_limit})
            return {'value':res}
        except Exception as E :
            raise osv.except_osv(_("Error!"), _("{}").format(E.message))
    
#     def decorate_me(func):
#         '''My 1st decorator  '''
#         import ipdb;ipdb.set_trace()
#         def closure(self,user_line,mode,employee):

#             employee=self.check_employee_hierarchy(user_line.partner_id.user_id)
#             return func(user_line,mode,employee)
#         return closure
    

    def decorate_me(self,cr,user_line): 
        '''Do something before sending form for approval '''
        employee=self.check_employee_hierarchy(cr,user_line.partner_id.user_id)
        return employee
        
        

    def send_for_approval(self,cr,user_line,mode): 
        ''' send request for approval'''
        
        obj=self.browse_list()
        employee=self.decorate_me(cr,user_line)
        assert employee,'Employee Record Not Found'
        
        if mode=='create'  :
            
            vals=dict(creation_date=user_line.create_date,name=user_line.partner_id.name,type='pending',\
                      odoo_id=user_line.partner_id.partner_sequence,partner_id=user_line.partner_id.id,\
                      business_manager = user_line.partner_id.user_id.id,\
                      user_obj=user_line.id,user_name=user_line.username,server=user_line.server_domain.id,\
                      local_price=user_line.local_price,od_limit=user_line.od_limit,\
                      reseller_code = user_line.reseller_code,distributor_code = user_line.distributor_code,\
                      route_type = user_line.route_type,routesms_notes = user_line.routesms_notes,\
                      is_local_server = user_line.is_local_server,\
                      account_type='prepaid' if user_line.partner_id.prepaid else 'postpaid',
                      credit_limit=user_line.credit_limit,user_id=employee.parent_id.user_id.id or employee.user_id.id,\
                      employee_id=employee.parent_id.id or employee.id,create_record=True,\
                      is_active = user_line.is_active,agreement = user_line.agreement,\
                      commercial_name_phone = user_line.commercial_name_phone,\
                      commercial_email = user_line.commercial_email ,\
                      price_notification_name_phone = user_line.price_notification_name_phone,\
                      price_notification_email = user_line.price_notification_email,\
                      account_name_phone = user_line.account_name_phone,\
                      account_email = user_line.account_email, technical_name_phone = user_line.technical_name_phone,\
                      technical_email = user_line.technical_email, user_email_temp = user_line.user_email_temp,\
                      user_account_phone_number = user_line.user_account_phone_number,\
                      manage_subroute = user_line.manage_subroute.id,)
            
        elif mode=='update' :
            vals=dict(creation_date=user_line.create_date,updation_date=fields.datetime.now(),name=user_line.partner_id.name,type='pending',\
                      odoo_id=user_line.partner_id.partner_sequence,partner_id=user_line.partner_id.id,\
                      business_manager = user_line.partner_id.user_id.id,\
                      user_obj=user_line.id,user_name=user_line.username,server=user_line.server_domain.id,\
                      local_price=user_line.local_price,od_limit=user_line.od_limit,\
                      reseller_code = user_line.reseller_code,distributor_code = user_line.distributor_code,\
                      route_type = user_line.route_type,routesms_notes = user_line.routesms_notes,\
                      is_local_server = user_line.is_local_server,\
                      account_type='prepaid' if user_line.partner_id.prepaid else 'postpaid',
                      credit_limit=user_line.credit_limit,user_id=employee.parent_id.user_id.id or employee.user_id.id,\
                      employee_id=employee.parent_id.id or employee.id,create_record=True,\
                      is_active = user_line.is_active,agreement = user_line.agreement,\
                      commercial_name_phone = user_line.commercial_name_phone,\
                      commercial_email = user_line.commercial_email ,\
                      price_notification_name_phone = user_line.price_notification_name_phone,\
                      price_notification_email = user_line.price_notification_email,\
                      account_name_phone = user_line.account_name_phone,\
                      account_email = user_line.account_email, technical_name_phone = user_line.technical_name_phone,\
                      technical_email = user_line.technical_email, user_email_temp = user_line.user_email_temp,\
                      user_account_phone_number = user_line.user_account_phone_number,\
                      manage_subroute = user_line.manage_subroute.id, )  
             
        else :
            raise osv.except_osv(_("Error"), _("Invalid Mode\nContact Odoo Team"))
        
        
        obj.authenticate_obj.create(cr,SUPERUSERID,vals)
        print 'USER ADDED & FORM SENT TO MANAGER FOR APPROVAL'

    
    def post_data_to_server_old(self,vals):
        '''add users '''

        post_data = vals
        url='http://192.168.0.13/odoo/' #Local
        #url='http://121.241.242.102/odoo/' #Live
        try : 
            
            post_response = requests.post(url=url, data=post_data)
        #raise osv.except_osv(_('Error!'), _("REQUEST =%s .\n\n\nRESPONSE=%s") % (post_data,post_response.text))
 
        except Exception as E : 
            raise osv.except_osv(_('Error !'), _('Connection To Server Failed !!'))
#                                 
        return post_response.text         

    def restict_user_to_add_update_user_account(self,cr,uid,user_id): 
        '''Restrict User to Add/Update User '''
        
        assert uid==user_id.id,'You Are Not The Business Manager Of This Partner'
        return True

    def validate_server_fields_during_update(self,cr, uid ,partner ) : 
        '''Check values during modifying user details '''
        
        # COMMON FOR ALL
        #assert not partner.routesms_notes, "Comments Cannot Be Modified"
        
        # CASE 1: GENERAL->  INTERNATIONAL
       
        if partner.server.type=='general' and partner.server.locality =='international': 
            pass
        # CASE 2: GENERAL-> LOCAL 
        elif partner.server.type=='general' and partner.server.locality =='local': 
            assert not partner.route_type,'You Cannot Modify Route Type'
           
        
        #CASE 3: RESELLER ->  INTERNATIONAL
        elif partner.server.type=='reseller' and partner.server.locality =='international': 
            assert not partner.reseller_code,'You Cannot Modify Reseller Code'
        
        #CASE 4: RESELLER ->  LOCAL
        elif partner.server.type=='reseller' and partner.server.locality =='local': 
            assert not partner.reseller_code,'You Cannot Modify Reseller Code'

            
        #CASE 5: DISTRIBUTOR ->  INTERNATIONAL
        elif partner.server.type=='distributor' and partner.server.locality =='international': 
            assert not partner.distributor_code,'You Cannot Modify Distributor Code'
             
        #CASE 6: DISTRIBUTOR ->  LOCAL
        elif partner.server.type=='distributor' and partner.server.locality =='local': 
            assert not partner.distributor_code,'You Cannot Modify Distributor Code'
        
        else : 
            raise osv.except_osv(_('Error'), _('Technical Issue\nContact Odoo Team'))
        
    def restore_user_detail(self, cr, uid, user_account_id):
        ''' restore previous user detail like prices'''
        
        assert user_account_id.user_line_restore, "No Mapping Found For Restoring User Account Previous Session"
        restore = user_account_id.user_line_restore
        # RESTORE PREVIOUS SESSION OF USER ACCOUNT
        user_account_id.write( {
                                
        "status" : restore.status,"approved_by_name" : restore.approved_by_name,\
        "local_price" : restore.local_price, "od_limit" : restore.od_limit,"credit_limit" : restore.credit_limit,\
        "route_type" : restore.route_type, "is_local_server" : restore.is_local_server, "is_active" : restore.is_active,\
        "update_date" : restore.update_date,\
        "commercial_name_phone" : restore.commercial_name_phone ,  "commercial_email" :  restore.commercial_email,\
        "price_notification_name_phone" : restore.price_notification_name_phone, "price_notification_email" : restore.price_notification_email,\
        "account_name_phone" : restore.account_name_phone ,  "account_email" :  restore.account_email,\
        "technical_name_phone" : restore.technical_name_phone ,  "technical_email" :  restore.technical_email,\
        "user_account_phone_number" : restore.user_account_phone_number,"manage_subroute" : restore.manage_subroute.id
        
        })
        
        user_account_id.approved_by = [ restore.approved_by]
        # DELETE PREVIOUS SESSION ROW
        return user_account_id.user_line_restore.unlink ()


    def unlink_restore_user_detail_directly(self, cr, uid, user_account_id ):
        ''' remove restore previous user detail like prices'''

        return user_account_id.user_line_restore.unlink ()        
        
    
    def user_factory_restore(self, cr, uid, user_account_id): 
        '''store user account data for restoring if updated user request rejected '''
        
        # COPY DATA FROM ONE TABLE AND INSERT INTO OTHER FOR RESTORING DATA WHEN REQUIRED 
        insert_to_restore_table_query = ''' INSERT INTO res_partner_add_user_restore (create_uid, create_date, server_domain, write_uid,write_date, partner_id, is_live, credit_limit, od_limit, status, update_date, approved_by_name, username, local_price, reseller_code, routesms_notes, distributor_code, route_type, is_local_server, is_active, commercial_name_phone, commercial_email, price_notification_name_phone, price_notification_email, account_name_phone, account_email, technical_name_phone, technical_email,user_account_phone_number,manage_subroute,agreement) \
        SELECT create_uid, create_date, server_domain, write_uid,write_date, partner_id, is_live, credit_limit, od_limit, status, update_date, approved_by_name, username, local_price, reseller_code, routesms_notes, distributor_code, route_type, is_local_server, is_active, commercial_name_phone, commercial_email, price_notification_name_phone, price_notification_email, account_name_phone, account_email, technical_name_phone, technical_email,user_account_phone_number,manage_subroute,agreement FROM res_partner_add_user where id = {} RETURNING id '''.format( \
                                          user_account_id.id,  )
        cr.execute ( insert_to_restore_table_query )
        return_id = cr.fetchone ()
        
#         approved_user_many2many = '''INSERT INTO approved_by_users_restore_rel (add_users_id, users_id)\
#         SELECT add_users_id, users_id FROM approved_by_users_rel where add_users_id = {} '''.format(user_account_id.id)
#         import ipdb;ipdb.set_trace()
#         cr.execute ( approved_user_many2many )
    
        # MAP NEW ROW ID TO OLD TABLE
        return cr.execute (''' update res_partner_add_user_restore set res_partner_add_user_id = %s where id = %s''',\
                    ( user_account_id.id,return_id[0] ))
         


    def button_updating_user(self,cr,uid,ids,context):
        '''update users '''
        #raise osv.except_osv(_('Error'), _('THIS FEATURE WILL BE UNLOCKED SOON'))
        return self.button_adding_user(cr,uid,ids,context) 
        
        
    
    def validate_pricing(self,cr,uid,partner):
        '''validate price as per buisness flow '''
        credit_limit=0.0
        
        assert  partner.od_limit >= 0.0,'Invalid OD Limit Amount\nOD Limit Must Be Greater Than 0.0'

        if partner.server.type not in ["reseller", "distributor"] and partner.server.locality != "local" :
            
            assert partner.local_price > 0.0,'Local Price Should Be Always Greater Than 0.0'
        if partner.postpaid : 
            credit_limit = partner.od_limit 
        return credit_limit

    def check_server_code_real_time(self,cr, uid, **post_vals ): 
        ''' Check reseller and distributor code on real time and if code exist on rsl server throw exception'''
        api_obj = self.pool.get("odoo.rsl.api")
        response = api_obj.check_user_account_code (cr, uid, [],post_vals )
        if response != '"SUC_607"'  :
            raise osv.except_osv(_('Error'), _('Code Already Exist'))
        return True            
        
        
    def validate_values_per_server(self,cr,uid,partner,context): 
        '''validate server fields '''
        
        # THROW EXCEPTION IF USER ACCOUNT ALREADY CREATED
        # ONLY APPLICABLE WHILE CREATING USER/IGNORED DURING UPDATION
        val_line={}
        if context.get('mode')!='update' : 
            # RESTRICT TO DEACTIVE USER ACCOUNT DURING CREATION
            assert partner.is_active , "User Account Cannot Be Deactivated During Creation"
            val_line['is_active'] = True
            
            cr.execute('''select id from res_partner_add_user where username=%s ''',(partner.add_user,))
            user_list=map(lambda x:x[0],cr.fetchall()) 
            assert not user_list,'UserName Already Exist'

                
            # CASE 1: GENERAL->  INTERNATIONAL
            if partner.server.type=='general' and partner.server.locality =='international': 
                pass
            # CASE 2: GENERAL-> LOCAL 
            elif partner.server.type=='general' and partner.server.locality =='local': 
                assert partner.route_type,'Select Route Type'
                val_line['route_type'] = partner.route_type
            
            #CASE 3: RESELLER ->  INTERNATIONAL
            elif partner.server.type=='reseller' and partner.server.locality =='international': 
                assert partner.reseller_code,'Enter Reseller Code'
                assert len(partner.reseller_code) == 4,'Reseller Code Must Be 4 Digits'
                cr.execute('''select id from res_partner_add_user where reseller_code=%s ''',(partner.reseller_code,))
                user_list=map(lambda x:x[0],cr.fetchall())
                assert not user_list,'Reseller Code Already Exist'
                self.check_server_code_real_time(cr, uid, servername = partner.server.name, code = partner.reseller_code)

                val_line['reseller_code'] = partner.reseller_code
            
            #CASE 4: RESELLER ->  LOCAL
            elif partner.server.type=='reseller' and partner.server.locality =='local': 
                assert partner.reseller_code,'Enter Reseller Code'
                assert len(partner.reseller_code) == 4,'Reseller Code Must Be 4 Digits'
                cr.execute('''select id from res_partner_add_user where reseller_code=%s ''',(partner.reseller_code,))
                user_list=map(lambda x:x[0],cr.fetchall())
                assert not user_list,'Reseller Code Already Exist'
                self.check_server_code_real_time(cr, uid, servername = partner.server.name, code = partner.reseller_code)

                val_line['reseller_code'] = partner.reseller_code
                
            #CASE 5: DISTRIBUTOR ->  INTERNATIONAL
            elif partner.server.type=='distributor' and partner.server.locality =='international': 
                assert partner.distributor_code,'Enter Distributor Code'
                assert len(partner.distributor_code) == 4,'Distributor Code Must Be 4 Digits'
                cr.execute('''select id from res_partner_add_user where distributor_code=%s ''',(partner.distributor_code,))
                user_list=map(lambda x:x[0],cr.fetchall())
                assert not user_list,'Distributor Code Already Exist'
                self.check_server_code_real_time(cr, uid, servername = partner.server.name, code = partner.distributor_code)

                val_line['distributor_code'] = partner.distributor_code
                 
            #CASE 6: DISTRIBUTOR ->  LOCAL
            elif partner.server.type=='distributor' and partner.server.locality =='local': 
                assert partner.distributor_code,'Enter Distributor Code'
                assert len(partner.distributor_code) == 4,'Distributor Code Must Be 4 Digits'
                cr.execute('''select id from res_partner_add_user where distributor_code=%s ''',(partner.distributor_code,))
                user_list=map(lambda x:x[0],cr.fetchall())
                assert not user_list,'Distributor Code Already Exist'  
                self.check_server_code_real_time(cr, uid, servername = partner.server.name, code = partner.distributor_code)

                val_line['distributor_code'] = partner.distributor_code          
            
            else : 
                raise osv.except_osv(_('Error'), _('Technical Issue\nContact Odoo Team'))
        
        else : 
                # CASE 2: GENERAL-> LOCAL 
                if partner.server.type=='general' and partner.server.locality =='local': 
                    if partner.route_type  :
                        val_line['route_type'] = partner.route_type
                
                # USER ACCOUNT ACTIVE OR NOT DURING UPDATING
                val_line['is_active'] = partner.is_active
        
        return val_line 


    def onchange_user_account(self,cr, uid, ids, user, context):
        ''' Fetch User Account detail during updation'''
        commercial = self.pool.get('commercial')
        price_notification = self.pool.get('price.notification')
        account = self.pool.get('account')
        technical = self.pool.get('technical')      
        for_emails = ["" for x in range(4) ]
        for_name_phone = ["" for x in range(2) ]
        commercial_email, price_notification_email, account_email, technical_email = for_emails
        
        commercial_name, commercial_phone = for_name_phone
        price_notification_name, price_notification_phone = for_name_phone
        account_name, account_phone = for_name_phone
        technical_name, technical_phone = for_name_phone  
        #import ipdb;ipdb.set_trace()     
        try :
            res={}
            if user : 
                partner = self.browse(cr, uid, context.get("active_id") )
                for user_rec in partner.user_line : 
                    if user ==  user_rec.username  :
                        # GET EMAILS OF USER ACCOUNT DURING UPDATING
                        
                        if user_rec.commercial_email : 
                            commercial_email = [(6, 0,  commercial.search (cr, uid, [("email", "in", user_rec.commercial_email.split(',') )])  )]

                        if user_rec.price_notification_email :
                            price_notification_email = [(6, 0,  price_notification.search (cr, uid, [("email", "in", user_rec.price_notification_email.split(',') )])  )] 
                            
                        if user_rec.account_email : 
                            account_email = [(6, 0,  account.search (cr, uid, [("email", "in", user_rec.account_email.split(',') )])  )]
                        
                        if user_rec.technical_email : 
                            technical_email =[ (6, 0,  technical.search (cr, uid, [("email", "in", user_rec.technical_email.split(',') )])  )]
                        
                        

                        
                        # GET NAMES & PHONE OF USER ACCOUNT DURING UPDATING
                        if user_rec.commercial_name_phone : 
                            commercial_name, commercial_phone = user_rec.commercial_name_phone.split('/') 
                            
                        if user_rec.price_notification_name_phone  : 
                            price_notification_name, price_notification_phone = user_rec.price_notification_name_phone.split('/')
                        
                        if user_rec.account_name_phone :
                            account_name, account_phone = user_rec.account_name_phone.split('/') 
                            
                        if user_rec.technical_name_phone : 
                            technical_name, technical_phone = user_rec.technical_name_phone.split('/')
                    
                        
                        res.update({'credit_limit' : user_rec.credit_limit, 'od_limit' : user_rec.od_limit ,\
                        'local_price' : user_rec.local_price , 'routesms_notes' : user_rec.routesms_notes,\
                        'is_active' : user_rec.is_active, 'user_email_temp' : user_rec.user_email_temp,\
                        'commercial_name' : commercial_name, 'commercial_phone' : commercial_phone, 'commercial_email' : commercial_email,\
                        'price_notification_name' : price_notification_name, 'price_notification_phone' : price_notification_phone, 'price_notification_email' : price_notification_email,\
                        'account_name' : account_name,'account_phone' : account_phone, 'account_email' : account_email,\
                        'technical_name' : technical_name,'technical_phone' : technical_phone, 'technical_email' : technical_email,\
                        'user_account_phone_number'  :user_rec.user_account_phone_number,\
                        'manage_subroute' : user_rec.manage_subroute,'agreement' : user_rec.agreement,
                        })

                        break
            
            return {'value':res}
        except Exception as E : 
            raise osv.except_osv(_("Error!"), _("{}").format(E.message))

    def user_account_email_config(self,cr, uid ,partner ): 
        '''add name and phone for commercial,pricing,accounts,techincal '''
        vals ={}
        
        # COMMERCIAL
        commercial_name_phone = partner.commercial_name + '/' + partner.commercial_phone
        
        commercial_email = ','.join ( [ commercial.email for commercial in partner.commercial_email ] ) 
        # PRICE NOTIFICATION
        price_notification_name_phone = partner.price_notification_name + '/' + partner.price_notification_phone  
        price_notification_email = ','.join ( [ price_notification.email for price_notification in partner.price_notification_email ] )     
        # ACCOUNTS
        account_name_phone = partner.account_name + '/' + partner.account_phone        
        account_email = ','.join ( [ account.email for account in partner.account_email ] )
        # TECHINCAL
        technical_name_phone = partner.technical_name + '/' + partner.technical_phone
        technical_email = ','.join ( [technical.email for technical in partner.technical_email ] )
        
        
        vals.update ( {"commercial_name_phone" :commercial_name_phone, "commercial_email" : commercial_email,\
        "price_notification_name_phone" : price_notification_name_phone, "price_notification_email" : price_notification_email,\
        "account_name_phone" : account_name_phone, "account_email" : account_email,\
        "technical_name_phone" : technical_name_phone, "technical_email" : technical_email   } )  
        return vals      
        
        

    def validate_phone_number (self,phone_numbers): 
        '''check phone number valid or not '''
        
        try : 
            for phone_number in phone_numbers : 
                number_format = phonenumbers.parse(phone_number, None)
                
                #assert phonenumbers.is_valid_number(number_format)
        except Exception as E : 
            
            raise osv.except_osv(_("Error "), _("Invalid Phone Number : {} ").format(phone_number))  

    def check_email_limit(self, email_lists) : 
        '''Email creation limit <=5 '''
        
        for email_key in  email_lists.keys () : 
            
            assert len(email_lists [email_key] ) <= 5, "You Cannot Assign More Than 5 Email Addresses for {}".format(email_key)
    
        
        return True        
         

            
    def action_manage_subroute(self, cr, uid, ids, context=None): 
        ''' manage subroute of india reseller and india distributor'''
        
        partner = self.browse(cr, uid, ids[0] )
        
        id = partner.manage_subroute and partner.manage_subroute.id or False
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'routesms', 'view_routesms_subroute_form')
        view_id = view_ref and view_ref[1] or False,
        #import ipdb;ipdb.set_trace()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Manage Subroute'),
            'res_model': 'subroute',
            'res_id': id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }

    def assertions(self, cr ,uid, partner, context ):
        '''validate before adding/updating  user account '''

        assert partner.state=='confirm','Odoo Id Not Found'
        assert partner.user_id,'Salesperson Not Found'
        assert partner.add_user,'Enter User Name'            
        assert uid!=SUPERUSERID,'User Cannot Be Added With Odoo SuperAdmin Account'
        assert partner.server,'Select Server'
        assert partner.child_ids, "Contact Person Not Found\nAdd New Contact Person"
        assert partner.agreement, "Please Select Agreement"
        assert partner.add_user.isalnum(), "Invalid UserName"
#         assert partner.user_email_temp, "Enter User Email"
#         valid_email =self.email_validation (cr, uid, [partner.user_email_temp] )
#         assert  valid_email, "Invalid User Email"
 
        # commercial 
        assert partner.commercial_name , "Enter Commercial Name"
        assert partner.commercial_phone , "Enter Commercial Phone"
        assert partner.commercial_email , "Enter Commercial Email"
        

        # PRICE NOTIFICATION
        assert partner.price_notification_name , "Enter Price Notification Name"
        assert partner.price_notification_phone , "Enter Price Notification Phone"
        assert partner.price_notification_email , "Enter Price Notification Email"  

        # ACCOUNTS 
        assert partner.account_name , "Enter Account Name"
        assert partner.account_phone , "Enter Account Phone"
        assert partner.account_email , "Enter Account Email"   

        # TECHNICAL 
        assert partner.technical_name , "Enter Technical Name"
        assert partner.technical_phone , "Enter Technical Phone"
        assert partner.technical_email , "Enter Technical Email"
        
        #PER USER PHONE NUMBER
        assert partner.user_account_phone_number, "Enter Phone Number"
        phone_list = [partner.commercial_phone, partner.price_notification_phone,\
                                    partner.account_phone, partner.technical_phone,partner.user_account_phone_number]

        
        email_list = {"Commerical" :  partner.commercial_email, "Price Notification" : partner.price_notification_email,\
         "Account" :  partner.account_email, "Technical" : partner.technical_email}
        
        self. validate_phone_number(phone_list)
        self. check_email_limit(email_list)
        

        return True
    
    def check_user_configuration(self, cr, uid, partner, context) : 
        ''' check configuration of login user to create user account
        Check user priviledges'''
        user_settings_obj=self.pool.get('user.settings')
        user_setting_id=user_settings_obj.search(cr,SUPERUSERID,[('user_id','=',partner.user_id.id)])
        assert user_setting_id,'Your Account Is Not Registered To Add Users \nContact Administrator'
        assert len(user_setting_id)==1,'Multiple User Settings Found \nContact Administrator'
        if context.get('mode')!="update" : 
                
            if partner.user_line :
                system_user_count=user_settings_obj.browse(cr,SUPERUSERID,user_setting_id[0]).count
                assert system_user_count,'Add User Configuration Missing\nContact Administrator'
                assert len(partner.user_line)!= system_user_count,'You Cannot Add User More Than {} \nContact Administrator'.format(system_user_count)
        
        return True

    def button_adding_user(self,cr,uid,ids,context): 
#        raise osv.except_osv(_('Error'), _('THIS FEATURE WILL BE UNLOCKED SOON'))
        user_line_obj=self.pool.get('res.partner.add.user')
        
        vals={}
        vals_line={}
        try : 
            
            partner=self.browse(cr,uid,ids[0])
            # Do Not Allow Other user to create /update user account
            self.restict_user_to_add_update_user_account(cr,uid,partner.user_id)
            # Validate before adding /updating user account
            self.assertions(cr, uid, partner ,context)
            
            # Check user account creation configuration per odoo user
            self.check_user_configuration(cr, uid, partner, context)
            
            # VALIDATE FIELD VALUES AS PER SERVERS
            vals_line=self.validate_values_per_server(cr,uid,partner,context)
            # VALIDATE PRICING
            credit_limit=self.validate_pricing(cr,uid,partner)
            # CONCAT USER commercial ,PRICING,ACCOUNTS,TECHINCAL name & phone
            concat_vals_line= self.user_account_email_config (cr, uid, partner)
            ########update user######################## 
            
            if context.get('mode')=='update' :
                #user_to_update=[user for user in partner.user_line if user.username==partner.add_user and user.server_domain.id == partner.server.id]
                user_to_update=[user for user in partner.user_line if user.username==partner.add_user ]
#                 assert user_to_update,'User Does Not Exist For Update\nUserName and Server \
#                 Must Be Equivalent For Modifying User Record'
                assert user_to_update,'User Does Not Exist For Update'                
                assert user_to_update[0].status=='approved','You Cannot Update Pending User'
                # VERFIY VALUES INSERTED ON  SERVER LEVEL & THROW EXCEPTION AS PER FLOW
                self.validate_server_fields_during_update(cr, uid , partner)
                vals_line.update({'update_date':fields.datetime.now(),'partner_id':partner.id,\
                'local_price':partner.local_price,'od_limit':partner.od_limit,\
                'credit_limit':credit_limit,'status':'pending','approved_by':[(5, 0)],\
                'approved_by_name':'', 'routesms_notes' : partner.routesms_notes,'user_email_temp' : partner.user_email_temp,\
                'user_account_phone_number' : partner.user_account_phone_number,\
                'manage_subroute' : partner.manage_subroute.id, 'agreement' : partner.agreement, 
                })
                
                user_line_id = user_line_obj.browse(cr,SUPERUSERID,user_to_update[0].id)
                # STORE CURRENT USER DETAILS BEFORE UPDATING LIKE PRICING
                self.user_factory_restore(cr, uid, user_line_id)
                # COMBINE 2 DICTIONARY 
                vals_line_combine = dict (vals_line.items() + concat_vals_line.items() )                
                user_line_obj.write(cr,uid,[user_line_id.id],vals_line_combine)
                
                self.send_for_approval(cr,user_line_id,'update')
                
            else : 
                
                # Create user on odoo
                
                vals_line.update({'username':partner.add_user,'server_domain':partner.server.id,\
                'partner_id':partner.id,'local_price':partner.local_price,'od_limit':partner.od_limit,\
                'credit_limit':credit_limit,'status':'pending', 'routesms_notes':partner.routesms_notes,\
                'is_local_server' : partner.is_local_server,'user_email_temp' : partner.user_email_temp,\
                'user_account_phone_number' : partner.user_account_phone_number,\
                'manage_subroute' : partner.manage_subroute.id, 'agreement' : partner.agreement,
                })

                # COMBINE 2 DICTIONARY 
                vals_line_combine = dict (vals_line.items() + concat_vals_line.items() )                
                user_line_id=user_line_obj.create(cr,uid,vals_line_combine)
                user_line = user_line_obj.browse(cr,SUPERUSERID,user_line_id)
                self.send_for_approval(cr, user_line, 'create')
            
            
            
            # Wipe out all records filled early
            
            vamp={'add_user':'','server':False,'local_price':0.0,'od_limit':0.0,'credit_limit':0.0,\
                    'route_type':False, 'reseller_code':'', 'distributor_code':'', 'routesms_notes':'',\
                    'is_local_server' : False, 'is_reseller_server' : False, 'is_distributor_server' : False,\
                    'is_route_type' : False ,'is_manage_subroute' : False,'manage_subroute' : False,'commercial_name'  : '', 'commercial_phone' : '',\
                    'commercial_email' : [(5, [ commercial.id for commercial in partner.commercial_email ] )], 'price_notification_name' : '', 'price_notification_phone' : '',\
                    'price_notification_email' : [(5, [ price_notification.id for price_notification in partner.price_notification_email ] )],'account_name' : '', 'account_phone' : '', \
                    'account_email' : [(5, [ account.id for account in partner.account_email ] )],
                     'technical_name' : '', 'technical_phone' : '','technical_email' : [(5, [technical.id for technical in partner.technical_email ] )], 'user_email_temp' : '',\
                     'user_account_phone_number' : '', 'agreement' : ''
                     }
            self.write(cr,uid,ids,vamp)
            
            
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        
        return user_line_id
#             return {
#                 'type': 'ir.actions.client',
#                 'tag': 'reload_context',
#             }
            
##########################API 3 FEATURE ENDS HERE ########################################        





    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        user_obj=self.pool.get('res.users')
          
        res = super(res_partner, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form': 
            if uid ==SUPERUSERID or uid in SUPERACCOUNTUSER: 
                return res
             
            doc = etree.XML(res['arch'])

            for node in doc.xpath("//field[@name='email']"):
                user_id=str(uid)
                 
                 
                #modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]] ,"readonly": [["state","!=","initial"]] }'
		modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]] ,"readonly": ["&",["state","!=","initial"],["check_primary_email","=",false]] }'
                node.set('modifiers',modifier)
            
            for node in doc.xpath("//field[@name='phone']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]],"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)

            for node in doc.xpath("//field[@name='mobile']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]],"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)
                
#             for node in doc.xpath("//field[@name='partner_line']"):
#                 user_id=str(uid)
#                 
#                 modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]] ,"readonly": [["state","!=","initial"]] }'
#                 node.set('modifiers',modifier)                
            
                       
            
            
            res['arch'] = etree.tostring(doc)
            return res            

                  
        return res     

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        ''' Filter partner based on Vertical'''
        user_obj=self.pool.get('res.users')
        res=super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        try :
            if res : 
                #iterate to check status,vertical of partner
                
                res=[x for x in res if self.browse(cr,uid,x[0]).vertical == user_obj.browse(cr,uid,uid).vertical if self.browse(cr,uid,x[0]).state =='confirm']
    
            return res
        
        except Exception as E  : 
            
            raise osv.except_osv(_('Error in displaying Partner!'), _("Contact Odoo Team"))

    def default_vertcal_id(self, cr, uid, context=None):
        '''Return vertical assigned to company to which user logged in  '''
         
        if context is None:
            context = {}
         
        vertcial_id = self.pool.get('res.users').browse(cr, uid, uid).company_id.vertical
        if vertcial_id :
             
            return vertcial_id

        
    def _partner_lead(self, cr, uid, ids, name, args, context=None):
        crm_obj = self.pool.get('crm.lead')
        res = {}
        for partner_id in self.browse(cr, uid, ids) :
        #
            crm_id = crm_obj.search(cr, uid, [('partner_id', '=', partner_id.id)])
            if crm_id :
                
                if len(crm_id) > 1 :
                    raise osv.except_osv(_('Error!'), _('Multiple Partners "%s" assigned for single CRM.') % (self.browse(cr, uid, partner_id.id).name))
                
                res[partner_id.id] = crm_obj.browse(cr, uid, crm_id[0]).stage_id.name
            else :
                res[partner_id.id] =''
        
        return res

    

    def _set_domain(self, cr, uid, vals):
        ''' set doamin from email '''

       # import ipdb;ipdb.set_trace()
        block_domain_list= ['gmail.com','outlook.com','yahoo.com','rediffmail.com'] 
        if '@' in vals : 
            if vals.split('@')[1].lower() in block_domain_list : 
                domain=''
            
            else : 
                domain=vals.split('@')[1]
        else :
            domain=''
            
        return domain

#     def _check_unique(self, cr, uid, ids, context=None):
#         import ipdb;ipdb.set_trace()
#         names= self.search(cr, 1 , [], context=context)
# #         lst = [x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context) if x.name and x.id not in ids]
# #         for self_obj in self.browse(cr, uid, ids, context=context):
# #             if self_obj.name and self_obj.name.lower() in  lst:
# #                 return False
# #             return True
#         return True
#             
#     def _restricted_view(self, cr, uid, ids, field_name, arg, context=None):
#         import ipdb;ipdb.set_trace()
#         vals=''
#         if self.browse(cr,uid,ids[0]).user_id.id == uid :
#             self.write(cr,uid,ids[0],{'flag':True})
#          
#         return vals    
        
        
        
    def check_phone(self,cr,uid,vals): 
        ''' Phone validation'''
        
        return True

    
    def check_partner_email(self,cr,uid,vals): 
        '''Email validation to avoid dublicate partner '''
        
        cr.execute(''' select email from res_partner where is_company =True and state='confirm' ''')
        partner_email_list=[x[0] for x in cr.fetchall()]
        
        
        cr.execute(''' select id from res_partner where is_company =True and state='confirm' ''')
        partner_ids_list=[x[0] for x in cr.fetchall()]
        
        cr.execute(''' select email from res_partner_contact_line where partner_id in %s ''',(tuple(partner_ids_list),))
        partner_line_email_list=[x[0] for x in cr.fetchall()]
        
       
        if partner_line_email_list: 
            partner_email_list.extend(partner_line_email_list)
        
        if partner_email_list :
           
            for email_val in vals : 
                
                if email_val in partner_email_list :
                #import ipdb;ipdb.set_trace()
                    return False 
        return True



    def email_validation(self,cr,uid,vals): 
        '''Email validation to avoid dublicate partner '''
       # pattern='[^@]+@[^@]+\.[^@]+'
        pattern='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
        for email_val in [non_false for  non_false in vals if non_false not in (False,None)] : 

            if not re.match(pattern, email_val) : 
                #import ipdb;ipdb.set_trace()
                return False

        return True
    
    def collect_email_data(self,cr,uid,email,additional_email): 
        '''reformat email and additional email data '''

        domain_list=[ x['domain'] or False for x in map(lambda x:x[2],additional_email) ]
        check_email_list=[ x['email'] or False for x in map(lambda x:x[2],additional_email) ]
        
        if False in domain_list : 
            raise osv.except_osv(_('Invalid Action !'), _("Insert Secondary Domain"))

        if False in check_email_list : 
            raise osv.except_osv(_('Invalid Action !'), _("Insert Secondary Email")) 
        
        email_list=[ x['email'] for x in map(lambda x:x[2],additional_email) ]
        email_list.append(email)
        
        for email_val in  [non_false for  non_false in email_list if non_false not in (False,None)] :
            
            if email_list.count(email_val) > 1 : 
                return {'status':False,'email':email_val} 
                
         
        return {'status':True,'email_list':email_list} 


    _columns = {
              
              'partner_sequence':fields.char('Customer ID', size=15),
              'prepaid':fields.boolean('Prepaid',required=False),
              'postpaid':fields.boolean('Postpaid',required=False),
              'tan':fields.char('TAN', size=10),
              'pan':fields.char('PAN', size=10),
              'vat': fields.char('VAT', help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
              'vertical':fields.many2one('vertical.business', 'Vertical',readonly=False),
              'email_1':fields.char('Email 1'),
              'email_2':fields.char('Email 2'),
              'email_3':fields.char('Email 3'),
              'email_4':fields.char('Email 4'),
              'crm_lead_state':fields.char('Lead Status'),
              'partner_type': fields.selection([('india','India'), ('international','International')] ,'Type'),
              'routesms_cust_id':fields.char('Routesms Customer Id'),
              'routesms_remark':fields.char('Routesms Remark'),
              'company_registery':fields.char('Service Tax Reg.'),
              'signatory':fields.char('Authorize Signatory',size=20),
              'cin':fields.char('CIN'),
              'domain':fields.char('Domain'),
              'state': fields.selection([
                        ('initial', 'Draft'),                                         
                        ('cancel', 'Rejected'),                                         
                        ('draft', 'Pending'),
                        ('confirm', 'Confirm'),
                        ], 'Status', readonly=True, track_visibility='onchange',
                        help="Validating Partner", select=True),
              'partner_line': fields.one2many('res.partner.contact.line', 'partner_id', 'Contact Lines'), 
              'partner_alias':fields.char('Alias',size=20),
              'responsbile_for_partner':fields.char('RM',size=20),
              'user_line': fields.one2many('res.partner.add.user', 'partner_id', 'Add User Lines'),             
              
              'server':fields.many2one('server','Server'),
              'add_user':fields.char('User'),
	      'swap_history_line': fields.one2many('partner.swap.history', 'partner_id', 'Add Swap History'),
              'exclude_primary_email':fields.boolean('Do Not Send Email To Primary Address'),
              'check_primary_email':fields.boolean('Flag'),
              'local_price':fields.float('Local Price',digits=(32, 4)),
              'od_limit':fields.float('OD Limit'),
              'credit_limit':fields.float('Credit Limit'),
              'is_local_server':fields.boolean('Local Server?'),
              'reseller_code':fields.char('Reseller Code',size=4),
              'is_reseller_server':fields.boolean('Reseller Server?'),
              'distributor_code':fields.char('Distributor Code',size=4),
              'is_distributor_server':fields.boolean('Distributor Server?'),
              'routesms_notes':fields.text('Comments',size=100),
              'is_route_type':fields.boolean('Route Type?'),
              'is_active':fields.boolean('Active User Account'),
              'route_type':fields.selection([('promotional','Promotional'),('transactional','Transactional'),\
                            ('both','Both'),('transcrub','TranScrub')],'Route Type'),

              'user_email_temp':fields.char('User Email'),
              'agreement':fields.selection([('yes','Yes'),('no','No')],'Agreement'),
              
              'commercial_name':fields.char('Commercial Name', size=20),
              'commercial_phone':fields.char('Phone', size=15),
              'commercial_email':fields.many2many('commercial','partner_commercial_rel','partner_id','commercial_id',\
                                                  'Commercial Email'),

              
              'price_notification_name':fields.char('Price Notification Name', size=20),
              'price_notification_phone':fields.char('Phone', size=15),
              'price_notification_email':fields.many2many('price.notification', 'partner_price_notification_rel','partner_id',\
                                        'price_notification_id','Price Notification Email'),
              
              
              'account_name':fields.char('Account Name', size=20),
              'account_phone':fields.char('Phone', size=15),
              'account_email':fields.many2many('account', 'partner_account_rel','partner_id',\
                                        'account_id','Account Email'),
                
              'technical_name':fields.char('Technical Name', size=20),
              'technical_phone':fields.char('Phone', size=15),
              'technical_email':fields.many2many('technical', 'partner_technical_rel','partner_id',\
                                        'technical_id','Technical Email'),
              'user_account_phone_number' : fields.char('Phone'),
              'is_manage_subroute' : fields.boolean('Is Manage Routetype'),
              'manage_subroute' : fields.many2one('subroute', 'Manage Subroute'),


                              
              
              #'flag':fields.boolean('FLag'),
            #  'flag_function':fields.function(_restricted_view, string='Restricted View', type='char'),
              }

    _defaults = {
                
           #    'vertical':default_vertcal_id,
               'state': 'initial',
               'is_company':True,
               'exclude_primary_email':False,
               'check_primary_email':False,
               'is_local_server':False,
               'is_reseller_server':False,
               'is_distributor_server':False,
               'is_route_type':False,
               "is_active" : True ,
		'is_manage_subroute':False,

               
               } 


#    _constraints = [(_check_unique, 'Duplicate Name or Invalid format', ['name'])]

#     _defaults={'flag':False,
#                }

# 
#     def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#         user_obj=self.pool.get('res.users')
#         res = super(res_partner, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
#         if view_type == 'form':
#                
# 
#             import ipdb;ipdb.set_trace()
#             
#             return res
#         else:
#             return res


    # @api.model

    def validate_contact_person(self,cr,uid,ids,context): 
        '''auto generate odoo id contact person if parent '''
        vals={}
        if ids : 
                vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
                cr.execute('''update res_partner set state='confirm',partner_sequence=%s where id=%s ''',\
                           (vals['partner_sequence'],ids[0]))
#                 self.write(cr,uid,ids,{'state':'confirm','partner_sequence':vals['partner_sequence']})            
                print '--------contact person validated---------'
                 
        return True   
    
    def create(self, cr, uid, vals, context=None):
        ''' Overide create method to do validation'''
        
#         obj_sequence=self.pool.get('ir.sequence')
#         #obj_sequence.search(cr,uid,[('name','=',name)])
#         seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
#         if vals.get('partner_sequence', False) == False:
#             vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
        
        
###################################CUSTOMER VALIDATIONS######################### 
        master_email=[] 
        
        try :
            #vals['vertical']=self.pool.get('res.users').browse(cr, uid, uid).company_id.vertical.id
            vals['state']='draft'
            ############if partner is not customer and supplier################# 
            if vals.has_key('customer') ==False and vals.has_key('supplier')==False : 
                partner = super(res_partner, self).create(cr, 1, vals, context)
                return partner
            ######################################################################            
            if vals.has_key('company_id') : 
                vals['vertical']=self.pool.get('res.company').browse(cr, 1, vals['company_id']).vertical.id
            if vals['customer'] :
                cr.execute(''' select name from res_partner''')
                
                partner_name=[x[0] for x in cr.fetchall()]
                
                if vals['name'] in partner_name :
                    #raise osv.except_osv(_('Restricted!'), _('Partner already Exist'))
                    pass 
               # import ipdb;ipdb.set_trace()
                if vals.has_key('parent_id'):
                    if vals.get('parent_id') :
                        ################## CONTACT   PERSON  ##########################                        
                        partner_val=self.browse(cr,uid,vals['parent_id'])
                        user_id=partner_val.user_id.id
                        prepaid=partner_val.prepaid
                        postpaid=partner_val.postpaid
                        vertical=partner_val.vertical.id
                        vals['vertical']=vertical
                        
                        vals.update({'company_id':partner_val.company_id.id})
                        
                        #make is_company false for contact perosn

                        if vals.get('email') :
                           email_validation=self.email_validation(cr,uid,[vals.get('email')]) 
                           if not email_validation : 
                                raise osv.except_osv(_('Error!'), _('Incorrect Contact Person Email Id.'))
                            



                        vals['is_company']=False
                        
                        if user_id :
                            vals.update({'user_id':user_id})
                            if prepaid and postpaid :
                                raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))
                            
                            elif prepaid :
                                vals.update({'prepaid':True})
                                
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                ###generate contact person odoo id auto##
                                if partner_val.state=='confirm' : 
                                    self.validate_contact_person(cr,uid,[partner],context) 
                                return partner
                    
                            elif postpaid :
                                vals.update({'postpaid':True})
                                
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                ###generate contact person odoo id auto##
                                if partner_val.state=='confirm' : 
                                    self.validate_contact_person(cr,uid,[partner],context) 
                                return partner
                                
                            else :
                                raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                        raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))
    
    
                    else :
                        ################FOR COMPANY####################
                        ###############email validation############

                        if vals.get('email')==False : 
                            raise osv.except_osv(_('Error!'), _('Please Enter Email Address '))

                        if vals.get('domain')==False : 
                            raise osv.except_osv(_('Error!'), _('Please Enter Domain '))                        
                        
                        
                        if vals.get('partner_line') and vals.get('email'): 
                            #check both email data for dublication
                            master_email_additonal_email=self.collect_email_data(cr,uid,vals.get('email')\
                                                                ,vals.get('partner_line'))
                            
                            if master_email_additonal_email.get('status')==False : 
                                raise osv.except_osv(_('Error!'), _('Mulitple Email %s not allowed.') % (master_email_additonal_email.get('email')))
                                
                            else : 
                                master_email=master_email_additonal_email.get('email_list')
                                
                            
                       
                        if vals.get('email') : 
                            if master_email : 
                                email_validation=self.email_validation(cr,uid,master_email)
                                not_unique_email=self.check_partner_email(cr,uid,master_email)
                                
                            else : 
                                email_validation=self.email_validation(cr,uid,[vals.get('email')]) 
                                not_unique_email=self.check_partner_email(cr,uid,[vals.get('email')])
                                
                               
                            if not email_validation : 
                                raise osv.except_osv(_('Error!'), _('Incorrect Email Id '))
                            
                        ###check dublicate mail#####
                            
                            if not not_unique_email : 
                                raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))
                            
                            #vals['domain']=self._set_domain(cr,uid,vals.get('email'))



                       
                        prepaid=vals.get('prepaid')
                        postpaid=vals.get('postpaid')                
                        
                        if vals.has_key('user_id'):
                            if vals.get('user_id') :
                                if prepaid and postpaid :
                                    raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
        
                                elif prepaid :
                                    
                                
                                    partner = super(res_partner, self).create(cr, 1, vals, context)
                                    return partner                        
                                
                                
                                elif postpaid :
                                    
                                    partner = super(res_partner, self).create(cr,1, vals, context)
                                    return partner      
        
                                else :
                                    raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                                
                        raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))                                          
        
                    
                
                else :
                    ######FOR   COMPANY#####################
                    ###############email validation############

                    if vals.get('email')==False : 
                        raise osv.except_osv(_('Error!'), _('Please Enter Email Address '))
                    
                    if vals.get('domain')==False : 
                        raise osv.except_osv(_('Error!'), _('Please Enter Domain '))                       

                    
                    if vals.get('partner_line') and vals.get('email'): 
                        #check both email data for dublication
                        master_email_additonal_email=self.collect_email_data(cr,uid,vals.get('email')\
                                                            ,vals.get('partner_line'))
                        
                        if master_email_additonal_email.get('status')==False : 
                            raise osv.except_osv(_('Error!'), _('Mulitple Email %s not allowed.') % (master_email_additonal_email.get('email')))
                            
                             
                    
                    if vals.get('email') : 
                        if master_email : 
                            email_validation=self.email_validation(cr,uid,master_email)
                            not_unique_email=self.check_partner_email(cr,uid,master_email)
                            
                        else : 
                            email_validation=self.email_validation(cr,uid,[vals.get('email')]) 
                            not_unique_email=self.check_partner_email(cr,uid,[vals.get('email')])
                            
                           
                        if not email_validation : 
                            raise osv.except_osv(_('Error!'), _('Incorrect Email Id '))
                        
                    ###check dublicate mail#####
                        
                        if not not_unique_email : 
                            raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))
#                         vals['domain']=self._set_domain(cr,uid,vals.get('email'))


                   
                    prepaid=vals.get('prepaid')
                    postpaid=vals.get('postpaid')       
                    
                    if vals.has_key('user_id'):
                        if vals.get('user_id') :
        
                            if prepaid and postpaid :
                                raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
            
                            elif prepaid :
                                
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                return partner                        
                            
                            
                            elif postpaid :
                                
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                return partner      
            
                            else :
                                raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.')) 
        
        
                    
                    raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))
                    #partner = super(res_partner, self).create(cr, uid, vals, context)
            else :
                
                partner = super(res_partner, self).create(cr, 1, vals, context)
                return partner       
        except Exception as E :


            if vals.has_key('parent_id'):
                if vals.get('parent_id') :
                    #############FOR  CONTACT PEROSN#################
                    partner_val=self.browse(cr,uid,vals['parent_id'])
                    user_id=partner_val.user_id.id
                    prepaid=partner_val.prepaid
                    postpaid=partner_val.postpaid

                    ###############email validation############
                    if vals.get('email') : 
                       email_validation=self.email_validation(cr,uid,[vals.get('email')])
                       if not email_validation : 
                            raise osv.except_osv(_('Error!'), _('Incorrect Contact Person Email Id.'))
                                    

                    
                    if user_id :
                        vals.update({'user_id':user_id})
                        if prepaid and postpaid :
                            raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))
                        
                        elif prepaid :
                            vals.update({'prepaid':True})
                            partner = super(res_partner, self).create(cr, 1, vals, context)
                            ###generate contact person odoo id auto##
                            if partner_val.state=='confirm' : 
                                self.validate_contact_person(cr,uid,[partner],context) 
                                               
                            return partner
                
                        elif postpaid :
                            vals.update({'postpaid':True})
                            
                            partner = super(res_partner, self).create(cr, 1, vals, context)
                            ###generate contact person odoo id auto##
                            if partner_val.state=='confirm' : 
                                self.validate_contact_person(cr,uid,[partner],context) 
                                               
                            return partner
                            
                        else :
                            raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                    raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))


                else :
                    ############FOR  COMPANY############

                    ###############email validation############
                    if vals.get('email')==False : 
                        raise osv.except_osv(_('Error!'), _('Please Enter Email Address '))

                    if vals.get('domain')==False : 
                        raise osv.except_osv(_('Error!'), _('Please Enter Domain '))                       
                    
                    if vals.get('partner_line') and vals.get('email'): 
                        #check both email data for dublication
                        master_email_additonal_email=self.collect_email_data(cr,uid,vals.get('email')\
                                                            ,vals.get('partner_line'))
                        
                        if master_email_additonal_email.get('status')==False : 
                            raise osv.except_osv(_('Error!'), _('Mulitple Email %s not allowed.') % (master_email_additonal_email.get('email')))
                            
                         

                    
                    if vals.get('email') : 
                        if master_email : 
                            email_validation=self.email_validation(cr,uid,master_email)
                            not_unique_email=self.check_partner_email(cr,uid,master_email)
                            
                        else : 
                            email_validation=self.email_validation(cr,uid,[vals.get('email')]) 
                            not_unique_email=self.check_partner_email(cr,uid,[vals.get('email')])
                            
                           
                        if not email_validation : 
                            raise osv.except_osv(_('Error!'), _('Incorrect Email Id '))
                        
                    ###check dublicate mail#####
                        
                        if not not_unique_email : 
                            raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))
                       # vals['domain']=self._set_domain(cr,uid,vals.get('email'))


                   
                    prepaid=vals.get('prepaid')
                    postpaid=vals.get('postpaid')                
                    
                    if vals.has_key('user_id'):
                        if vals.get('user_id') :
                            if prepaid and postpaid :
                                raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
    
                            elif prepaid :
                            
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                return partner                        
                            
                            
                            elif postpaid :
                                partner = super(res_partner, self).create(cr, 1, vals, context)
                                return partner      
    
                            else :
                                raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                            
                    raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))                                          
    
                
            
            else :

                ###############email validation############
                ###############FOR  COMPANY###############

                if vals.get('email')==False : 
                    raise osv.except_osv(_('Error!'), _('Please Enter Email Address '))
                
                if vals.get('domain')==False : 
                    raise osv.except_osv(_('Error!'), _('Please Enter Domain '))                   
                
                if vals.get('partner_line') and vals.get('email'): 
                    #check both email data for dublication
                    master_email_additonal_email=self.collect_email_data(cr,uid,vals.get('email')\
                                                        ,vals.get('partner_line'))
                    
                    if master_email_additonal_email.get('status')==False : 
                        raise osv.except_osv(_('Error!'), _('Mulitple Email %s not allowed.') % (master_email_additonal_email.get('email')))
                        
                     


                
                if vals.get('email') : 
                    if master_email : 
                        email_validation=self.email_validation(cr,uid,master_email)
                        not_unique_email=self.check_partner_email(cr,uid,master_email)
                        
                    else : 
                        email_validation=self.email_validation(cr,uid,[vals.get('email')]) 
                        not_unique_email=self.check_partner_email(cr,uid,[vals.get('email')])
                        
                       
                    if not email_validation : 
                        raise osv.except_osv(_('Error!'), _('Incorrect Email Id '))
                    
                ###check dublicate mail#####
                    
                    if not not_unique_email : 
                        raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))
                    #vals['domain']=self._set_domain(cr,uid,vals.get('email'))
 



               
                prepaid=vals.get('prepaid')
                postpaid=vals.get('postpaid')       
                      
                if vals.has_key('user_id'):
                    if vals.get('user_id') :
    
                        if prepaid and postpaid :
                            raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
        
                        elif prepaid :
                        
                            partner = super(res_partner, self).create(cr, 1, vals, context)
                            return partner                        
                        
                        
                        elif postpaid :
                            partner = super(res_partner, self).create(cr, 1, vals, context)
                            return partner      
        
                        else :
                            raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.')) 
    
    
                
                raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))
            
            
            
            ##################################CUSTOMER VALIDATIONS STOPS##########


    def check_exclude_primary_email(self,cr,uid,partner): 
        ''' check atleast one email id active for this partner '''
        

        if partner.exclude_primary_email : 

            if not partner.partner_line : 
                raise osv.except_osv(_('Invalid Action!'), _('Partner Should Have Atleast One Active Email Id'))
            
            else :
                active_secondary_email=[ contact_line.email for contact_line in partner.partner_line if contact_line.send_email ]
                if not active_secondary_email : 
                    raise osv.except_osv(_('Invalid Action!'), _('Please Mark Send Email Option For Secondary Email'))

                
        return True 


    def check_for_duplicate_secondary_email(self,cr,uid,vals) : 
        '''raise error if secondary email already exist '''
        if vals.get('partner_line') : 
            
            email_vals=[ jj.get('email',False) for x in vals.get('partner_line') for jj in x  if type(jj)==dict if jj.get('email') ]
            not_unique_email=self.check_partner_email(cr,uid,email_vals)
            if not not_unique_email : 
                raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))  


    def check_other_contact_details(self,cr,uid,vals,partner_browse):
        '''validations on other contact details '''
        
        if vals.get('partner_line') : 
            
#             email_vals=[ jj.get('email',False) for x in vals.get('partner_line') for jj in x  if type(jj)==dict if jj.get('email') ]
#             domain_vals=[ jj.get('domain',False) for x in vals.get('partner_line') for jj in x  if type(jj)==dict if jj.get('domain') ]
#             send_email_vals=[ jj.get('send_email',False) for x in vals.get('partner_line') for jj in x  if type(jj)==dict if jj.get('send_email') ]


            email_vals=[x.email for x in partner_browse.partner_line   ]
            domain_vals=[x.domain for x in partner_browse.partner_line   ]
            send_email_vals=[x.send_email for x in partner_browse.partner_line   ]


#             
#             email_vals=[x.email for x in partner_browse.partner_line if partner_browse.partner_line  ]
#             domain_vals=[x.domain for x in partner_browse.partner_line if partner_browse.partner_line  ]
#             send_email_vals=[x.send_email for x in partner_browse.partner_line if partner_browse.partner_line  ]
            #import ipdb;ipdb.set_trace()
            if False in domain_vals :
                raise osv.except_osv(_('Error!'), _('Insert Secondary Domain !!')) 
            
            if False in email_vals  :
                raise osv.except_osv(_('Error!'), _('Insert Secondary Email Address !!'))              
            
            if len(email_vals) != len(set(email_vals)) : 
                raise osv.except_osv(_('Error!'), _('Duplicate Secondary Email Not Allowed !!'))   
            
#             if len(domain_vals) != len(set(domain_vals)) : 
#                 raise osv.except_osv(_('Error!'), _('Duplicate Secondary Domain Not Allowed !!')) 
#             

            
            email_validation=self.email_validation(cr,uid,email_vals) 
            if not email_validation : 
                raise osv.except_osv(_('Error!'), _('Incorrect Email Id '))                      

            
            if send_email_vals.count(False)==len(send_email_vals) and  partner_browse.exclude_primary_email : 
                raise osv.except_osv(_('Invalid Action!'), _('Partner Should Have Atleast One Active Email Id'))
     


    def write(self, cr, uid, ids, vals, context=None):
#         vals['vertical']=self.pool.get('res.users').browse(cr, uid, uid).company_id.vertical.id

	#import ipdb;ipdb.set_trace()
        if not ids : 
            return super(res_partner, self).write(cr, uid, ids,vals, context)

        ###############email validation############


	if vals.has_key('email') and not vals.get('email') : 
            raise osv.except_osv(_('Error!'), _('Primary Email Cannot Be Blank !!'))
 
        if vals.get('email') : 
            email_validation=self.email_validation(cr,uid,[vals.get('email')])
            if not email_validation : 
                raise osv.except_osv(_('Error!'), _('Incorrect Email Id.'))

        ###check dublicate mail#####
            if self.browse(cr,uid,ids[0]).is_company==True : 
                not_unique_email=self.check_partner_email(cr,uid,[vals.get('email')])
                if not not_unique_email : 
                    raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))            
            #vals['domain']=self._set_domain(cr,uid,vals.get('email'))

        if vals.has_key('company_id') : 
         
            vals['vertical']=self.pool.get('res.company').browse(cr, 1, vals['company_id']).vertical.id


        if ids : 
            
            partner_browse=self.browse(cr,uid,ids[0])

            if vals.get('user_id') :
                
                ###update crm sale order invoices record when bm is changed#########
                
                #if partner_browse.child_ids : 
                if partner_browse.is_company==True : 
                    
                    documents_migration=self.bm_swapping(cr,uid,ids,vals.get('user_id'))
                    if not documents_migration : 
                        raise osv.except_osv(_('Error!'), _('Salesperson Swapping Failed'))    
                

                ##check dublicate swecondary email
            if vals.get('partner_line') :  
                
                self.check_for_duplicate_secondary_email(cr,uid,vals)

            
        res_set = super(res_partner, self).write(cr, uid, ids,vals, context)
        '''Overide method to do assign saleperson & account type automatically '''
        res={}
    
        
        if vals :

            #PARTNER ACCOUNT TYPE SWAP
            if "prepaid" in vals or "postpaid" in vals : 
                if partner_browse.is_company : 
                    if not partner_browse.prepaid and not partner_browse.postpaid :  
                        raise osv.except_osv(_('Error!'), _('Select Prepaid/Posptaid'))
                    elif partner_browse.prepaid and partner_browse.postpaid : 
                        raise osv.except_osv(_('Error!'), _('Account Can Be Prepaid Or Postpaid'))
                    
                    self.partner_account_swapping(cr, uid, partner_browse)


            ###############check if BM,Account type is empty#####################
            
#             for key in vals.iterkeys(): 
#                 if vals.has_key('user_id') : 
#                     if not vals[key] : 
#                         raise osv.except_osv(_('Error!'), _('Record cannot be updated without Saleperson.'))
#                 elif vals.has_key('prepaid') : 
#                      

            ###check for atleast one active mail id###
            
            if vals.get('exclude_primary_email') : 
                self.check_exclude_primary_email(cr,uid,partner_browse)

        ####validatons on  secondary emails###
            if vals.get('partner_line') :  
                ##check dublicate swecondary email

                self.check_other_contact_details(cr,uid,vals,partner_browse)

                        
            
            if vals.get('user_id') :
                
                contact_id=self.search(cr,uid,[('parent_id','=',ids[0])])
                
                if contact_id :
                    for val in vals.iterkeys() :
                        
                        if val in ['user_id','prepaid','postpaid','customer','supplier','company_id','vertical'] :
                            res.update({val:vals[val]})
                    #cr.execute('''update res_partner set name='pppp' where id=%s''',(contact_id[0],))
                    
                    res=self.write(cr,uid,contact_id,res)
                    partner=self.browse(cr,uid,ids[0])
                    
                    if not partner.user_id : 
                        raise osv.except_osv(_('Error!'), _('Plese select Salesperson.'))
                    
                    
                    if partner.postpaid and partner.prepaid : 
                        raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))

                    if not partner.postpaid and not partner.prepaid : 
                        raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                         
                    return res   
                        
            else :
                try :

                    contact_id=self.search(cr,uid,[('parent_id','=',ids[0])])
                
                except Exception as E :
                    return res_set
                
                if contact_id :
                    for val in vals.iterkeys() :
                        
                        if val in ['user_id','prepaid','postpaid','customer','supplier','company_id','vertical'] :
                            res.update({val:vals[val]})
                    #cr.execute('''update res_partner set name='pppp' where id=%s''',(contact_id[0],))
                    
                    res=self.write(cr,uid,contact_id,res)
                    partner=self.browse(cr,uid,ids[0])
                   # import ipdb;ipdb.set_trace()
                    if not partner.user_id : 
                        raise osv.except_osv(_('Error!'), _('Plese select Salesperson.'))
                    
                    
                    if partner.postpaid and partner.prepaid : 
                        raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))

                    if not partner.postpaid and not partner.prepaid : 
                        raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                    
                    return res                  
        
        return res_set


    def remove_crm_record(self,cr,uid,partner_id):
        ''' remove CRM record for pending rejcted partners'''
        crm_obj=self.pool.get('crm.lead')
        try : 
            for crm_id in crm_obj.search(cr,uid,[('partner_id','=',partner_id)]) : 
                res=crm_obj.unlink(cr,SUPERUSERID,[crm_id])
                print '--------CRM REMOVED------'
        except Exception as E : 
            raise osv.except_osv(_('Error'), _('{}').format(E.message)) 
        
        return True


    def unlink(self,cr,uid,ids,context): 
        ''' Do not delete partner whose odoo id generated'''
        
        try : 
            for partner in self.browse(cr,uid,ids) :
                
                assert  partner.state!='confirm' and not partner.partner_sequence,\
                'Once The Odoo Id Generated You Cannot Delete Partner'
                self.remove_crm_record(cr,uid,partner.id)
            return super(res_partner,self).unlink(cr,uid,ids,context)

        except Exception as E :
            raise osv.except_osv(_('Error'), _('{}').format(E.message)) 


# Copy functionality


    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        ''' Restrict Users to duplicate partners'''
#        res= super(res_partner, self).copy(cr, uid, id, default, context=context)
        raise osv.except_osv(_('Validation Error!'), _('Partner Cannot Be Duplicated.'))



    def get_mailserver_details(self,cr,uid ): 
        '''get outgoing  mail server credentials to send email '''
        SUPERID=1
        uid=SUPERID
        mail_server_obj=self.pool.get('ir.mail_server')
        
        mail_server=mail_server_obj.search(cr,uid,[])
        if not mail_server : 
            raise osv.except_osv(_('Email Sending Failed'), _("Outgoing Mail Server Not Found!"))

        if len(mail_server) > 1 : 
            raise osv.except_osv(_('Email Sending Failed'), _("Multiple Outgoing Mail Server Found!"))
        server= mail_server_obj.browse(cr,uid,mail_server[0])
        
        return {'host':server.smtp_host + ':' +str(server.smtp_port),'username':server.smtp_user,'password':\
                server.smtp_pass}      

    def send_swap_mail_to_support(self,cr,uid,partner,server,**mail_context): 
        
        ''' send notificayion email to support team '''
        SUBJECT='Update Salesperson (BM) On BMXPIN of Odoo Id: {}'.format(partner.partner_sequence)
        MESSAGE='Hello Support Team,\n\nKindly Update Salesperson(BM) for Odoo Id :{}\n\nNew Salesperson(New BM): {}'\
        .format(partner.partner_sequence,mail_context.get('cc_addr_list'))
        
        notification=sendmail(
            from_addr    = mail_context.get('from_addr'),                               
            #to_addr_list = ['asmita.s@routesms.com'],
            to_addr_list = mail_context.get('to_addr_list'),
            cc_addr_list = [], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = server.get('username'), 
            password     = server.get('password')
             
            )                   
        
        if notification : 
            return True
        
        return False



    def send_swap_mail_to_bm(self, cr, uid, ids, context):
        ''' Send mail to bm about partner swap'''
        user_obj=self.pool.get('res.users')
        
        if not context.get('from_bm_id') or not context.get('to_bm_id') :
            raise osv.except_osv(_('Error!'), _('Salesperson Swapping Failed'))
        partner=context.get('partner')
        From_Salesperson=user_obj.browse(cr,SUPERUSERID,context.get('from_bm_id'))
        To_Salesperson=user_obj.browse(cr,SUPERUSERID,context.get('to_bm_id'))
                
            
        FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
        email_validation=self.email_validation(cr,uid,[FROM_MAIL])
        if not email_validation :
        #if '@' and '.com' not in FROM_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
             
        
        email_validation=self.email_validation(cr,uid,[From_Salesperson.login,To_Salesperson.login])
        if not email_validation :
        #if '@' and '.com' not in FROM_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Receiver's Email Id \n Contact HR Team"))
             


        SUBJECT = '''Partner Swapped/Migrated Successfully for "{}" & Odoo Id {}'''.format(partner.name,partner.partner_sequence)    
        
                         
        MESSAGE = '''Hello {} ,\n\nAll the documents associated with  {} & Odoo Id {} has been swapped/Migrated to {} \n\nThanks & Regards \n\n{}
        ''' .format(From_Salesperson.name,partner.name , partner.partner_sequence,To_Salesperson.name
                                    ,self.pool.get('res.users').browse(cr,uid,uid).name) 
         
        #check internet connection 
        
        connection =check_internet_connection('http://erp.routesms.com')
        #connection =check_internet_connection('182.72.52.19')  
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team'))              
        
                                            
        
        ###get server details
        
        server=self.get_mailserver_details(cr,uid)
        
        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            #to_addr_list = ['asmita.s@routesms.com'],
            to_addr_list = [From_Salesperson.login],
            cc_addr_list = [To_Salesperson.login], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = server.get('username'), 
            password     = server.get('password')
             
            )                   
        
        if notification :
            return {'type': 'ir.actions.act_window_close'}	
            ####send email to support team
#             if To_Salesperson.partner_type=='india' : 
#                 
#                 support_team_notification=self.send_swap_mail_to_support(cr,uid,partner,server,from_addr=FROM_MAIL,to_addr_list=['service.desk@routesms.com'],\
#                             cc_addr_list=To_Salesperson.login)
# 
#             else:
#                 support_team_notification=self.send_swap_mail_to_support(cr,uid,partner,server,from_addr=FROM_MAIL,to_addr_list=['support@routesms.com ','support24x7@routesms.com'],\
#                             cc_addr_list=To_Salesperson.login)
#             
#             if not support_team_notification : 
#                 raise osv.except_osv(_('ERROR'),
#                                     _('Email Sending To Support Team Failed ! \n Contact Odoo Team')) 
        
        else :
            ''' Sending fail'''
             
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))
        


    def check_uncicode(self,partner):
        '''throw exception of partner contains symbols '''
        try :
            print '{}'.format(partner.name)
        except Exception as E  :
            raise osv.except_osv(_('Error'),_('BM Swapping Failed\nUnicode Character Not Accepted\n\
            Kindly Rectify Partner Name'))
        return True


    def partner_account_swapping(self, cr, uid, partner) : 
        '''Send Account Swap Data To RSL Servers if account type chagnged from prepaid => postpaid or postpaid to prepaid '''
        return self.pool.get("odoo.rsl.api").partner_account_swap(cr, uid , partner )


    def bm_swapping(self,cr,uid,ids,bm_id) :
         
        '''Migrate BM and its other documents '''
        context={}
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        voucher_obj=self.pool.get('account.voucher')
        swap_history_obj=self.pool.get('partner.swap.history')
        hr_obj=self.pool.get('hr.employee')
        try :
             
            for partner in self.browse(cr,uid,ids) : 
                #bm_id=partner.user_id.id
                self.check_uncicode(partner)
                if partner.state !='confirm' : 
                    raise osv.except_osv(_('VALIDATION ERROR'),
                                        _('No Odoo Id Found'))

                if partner.is_company ==False : 
                    raise osv.except_osv(_('VALIDATION ERROR'),
                                        _('You Cannot Swap/Migrate Contact Person Directly'))
    
                    
                old_bm_id=partner.user_id.id
                 
                crm_id=crm_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])
#                 cr.execute('''select id from crm_lead where partner_id=%s ''',(partner.id,))
#                 crm_id=map(lambda x:x[0],cr.fetchall())
                if crm_id : 
                    print '*********import ipdb;ipdb.set_trace()*********TOTAL CRM *************',len(crm_id)
                      
                         
                    for crm in crm_obj.browse(cr,SUPERUSERID,crm_id) : 
                        if not crm.user_id or crm.user_id.id !=bm_id : 
                             
                            user_id_onchange=crm_obj.on_change_user(cr,bm_id,[crm],bm_id)
                            
                            if user_id_onchange.get('value').get('employee_id') :
                                #
                                crm_obj.write(cr,SUPERUSERID,[crm.id],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                            ,'user_id':bm_id})
                                 
                                print '*****************CRM UPDATED******************'
                            else : 
                                return 'Employee Not Found.\nContact HR xDepartment TO Create Employee For Odoo User'
                                       
     
     
                  
                ######assigne to Sale order#import ipdb;ipdb.set_trace()#########
                sale_id=sale_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])
                #import ipdb;ipdb.set_trace()
#                 cr.execute('''select id from sale_order where partner_id=%s ''',(partner.id,))
#                 sale_id=map(lambda x:x[0],cr.fetchall())                
                if sale_id : 
                    for sale in sale_obj.browse(cr,SUPERUSERID,sale_id)  :
                        if not sale.user_id or sale.user_id.id !=bm_id :
                            
                            user_id_onchange=sale_obj.sale_onchange_user(cr, bm_id, [sale_id], bm_id)
                            if user_id_onchange.get('value').get('employee_id') :
                                #import ipdb;ipdb.set_trace() 
                                sale_obj.write(cr,SUPERUSERID,[sale.id],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                 ,'user_id':bm_id})
                 
                                print '*****************SALE UPDATED******************'
                          
    
                #############assign to invoices##########
                #import ipdb;ipdb.set_trace()
                for invoice in inv_obj.browse(cr,SUPERUSERID,inv_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])) : 
                    if not invoice.user_id or invoice.user_id.id !=bm_id :
                            
                        inv_obj.write(cr,SUPERUSERID,[invoice.id],{'user_id':bm_id})
                        print '*****************INVOICE UPDATED******************'
                                
                
                #############assign to payments invoices##########        
                for voucher in voucher_obj.browse(cr,SUPERUSERID,voucher_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])) : 
                    if not voucher.user_id or voucher.user_id.id !=bm_id :
                        #import ipdb;ipdb.set_trace()    
                        
                        voucher_obj.write(cr,SUPERUSERID,[voucher.id],{'user_id':bm_id})
                        print '*****************PAYMENT  UPDATED******************'
                        
                
                #import ipdb;ipdb.set_trace()
                context.update({'from_bm_id':old_bm_id,'to_bm_id':bm_id,\
                                                                     'partner':partner})
                ########sync employee data to BMXPIN####
                hr_obj.synchronise_employee_record(cr,SUPERUSERID,None,api_type='bm_swapping',partner_record=partner,old_bm_id=old_bm_id,new_bm_id=bm_id,responsible=uid)

                ##send email to notify BM for swap
                self.send_swap_mail_to_bm(cr,uid,ids,context)
                
                ###maintain history of swap
                swap_history_obj.create(cr,SUPERUSERID,{'from_bm_id':old_bm_id,'to_bm_id':bm_id,'partner_id':partner.id})
                                
        except Exception as E :
            raise osv.except_osv(_('Error'),
                                        _('{}').format(str(E.value)))             
   
        
        print '------------UPDATE SUCCCESSFULLLY--------'
        return True

    def send_mail(self, cr, uid, ids, context=None):
        ''' Send mail to saleperson to notify partner is validated'''
         
        partner=self.browse(cr,uid,ids[0])
        if partner.supplier ==False and partner.customer ==False : 
            print '---------THIS COMPANY USER----------'
            return True         
 
        FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
        To_MAIL=partner.user_id.login
        if '@' and '.com' not in FROM_MAIL and To_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
 
 
        SUBJECT = '''Odoo ID Generated For "{}" '''.format(partner.name)         
                         
        MESSAGE = '''Hello {} ,\n\nPartner Details - \n\nName : {} \nOdoo Id : {}\n\nThanks & Regards \n\n{}
        ''' .format(partner.user_id.name , partner.name,partner.partner_sequence \
                                    ,self.pool.get('res.users').browse(cr,uid,uid).name) 
         
        #check internet connection
    #    import ipdb;ipdb.set_trace()
        connection =check_internet_connection('http://erp.routesms.com')  
        # connection =check_internet_connection('http://192.168.0.12:8069')
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team')) 
        
        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = [To_MAIL],
            cc_addr_list = ['sushma.gedam@routesms.com'], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = 'ar@routesms.com', 
            password     = 'Routesms@05'
             
            ) 
         
        if notification :
              
            return True
         
        else :
            ''' Sending fail'''
             
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))
# #     
#          ##################FOR TESTING PURPOESE#############
#     def send_mail(self, cr, uid, ids, context=None):
#         ''' Send mail to saleperson to notify partner is validated'''
#         
# 
#         
#         partner=self.browse(cr,uid,ids[0])
#         
# 
#         
#         FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
#         To_MAIL=partner.user_id.login
#         if '@' and '.com' not in FROM_MAIL and To_MAIL : 
#             raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
#                                 _("Invalid Sender's Email Id \n Contact HR Team"))
# 
# 
#         SUBJECT = '''Odoo ID Generated For "{}" '''.format(partner.name)         
#                         
#         MESSAGE = '''Hello {} ,\n\nPartner Details - \n\nName : {} \nOdoo Id : {}\n\nThanks & Regards \n\n{}
#         ''' .format(partner.user_id.name , partner.name,partner.partner_sequence \
#                                     ,self.pool.get('res.users').browse(cr,uid,uid).name) 
#         
#             #check internet connection 
#             
#         connection =check_internet_connection('http://erp.routesms.com')  
#         if not connection : 
#             raise osv.except_osv(_('No Internet Connection'),
#                                 _(' Contact IT Team'))        
#        
#         notification=sendmail(
#             from_addr    = 'shazzwazz20@gmail.com',                               
#             to_addr_list = ['shazz0020@gmail.com'],
#             cc_addr_list = ['shashank.verma@bistacloud.com'], 
#             subject      = SUBJECT, 
#             message      = MESSAGE, 
#             login        = 'ar@routesms.com', 
#             password     = 'Rsl@2015'
#             
# )                           
#         
#         if notification :
#              
#             return True
#         
#         else :
#             ''' Sending fail'''
#             
#             raise osv.except_osv(_('ERROR'),
#                                 _('Email Sending Failed! \n Contact Odoo Team'))
#     

    def check_employee_record(self,cr,uid,partner): 
        '''throw exception if  employee recorded not created '''
        try : 
	    #import ipdb;ipdb.set_trace()
            hr_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',partner.user_id.id)])
            assert hr_id,'No Employee Create By HR\nContact HR Department'
            assert len(hr_id)==1,'Duplicate Employee Record Found\nContact HR Department'

        except Exception as E :
            raise osv.except_osv(_('Error!'), _('{}').format(E.message)) 
        return True

    def check_employee_record_2(self,cr,uid,partner): 
        '''throw exception if  employee recorded not created.this partner record is not a company,instead
        its a employee of company, supplier and customer=False '''
        try : 
	    uid=1
	    #import ipdb;ipdb.set_trace()
            user=self.pool.get('res.users').search(cr,uid,[('partner_id','=',partner.id)])
            assert len(user)==1,'No Record or Multiple Odoo User Account Found\nContact Odoo Team'
            hr_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user[0])])
            assert hr_id,'No Employee Create By HR\nContact HR Department'
            assert len(hr_id)==1,'Duplicate Employee Record Found\nContact HR Department'

        except Exception as E :
            raise osv.except_osv(_('Error!'), _('{}').format(E.message)) 
        return True


    def validate_partner(self,cr,uid,ids,context): 
        ''' Confirm Partner'''
         
        obj_sequence=self.pool.get('ir.sequence')
        hr_obj=self.pool.get('hr.employee')
        #obj_sequence.search(cr,uid,[('name','=',name)])
        vals={}
        partner_email_list=[]
        ###check dublicate email id#####
        partner=self.browse(cr,uid,ids[0])
        
        if partner.email : 
            if partner.partner_line: 
                partner_email_list=[ jj.email for jj in partner.partner_line ];partner_email_list.append(partner.email)
            else : 
                partner_email_list.append(partner.email)

            not_unique_email=self.check_partner_email(cr,uid,[partner.email])
            if not not_unique_email : 
                raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))               

        ##################check weather employee record created#####################
        ############if confirming actual partner/client##########
        if partner.customer or partner.supplier :  
            self.check_employee_record(cr,SUPERUSERID,partner)

        seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
        if vals.get('partner_sequence', False) == False:
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
            self.write(cr,uid,ids,{'state':'confirm','partner_sequence':vals['partner_sequence']})
        #############if confirming employee of company########
            if not partner.customer and not partner.supplier : 
                self.check_employee_record_2(cr,SUPERUSERID,partner)
                hr_obj.synchronise_employee_record(cr,SUPERUSERID,None,api_type='create_employee',partner_employee_record=partner)
                                         
        contact_id=self.search(cr,uid,[('parent_id','=',ids[0])])
        if contact_id :
             
     
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
            try :
		#import ipdb;ipdb.set_trace()
                self.write(cr,uid,contact_id,{'state':'confirm','partner_sequence':vals['partner_sequence']})
            except Exception as E : 

                if not E.message : 
                    E.message=E.value 

                raise osv.except_osv(_('Error!'), _('Updating Document Failed'))


        if self.browse(cr,uid,ids[0]).routesms_remark != 'PARTNER CREATED FROM QMS' :
	    print '---------------------E M  A I L D  I  S  A  B  A L	E	D-----------' 
            self.send_mail(cr, uid, ids, context=None)        
#       self.send_mail(cr, uid, ids, context=None)
         
                 
         
        return True 


    def send_cancel_mail(self, cr, uid, ids, context=None):
        ''' Send mail to saleperson to notify partner is rejected'''
                  
        partner=self.browse(cr,uid,ids[0])
        if partner.supplier ==False and partner.customer ==False : 
            print '---------THIS COMPANY USER----------'
            return True
        
        FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
        To_MAIL=partner.user_id.login
        if '@' and '.com' not in FROM_MAIL and To_MAIL : 
            raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
                                _("Invalid Sender's Email Id \n Contact HR Team"))
  
  
        SUBJECT = '''Partner Rejected "{}" '''.format(partner.name)         
        
        MESSAGE = '''Hello {} ,\n\nPartner {} has been Rejected\nReason For Rejection : {}\n\nThanks & Regards \n\n{}
        ''' .format(partner.user_id.name,partner.name ,partner.comment,self.pool.get('res.users').browse(cr,uid,uid).name)
                                       
            #check internet connection 
        
        #connection =check_internet_connection('http://erp.routesms.com')  
        connection =check_internet_connection('http://192.168.0.12:8069')
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team'))         
        try :
        # remove partner
            contact_ids=self.search(cr,uid,[('parent_id','=',ids[0])])
            for contact_id in contact_ids : 
                self.unlink(cr,SUPERUSERID,[contact_id],context)
                 
            self.unlink(cr,SUPERUSERID,ids,context)
            
         
        except Exception as E : 
       	   # import ipdb;ipdb.set_trace() 
            raise osv.except_osv(_('ERROR'),
                                _('Deleting  Partner Document Failed ! \n Contact Odoo Team'))
            

        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = [To_MAIL],
            cc_addr_list = ['sushma.gedam@routesms.com'], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = 'ar@routesms.com', 
            password     = 'Art@76gr'
              
            )            

        if notification :
            return True        
          
        else :
            ''' Sending fail'''
              
            raise osv.except_osv(_('ERROR'),
                                _('Email Sending Failed! \n Contact Odoo Team'))    



#####################3

#########################3
     
# #############################TESTING  PURPOSE#################
#     def send_cancel_mail(self, cr, uid, ids, context=None):
#         ''' Send mail to saleperson to notify partner is rejected'''
#                  
#         partner=self.browse(cr,uid,ids[0])
#         FROM_MAIL=self.pool.get('res.users').browse(cr,uid,uid).login
#         To_MAIL=partner.user_id.login
#         if '@' and '.com' not in FROM_MAIL and To_MAIL : 
#             raise osv.except_osv(_('EMAIL VALIDATION ERROR'),
#                                 _("Invalid Sender's Email Id \n Contact HR Team"))
#          
#  
#         SUBJECT = '''Partner Rejected "{}" '''.format(partner.name)         
#            
#         MESSAGE = '''Hello {} ,\n\nPartner {} has been Rejected\n\nThanks & Regards \n\n{}
#         ''' .format(partner.user_id.name,partner.name ,self.pool.get('res.users').browse(cr,uid,uid).name)
#                                       
#          
#          
#         #import ipdb;ipdb.set_trace()
#             #check internet connection 
#              
#         connection =check_internet_connection('http://erp.routesms.com')  
#         if not connection : 
#             raise osv.except_osv(_('No Internet Connection'),
#                                 _(' Contact IT Team'))
#                         
# 
#         
#         
#              
#         try :
#             
# # remove partner
#             contact_ids=self.search(cr,uid,[('parent_id','=',ids[0])])
#             for contact_id in contact_ids : 
#                 self.unlink(cr,uid,[contact_id],context)
#             self.unlink(cr,uid,ids,context)
#                
# 
#                
#         except Exception as E : 
# 
#            raise osv.except_osv(_('ERROR'),
#                                _('Deleting  Partner Document Failed ! \n Contact Odoo Team'))                 
#    
#         notification=sendmail(
#             from_addr    = 'shazzwazz20@gmail.com',                               
#             to_addr_list = ['shazz0020@gmail.com'],
#             cc_addr_list = ['shashank.verma@bistacloud.com'], 
#             subject      = SUBJECT, 
#             message      = MESSAGE, 
#             login        = 'ar@routesms.com', 
#             password     = 'Rsl@2015'
#              
#             )         
#         
#         if notification :
#             return True
#          
# 
#         else :
#             ''' Sending fail'''
#              
#             raise osv.except_osv(_('ERROR'),
#                                 _('Email Sending Failed! \n Contact Odoo Team'))    
#      
#  
#          
# 
#         


    def reject_partner_old_23feb_2016(self,cr,uid,ids,context): 
        ''' Reject Partner'''
        if not self.browse(cr,uid,ids[0]).comment : 
            raise osv.except_osv(_('Validation Error'),
                                _('Kindly specify reason for rejection'))             
        self.write(cr,uid,ids,{'state':'cancel'})            
    #	import ipdb;ipdb.set_trace()    
        notification=self.send_cancel_mail(cr, uid, ids, context=None)
        
        if notification : 
            return True
        
        ''' Sending fail'''
        
        raise osv.except_osv(_('ERROR'),
                            _('Email Sending Failed! \n Contact Odoo Team'))        
    
    def reject_partner(self,cr,uid,ids,context): 
        ''' Reject Partner'''
        
        try:
            partner=self.browse(cr,uid,ids[0])
            assert partner.customer or  partner.supplier,'Employee Record Cannot Be Rejected'
            assert partner.is_company and not partner.parent_id,'Not Valid Company'
            self.write(cr,uid,ids,{'state':'cancel'})
            notification=self.send_cancel_mail(cr, uid, ids, context=None)
            assert notification,'Email Sending Failed! \n Contact Odoo Team' 
        
        except Exception as E : 
            raise osv.except_osv(_('Error'),
                            _('{}').format(E.message) )  
        return True


class res_partner_contact_line(osv.osv): 
    
    _name='res.partner.contact.line'
    _description='Add Multiple Email Details'
    
    _columns={
              'partner_id': fields.many2one('res.partner', 'Additional Contact Information', ondelete='cascade'),
              'email':fields.char('Email'),
              'domain':fields.char('Domain'),
              'send_email':fields.boolean('Send Email'),
                                          
              }


class res_partner_add_user(osv.osv): 
    
    _name='res.partner.add.user'
    _description='Add user and send odoo partner information to server'
    
    _columns={
              'partner_id': fields.many2one('res.partner', 'Server User Information', ondelete='cascade'),
              'username':fields.char('User', size = 15),
              'server_domain':fields.many2one('server','Server'),
              'local_price':fields.float('Local Price',digits=(32, 4)),
              'od_limit':fields.float('OD Limit'),
              'credit_limit':fields.float('Credit Limit'),
              'status':fields.selection([('pending','Pending'),('approved','Approved')],'Approval Status'),
              'create_date':fields.datetime('Created On'),
              'update_date':fields.datetime('Last updated'),
              'approved_by':fields.many2many('res.users','approved_by_users_restore_rel','add_users_id',\
                                             'users_id','Approved By'),
              'approved_by_name':fields.char('Approved By'),
              'is_live':fields.boolean('Is Live'),
              'reseller_code':fields.char('Reseller Code',size=4),

              'distributor_code':fields.char('Distributor Code',size=4),

              'routesms_notes':fields.text('Comments',size=100),

              'route_type':fields.selection([('promotional','Promotional'),('transactional','Transactional'),\
                            ('both','Both'),('transcrub','TranScrub')],'Route Type'),
              'is_local_server':fields.boolean('Local Server?'),
              'is_active' : fields.boolean('Active'),
              'user_line_restore': fields.one2many('res.partner.add.user.restore', 'res_partner_add_user_id',\
                                                   'User Account Restore'),                 
              'agreement':fields.selection([('yes','Yes'),('no','No')],'Agreement'),
              
              'commercial_name_phone':fields.char('Commercial Name/Phone'),
              'commercial_email':fields.text('Commercial Email'),

              'price_notification_name_phone':fields.char('Price Notification Name/Phone'),
              'price_notification_email':fields.text('Price Notification Email'),   

              'account_name_phone':fields.char('Accounts Name/Phone'),
              'account_email':fields.text('Accounts Email'),
              
              'technical_name_phone':fields.char('Technical Name/Phone'),
              'technical_email':fields.text('Technical Email'),
              'user_email_temp' : fields.char('User Email'),
              'user_account_phone_number' : fields.char('Phone'),
              'manage_subroute' : fields.many2one('subroute', 'Manage Subroute'),
              
              }
    
    _defaults={
               'is_live':False,
               'create_date':fields.datetime.now,
               'is_local_server':False,
               }


class res_partner_add_user_restore(osv.osv): 
    
    _name='res.partner.add.user.restore'
    _description='Store User Account Details Which Recovered During User Account Updation Rejection'
    
    _columns={
              'res_partner_add_user_id': fields.many2one('res.partner.add.user', 'User Account Details'),
              'partner_id': fields.many2one('res.partner', 'Server User Information', ondelete='cascade'),
              'username':fields.char('User', size = 15),
              'server_domain':fields.many2one('server','Server'),
              'local_price':fields.float('Local Price',digits=(32, 4)),
              'od_limit':fields.float('OD Limit'),
              'credit_limit':fields.float('Credit Limit'),
              'status':fields.selection([('pending','Pending'),('approved','Approved')],'Approval Status'),
              'create_date':fields.datetime('Created On'),
              'update_date':fields.datetime('Last updated'),
              'approved_by':fields.many2many('res.users','approved_by_users_restor_rel','add_users_id',\
                                             'users_id','Approved By'),
              'approved_by_name':fields.char('Approved By'),
              'is_live':fields.boolean('Is Live'),
              'reseller_code':fields.char('Reseller Code',size=4),

              'distributor_code':fields.char('Distributor Code',size=4),

              'routesms_notes':fields.text('Comments',size=100),

              'route_type':fields.selection([('promotional','Promotional'),('transactional','Transactional'),\
                            ('both','Both'),('transcrub','TranScrub')],'Route Type'),
              'is_local_server':fields.boolean('Local Server?'),
              'is_active' : fields.boolean('Active'),                 
              'agreement':fields.selection([('yes','Yes'),('no','No')],'Agreement'),
              'commercial_name_phone':fields.char('Commercial Name/Phone'),
              'commercial_email':fields.text('Commercial Email'),

              'price_notification_name_phone':fields.char('Price Notification Name/Phone'),
              'price_notification_email':fields.text('Price Notification Email'),   
              'account_name_phone':fields.char('Accounts Name/Phone'),
              'account_email':fields.text('Accounts Email'),
              'technical_name_phone':fields.char('Technical Name/Phone'),
              'technical_email':fields.text('Technical Email'),
              'user_email_temp' : fields.char('User Email'),
              'user_account_phone_number' : fields.char('Phone'),                
              'manage_subroute' : fields.many2one('subroute', 'Manage Subroute'),   
               
              
              }
    
    _defaults={
               'is_live':False,
               'create_date':fields.datetime.now,
               'is_local_server':False,
               }        
      
class commercial(osv.osv):  
    
    _name = 'commercial'
    _description = 'Create Commerical Emails'
    _rec_name = 'email'
    
    _columns={
              'email':fields.char('Email'),
              'user_id' : fields.many2one('res.users','Salesperson',readonly = True)
              }         
    
    def create(self, cr, uid, vals, context): 
        '''validate email address '''
        partner_obj=self.pool.get("res.partner")
        # VALIDATE EMAIL
        try : 
            
            valid_email = partner_obj.email_validation(cr, uid, [ vals.get("email") ] )
            assert valid_email, "Invalid Email Address"
            assert context.get("uid"), "Technical Error\nUser Id Not Found\nContact Odoo Team"
            vals["user_id"] = context.get("uid") 
            return super(commercial, self).create(cr, uid, vals, context)
        
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        

class price_notification(osv.osv):  
    
    _name = 'price.notification'
    _description = 'Create price Notification Emails'
    _rec_name = 'email'
    
    _columns={
              'email':fields.char('Email'),
              'user_id' : fields.many2one('res.users','Salesperson',readonly = True)
              }     
    def create(self, cr, uid, vals, context): 
        '''validate email address '''
        partner_obj=self.pool.get("res.partner")
        # VALIDATE EMAIL
        try : 
            
            valid_email = partner_obj.email_validation(cr, uid, [ vals.get("email") ] )
            assert valid_email, "Invalid Email Address"
            assert context.get("uid"), "Technical Error\nUser Id Not Found\nContact Odoo Team"
            vals["user_id"] = context.get("uid") 
            return super(price_notification, self).create(cr, uid, vals, context)
        
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))

class account(osv.osv): 
    
    _name = 'account'
    _description = 'Create Account Emails'
    _rec_name = 'email'
    
    _columns={
              'email':fields.char('Email'),
              'user_id' : fields.many2one('res.users','Salesperson',readonly = True,invisible = True)
              }

    def create(self, cr, uid, vals, context): 
        '''validate email address '''
        partner_obj=self.pool.get("res.partner")
        # VALIDATE EMAIL
            
        try : 
            valid_email = partner_obj.email_validation(cr, uid, [ vals.get("email") ] )
            #import ipdb;ipdb.set_trace()
            assert valid_email, "Invalid Email Address"
            assert context.get("uid"), "Technical Error\nUser Id Not Found\nContact Odoo Team"
            vals["user_id"] = context.get("uid") 
            return super(account, self).create(cr, uid, vals, context)
        
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
    
class technical(osv.osv):  
    
    _name = 'technical'
    _description = 'Create Technical Emails'
    _rec_name = 'email'
    
    _columns={
              'email':fields.char('Email'),
              'user_id' : fields.many2one('res.users','Salesperson',readonly = True),
              }

    def create(self, cr, uid, vals, context): 
        '''validate email address '''
        partner_obj=self.pool.get("res.partner")
        # VALIDATE EMAIL
        try : 
            
            valid_email = partner_obj.email_validation(cr, uid, [ vals.get("email") ] )
            assert valid_email, "Invalid Email Address"
            assert context.get("uid"), "Technical Error\nUser Id Not Found\nContact Odoo Team"
            vals["user_id"] = context.get("uid") 
            return super(technical, self).create(cr, uid, vals, context)
        
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        
class subroute(osv.osv):    
    _name='subroute'
    _description='Manage subroute of indiareseller and indiadistributor'    

    _columns={
              'name':fields.char('Name'),
              'route_type': fields.selection([('promotional','Promotional'), ('transactional','Transactional')] ,'Route Type'),
              'routename': fields.char('Routename',size=15),
              'defaultroute' : fields.char('Default RouteName',size=15),
              'local_price' : fields.float('Local Price',digits=(32, 4)),
              'username': fields.char('Username'),
              'server':fields.many2one('server','Server'),
              'res_partner_add_user_id': fields.many2one('res.partner.add.user', 'User Account Details'),
              'confirm' : fields.boolean('Confirm ?'),
              'subroute_line_promotional': fields.one2many('subroute.line', 'subroute_id_promotional', 'Promotional'),
              'subroute_line_transactional': fields.one2many('subroute.line', 'subroute_id_transactional', 'Transactional'),              
              }    

    _defaults={
               'confirm' : False,
               }        
#     def write(self,cr ,uid, ids, vals, context): 
#         result= super(subroute,self).write(cr, uid, ids, vals, context)
#         subroute_id = self.browse(cr, uid, ids[0])
#         if subroute_id.local_price <=0 :
#             raise osv.except_osv(_("Error"),_("Local Price Should Be Always Greater Than Zero"))
#         return result        
        
class subroute_line(osv.osv):    
    _name='subroute.line'
    _description='Manage subroute line of indiareseller and indiadistributor'    
    _rec_name = 'routename'
    _columns={
              'subroute_id_promotional' : fields.many2one('subroute','Subroute'),
              'subroute_id_transactional' : fields.many2one('subroute','Subroute'),
              'username': fields.char('Username'),
              'server':fields.many2one('server','Server'),
              'route_type': fields.selection([('promotional','Promotional'), ('transactional','Transactional')] ,'Route Type'),
              'routename': fields.char('Routename',size=15),
              'defaultroute' : fields.char('Default RouteName',size=15),
              'local_price' : fields.float('Local Price',digits=(32, 4)),
              'status': fields.selection([('pending','Pending'), ('approved','Approved'),('rejected','Rejected')] ,'Status'),
              'mode': fields.selection([('create','Create'), ('update','Update')] ,'Mode'),
              }
                

    _defaults={
               'status' : 'pending',
               'confirm_routename' : False,
               'mode' : 'create',
               }


    def create(self, cr, uid, vals, context=None): 
        subroute_obj = self.pool.get("subroute")

            
        if "subroute_id_promotional" in vals  :
            subroute_id = vals ["subroute_id_promotional"]
            vals ["route_type"] = "promotional"

        elif "subroute_id_transactional" in vals  :
            subroute_id = vals ["subroute_id_transactional"]
            vals ["route_type"] = "transactional"
        
        else : 
            raise osv.except_osv(_("Error"),_("Technical Error  subroute_id_promotional & subroute_id_transactional Not Found\nContact Odoo Team"))
        
        cr.execute('''select routename from subroute_line where routename=%s ''',( vals['routename'],))
        routename = map(lambda x:x[0], cr.fetchall())
        #routename=[]
        
        if routename  :
            raise osv.except_osv(_("Error"),_("Routename '%s' Already Exist\nRoutename Must Be Always Unique")%( vals['routename']))
        if vals ["local_price"] <=0.0 : 
            raise osv.except_osv(_("Error"),_("Local Price Of '%s' Should Be Always Greater Than Zero")%( vals["routename"]))
             
        # GET SUBROUTE USERNAME AND SERVER NAME
        subrouting = subroute_obj.browse(cr, uid, subroute_id) 
        vals.update( {"username" : subrouting.username, "server" : subrouting.server.id})
               
        return super(subroute_line, self).create(cr, uid, vals, context)
    
    def write(self,cr, uid, ids, vals, context):
        subrouting_line = self.browse( cr, uid, ids[0])
        if "local_price" in vals and vals.get("local_price") <=0.0 : 
            raise osv.except_osv(_("Error"),_("Local Price Of '%s' Should Be Always Greater Than Zero")%( subrouting_line.routename))
        
        # CASE 1 PENDING-CREATE AND REJECTED
        if subrouting_line.status == "pending" and vals.get("status") == "rejected" : 
            pass

        # CASE 2 PENDING-CREATE AND APPROVED

        elif subrouting_line.status == "pending" and vals.get("status") == "approved" : 
            vals ["mode"] = "update"    
            
#         # CASE 3 REJECTED-CREATE AND REJECTED
#         elif subrouting_line.status == "rejected" and vals.get("status") == "rejected" : 
#             pass
# 
#         # CASE 4 REJECTED-CREATE AND APPROVED
#         elif subrouting_line.status == "rejected" and vals.get("status") == "approved" : 
#             vals ["mode"] = "update"
# 
#         # CASE 5 APPROVED-UPDATE AND APPROVED
#         elif subrouting_line.status == "approved" and vals.get("status") == "approved" : 
#             pass
# 
#         # CASE 6 APPROVED-UPDATE AND APPROVED
#         elif subrouting_line.status == "approved" and vals.get("status") == "rejected" : 
#             pass 


        # CASE 8 PENDING-UPDATE AND REJECTED
        elif subrouting_line.status == "pending" and vals.get("status") == "rejected" : 
            pass         

        
        else : 
            vals ["status"] = "pending"
        
        
        return super(subroute_line, self).write(cr, uid, ids, vals, context) 
        
            
        
#     def action_manage_subroute(self,cr, uid, ids, context=None): 
#         ''' Confirm subroute details for reseller and distributor account'''
#         return self.write(cr, uid, ids, {"confirm" : True})

        
class partner_swap_history(osv.osv): 
    
    _name='partner.swap.history'
    _description='Maintain partner swap history'
    
    _columns={
              'name':fields.char('Date'),
              'from_bm_id': fields.many2one('res.users', 'From', ondelete='cascade'),
              'to_bm_id': fields.many2one('res.users', 'To', ondelete='cascade'),
              'date':fields.datetime('Date'),
              'partner_id': fields.many2one('res.partner', 'Partner', ondelete='cascade'),
              }    
    
    _defaults={
               'name':'/',
               'date':fields.datetime.now
               }        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
