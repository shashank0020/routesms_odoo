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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from lxml import etree
import bcrypt
import re
from openerp import models, fields as fields8, api, _
import datetime
SUPERID=1


class sync_partner_account_type(models.TransientModel):
    _name = "sync.partner.account.type"
    _description = "Wizard to sync partner account type data prepaid/postpaid manually"
    
    @api.multi
    def synchronise_partner_account_type(self):
        '''sync partner account type to RSL server '''
        partner_obj = self.env["res.partner"]
        
        for partner_id in self.env.context.get('active_ids') :
            partner = partner_obj.browse(partner_id)
            partner_obj.partner_account_swapping(partner)
            
        return True


class sync_employee_data(models.TransientModel):
    _name = "sync.employee.data"
    _description = "Wizard to sync employee data manually to 3rd party application"
    
    @api.multi
    def synchronise_employee_record(self):
        '''sync employee data to BMXPIN '''
        obj=self.env[self.env.context.get('active_model')]
        for emp_id in self.env.context.get('active_ids') : 
            
            obj.synchronise_employee_record(api_type='update_employee',employee_record=obj.browse(emp_id))
        return True



class change_password_user(osv.TransientModel):
    """
        A model to configure users in the change password wizard
    """

    _inherit = 'change.password.user'
    _description = 'Change Password Wizard User'

    def update_user_credentials(self,cr,**vals):
        '''set updated credentials to Indian /International user '''
        international_user_obj = self.pool.get('int.user')
        india_user_obj = self.pool.get('ind.user')
        
        if vals.get('user').partner_type =='india' :
            for ind_user in india_user_obj.browse(cr,SUPERID,india_user_obj.search(cr,SUPERID,[('name','=',vals.get('user').id)])) :
                india_user_obj.write(cr,SUPERID,[ind_user.id],{'password':vals.get('password'),'access_token':vals.get('access_token'),'password_reset':True}) 

        elif vals.get('user').partner_type =='international' :
            for int_user in international_user_obj.browse(cr,SUPERID,international_user_obj.search(cr,SUPERID,[('name','=',vals.get('user').id)])) :
                international_user_obj.write(cr,SUPERID,[int_user.id],{'password':vals.get('password'),'access_token':vals.get('access_token'),'password_reset':True})

        else : 
            raise osv.except_osv(_('Error!'), _('Partner Type International or India Not Set!\n Contact HR Department')) 
        
        

    def validate_user_password(self,cr,uid,password,user) : 
        '''check password '''
        
        password_reset_wizard_obj=self.pool.get('reset.user.password')
        ############validate password#####
        password_reset_wizard_obj.check_password_pattern(password)
        hashed_password=password_reset_wizard_obj.password_hashing(password)
        self.update_user_credentials(cr,password=password,access_token=hashed_password,user=user)
        
        


    def change_password_button(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            line.user_id.write({'password': line.new_passwd})
            #############custom code added to play with passsowrdss################
            self.validate_user_password(cr,uid,line.new_passwd,line.user_id)
            ####################ENDS##############################
        # don't keep temporary passwords in the database longer than necessary
        self.write(cr, uid, ids, {'new_passwd': False}, context=context)



class reset_user_password(osv.osv_memory):
    _name = "reset.user.password"
    _description = "Reset Password"
    
    _columns={
    'name':fields.char(string='New Password',help="This will be your new login password"),
    'reset_completed':fields.boolean('Reset Password Completed ?'),
    
        
    }
    _defaults={
               'reset_completed':False,
               }

    def send_username_newpassword_email(self, cr, uid, obj,user_id ):
        ''' Send mail to odoo users about new password reset from HR email'''
        
        partner_obj=self.pool.get('res.partner')
        user_obj=self.pool.get('res.users')
        routesms_email_config_obj=self.pool.get('send.email.with.attactment')
        
        if obj : 

        
            
            FROM_MAIL='sandhya@routesms.com' #odoo user will receive email from HR EMAIL ID
            email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
            if not email_validation :
                raise osv.except_osv(_('Error'),
                                    _("Invalid Sender's Email Id \n Contact HR Team"))
                 

            ##check receiver mail addres
            
            TO_MAIL=user_id.login#########receiver e
            
            
            email_validation=partner_obj.email_validation(cr,uid,[TO_MAIL])
            if not email_validation :
                raise osv.except_osv(_('Error'),
                                    _("Invalid Receiver's Email Id \n Contact HR Team"))

 
            SUBJECT = '''ODOO PASSWORD RESET'''    

                             
            MESSAGE = '''Hello {} ,\n\nNew Odoo credentials as follows: \n\nUsername: {}\nPassword: {}\n\nThanks & Regards \n\n{}
            ''' .format(user_id.name,user_id.login,obj.name,'HR DEPARTMENT') 
                          
            ###############ATTACHED FILES########################
            attachment,binary,extension='','','' 
            ###get server details#################################
            server=routesms_email_config_obj.get_mailserver_details(cr,SUPERID)
            ####################send mail to Odoo users#####################

            notification=routesms_email_config_obj.send_mail(FROM_MAIL, [TO_MAIL], [],\
                    attachment,SUBJECT,MESSAGE,extension,\
                     server,binary,'plain')
            
            
            if notification :
                  
                return {'type': 'ir.actions.act_window_close'}
             
            else :
                ''' Sending fail'''
                 
                raise osv.except_osv(_('Error'),
                                    _('Email Sending Failed! \n Contact Odoo Team'))
        else : 
                    
            raise osv.except_osv(_('Error'),
                                _('Email Sending Failed! \n Contact Odoo Team'))     

    def default_get(self, cr, uid, fields, context):
        '''Disable password reset if already reset '''
        
       
        international_user_obj = self.pool.get('int.user')
        india_user_obj = self.pool.get('ind.user')
        user_obj = self.pool.get('res.users')
        res={}
        
        user=user_obj.browse(cr,SUPERID,uid)
        if user.partner_type =='india'  :
            for ind_user in india_user_obj.browse(cr,SUPERID,\
                india_user_obj.search(cr,SUPERID,[('name','=',uid)])) :
                res.update({'reset_completed':True}) if ind_user.password_reset else res.update({'reset_completed':False})
            
            
        elif user.partner_type =='international' : 
            for int_user in international_user_obj.browse(cr,SUPERID,\
                international_user_obj.search(cr,SUPERID,[('name','=',uid)])) :
                res.update({'reset_completed':True}) if int_user.password_reset else res.update({'reset_completed':False})

        else :
            raise osv.except_osv(_('Error!'), _('Partner Type International or India Not Set!\n Contact HR Department'))
        if res.get('reset_completed') : 
            raise osv.except_osv(_('Error!'), _('Password Already Reset'))
            
        return res  
    
    def check_password_pattern(self,password): 
        '''check if password is valid '''
        pattern='^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{10,}$'
        
        if not re.match(pattern, password) : 
            raise osv.except_osv(_('Error'),_("Password Should Be at least 10 characters"+\
                                              "\nMust Contain uppercase letters: A-Z \n"+\
                                              "Must Contain lowercase letters: a-z\n"+\
                                              "Must Contain numbers: 0-9\n"+\
                                              "Special characters(like @#$%^&+=) not allowed"))
        return True 
    
    def password_hashing(self,password): 
        '''using  bcrypt moddule to hash password'''
        ###DOC####
        #https://pypi.python.org/pypi/bcrypt/2.0.0
        try : 
            
            hashed = bcrypt.hashpw(str(password), bcrypt.gensalt())
        except Exception as E: 
            raise osv.except_osv(_('Error'),_("Password Hashing  Failed/nContact Odoo Team ")) 
        return hashed       
       
        

    def reset_user_password(self,cr,uid,ids,context):
        ''' reset login password of current user'''
        
        user_obj = self.pool.get('res.users')
        international_user_obj = self.pool.get('int.user')
        india_user_obj = self.pool.get('ind.user')        
        
        
        obj=self.browse(cr,SUPERID,ids[0]) 
        if not obj.name : 
            raise osv.except_osv(_('Error'),_("Enter Password "))
        ###############check password pattern 
        self.check_password_pattern(obj.name)
        ###################hash password using bycrypt module@@@@@@@@@@@@@@@@@@@
        access_token=self.password_hashing(obj.name)
        user=user_obj.browse(cr,SUPERID,uid)

        if user.partner_type =='india' :
            for ind_user in india_user_obj.browse(cr,SUPERID,india_user_obj.search(cr,SUPERID,[('name','=',uid)])) :
                india_user_obj.write(cr,SUPERID,[ind_user.id],{'password':obj.name,'access_token':access_token,'password_reset':True}) 

        elif user.partner_type =='international' :
            for int_user in international_user_obj.browse(cr,SUPERID,international_user_obj.search(cr,SUPERID,[('name','=',uid)])) :
                international_user_obj.write(cr,SUPERID,[int_user.id],{'password':obj.name,'access_token':access_token,'password_reset':True})
                
        else : 
            raise osv.except_osv(_('Error!'), _('Partner Type International or India Not Set!\n Contact HR Department')) 
       
        try : 
            user_obj.write(cr,SUPERID,[uid],{'password':obj.name},{})
            #cr.execute(''' update res_users set password=%s where id=%s''',(obj.name,uid))
        except Exception as E: 
            raise osv.except_osv(_('Error'),_("Password Reset Failed\nContact Odoo Team "))
        
        ################send email to odoo user for username and updated password########
        self.send_username_newpassword_email(cr, uid, obj,user)
        
        return True

class account_invoice_holiday_wizard(osv.osv_memory):
    _name = 'account.invoice.holiday.wizard'
    _description = 'Selection of Holiday business verticals'

    _columns = {
        'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('other','Other')], 'Verticals', required=True),
                
#         'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('tour','TOURS & PACKAGES'), ('hotel','HOTEL BOOKING'), ('visa','VISA SERVICE'),\
#         ('rent','RENT A CAB SERVICE'),('insurance','INSURANCE SERVICE')], 'Verticals', required=False),
#                 

    }


    def submit(self,cr,uid,ids,context):
        
        user_obj=self.pool.get('res.users')
        
        if ids :
            holiday_vertical_val=self.browse(cr,uid,ids[0]).holiday_vertical_list
            if holiday_vertical_val :
                if user_obj.browse(cr,uid,uid).company_id.id == 3 :  
                    user_obj.write(cr,1,[uid],{'holiday_vertical_list':holiday_vertical_val})
                    
                    cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users AIR Ticket',))
                    air_group_id=cr.fetchall()
                    cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users Others',))
                    other_group_id=cr.fetchall()
                    
                    if holiday_vertical_val=='air' :
                        
                        if air_group_id:
                            
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_group_id[0],uid))
                            cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(air_group_id[0],uid))
                        
                        if other_group_id :
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(other_group_id[0],uid))
                    else :
                        
                        
                        
                        if air_group_id:
                            
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_group_id[0],uid))
                            
                        
                        if other_group_id :
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(other_group_id[0],uid))
                            cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(other_group_id[0],uid))
    
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }


class partner_custom_filter(osv.osv_memory):
    _name = 'partner.custom.filter'
    _description = 'Filter Partner'

    _columns = {
        'partner_name':fields.char('Enter Partner Name',required=False),
        'domain':fields.char('Enter Partner Domain',required=False),
        'email':fields.char('Enter Partner Email',required=False),
        'odoo_id':fields.char('Enter Odoo Id',required=False),
        'radio_domain':fields.boolean('Keep Domain',help='Mark To Remove Partner Value,Email,Odoo id'),
        'radio_email':fields.boolean('Keep Email',help='Mark To Remove Partner Value,Domain,Odoo id'),
        'radio_partner':fields.boolean('Keep Company',help='Mark To Remove Domain Value,Email,Odoo id'),
        'radio_odoo_id':fields.boolean('Keep Domain',help='Mark To Remove Partner Value,Domain,Email'),
    }
    
    _defaults={
        'radio_partner':False,               
        'radio_domain':False,
        'radio_email':False,
        'radio_odoo_id':False,
            }    

    def onchange_radio_partner(self, cr, uid, ids, radio_partner, context=None):
        
        if radio_partner: 
            return {'value': {'domain': '','email':'','odoo_id':'','radio_domain':False,'radio_email':False,\
                              'radio_odoo_id':False}}

        return {'value': {}}   


    
    def onchange_radio_domain(self, cr, uid, ids, radio_domain, context=None):

        if radio_domain:
            return {'value': {'partner_name': '','email':'','odoo_id':'','radio_partner':False,'radio_email':False,\
                              'radio_odoo_id':False}}

        return {'value': {}}

    def onchange_radio_email(self, cr, uid, ids, radio_email, context=None):
   
        if radio_email: 
            return {'value': {'partner_name': '','domain':'','odoo_id':'','radio_partner':False,'radio_domain':False,\
                              'radio_odoo_id':False}}

        return {'value': {}}   
    
    def onchange_radio_odoo_id(self, cr, uid, ids, radio_odoo_id, context=None):
   
        if radio_odoo_id: 
            return {'value': {'partner_name': '','domain':'','email':'','radio_partner':False,'radio_domain':False,\
                              'radio_email':False}}

        return {'value': {}}   

    def browse_partner(self,cr,uid,vals): 
        
        return  [partner for partner in self.pool.get('res.partner').browse(cr,uid,vals) ]
        

    def get_creation_date(self,cr,uid,partner):
        '''get creation date of partner lead '''
        crm_obj=self.pool.get('crm.lead') 
        crm_ids=[crm for crm in crm_obj.browse(cr,uid,crm_obj.search(cr,uid,[('partner_id','=',partner.id)]))]
        if not crm_ids :
            return 'No Lead Found'
            
        min_date=min([datetime.datetime.strptime(crm.create_date, "%Y-%m-%d %H:%M:%S") for crm in crm_ids]) 
        creation_datetime=[(datetime.datetime.strptime(crm.create_date, "%Y-%m-%d %H:%M:%S")+ datetime.timedelta(hours=5,minutes=30))\
                           .strftime("%Y-%m-%d %H:%M:%S") for crm in crm_ids \
                               if crm.create_date==min_date.strftime("%Y-%m-%d %H:%M:%S")]

        return creation_datetime[0] if creation_datetime else 'No Lead Found'

    def submit(self,cr,uid,ids,context):
        #uid=1
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window') 
        user_obj=self.pool.get('res.users')
        partner_obj=self.pool.get('res.partner')
        partner_dashboard_obj=self.pool.get('routsms.partner.filter')
                
        if ids :
            search_val=self.browse(cr,uid,ids[0])
            
            if search_val.partner_name and search_val.domain and search_val.email and  search_val.odoo_id:
                ###################CASE 1############
                
                cr.execute(''' select id,user_id from res_partner where name like %s 
                and domain like %s and email like %s and is_company=True and partner_sequence=%s''',\
                           ('%'+search_val.partner_name+'%',\
                            '%'+search_val.domain+'%','%'+search_val.email+'%',search_val.odoo_id))
                
                vals=cr.fetchall()
                
                ###check secondary contact details
          
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s and email like %s ''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                            partner_obj.browse(cr,SUPERID,vals_line) if  search_val.partner_name in partner.name and partner.partner_sequence == search_val.odoo_id] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()    
            
            elif search_val.partner_name and search_val.domain and search_val.email==False and search_val.odoo_id :
                ###################CASE 2############
                cr.execute(''' select id,user_id from res_partner where name like %s and domain like %s and is_company=True and partner_sequence=%s ''',\
                           ('%'+search_val.partner_name +'%','%'+search_val.domain+'%',search_val.odoo_id))
                vals=cr.fetchall()   
                
                ###check secondary contact details
          
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s''',\
                           ('%'+search_val.domain+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                            partner_obj.browse(cr,SUPERID,vals_line) if  search_val.partner_name in partner.name  and partner.partner_sequence == search_val.odoo_id] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()  

            elif search_val.partner_name and search_val.domain==False and search_val.email and search_val.odoo_id :
                ###################CASE 3############
                cr.execute(''' select id,user_id from res_partner where name like %s and email like %s and is_company=True and partner_sequence=%s''',\
                           ('%'+search_val.partner_name+'%','%'+search_val.email+'%',search_val.odoo_id))
                vals=cr.fetchall()    
                ###check secondary contact details
          
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where email like %s''',\
                           ('%'+search_val.email+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                            partner_obj.browse(cr,SUPERID,vals_line) if  search_val.partner_name in partner.name and partner.partner_sequence == search_val.odoo_id] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                       

            elif search_val.partner_name==False and search_val.domain and search_val.email and search_val.odoo_id:
                ###################CASE 4############
                
                cr.execute(''' select id,user_id from res_partner where  state='confirm' and domain like %s and email like %s and is_company=True and partner_sequence=%s''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%',search_val.odoo_id))
                vals=cr.fetchall()   
                
                ###check secondary contact details
          
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s and email like %s ''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                            partner_obj.browse(cr,SUPERID,vals_line) if partner.partner_sequence == search_val.odoo_id] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()              
                
            elif search_val.partner_name and search_val.domain and search_val.email and  search_val.odoo_id==False:
                ###################CASE 5 new############
                
                cr.execute(''' select id,user_id from res_partner where name like %s and domain like %s and email like %s and is_company=True''',\
                           ('%'+search_val.partner_name+'%',\
                            '%'+search_val.domain+'%','%'+search_val.email+'%'))
                vals=cr.fetchall()
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s and email like %s ''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                            partner_obj.browse(cr,SUPERID,vals_line) if  search_val.partner_name in partner.name   ] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()    
            
            elif search_val.partner_name and search_val.domain==False and search_val.email==False and search_val.odoo_id==False:
                ###################CASE 5############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and name like %s and is_company=True''',\
                           ('%'+search_val.partner_name+'%',))
                vals=cr.fetchall()                       


            elif search_val.partner_name==False and search_val.domain==False and search_val.email and search_val.odoo_id==False: 
                ###################CASE 6############
                cr.execute(''' select id,user_id from res_partner where state='confirm' and email like %s and is_company=True''',\
                           ('%'+search_val.email+'%',))
                vals=cr.fetchall()
                
#                 if not vals : 
# 
#                     cr.execute(''' select partner_id from res_partner_contact_line where email like %s''',('%'+search_val.email+'%',))
#                     vals_line=map(lambda x:x[0],cr.fetchall())
#                     if vals_line : 
# 
#                         cr.execute(''' select id,user_id from res_partner where state='confirm' and id=%s''',(vals_line[0],))
#                         vals=cr.fetchall()                 
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where email like %s ''',\
                           ('%'+search_val.email+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line) ] 

                    if not secondary_detail_partner_id : 
                        vals=primary_vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall() 

            
            elif search_val.partner_name==False and search_val.domain and search_val.email==False and search_val.odoo_id==False:
                ###################CASE 7############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and domain like %s and is_company=True ''',\
                           ('%'+ search_val.domain +'%',))
                vals=cr.fetchall()
                
                
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s ''',\
                           ('%'+search_val.domain+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line) ] 

                    if not secondary_detail_partner_id : 
                        vals=primary_vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                  


            elif search_val.partner_name==False and search_val.domain==False and search_val.email==False and search_val.odoo_id:
                ###################CASE 8############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and partner_sequence=%s and is_company=True ''',\
                           (search_val.odoo_id,))
                vals=cr.fetchall()

            elif search_val.partner_name and search_val.domain and search_val.email==False  and search_val.odoo_id==False :
                ###################CASE 1.1############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and name like %s and domain like %s and is_company=True ''',\
                           ('%'+search_val.partner_name+'%','%'+search_val.domain+'%'))
                vals=cr.fetchall()   

                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s ''',\
                           ('%'+search_val.domain+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line)\
                                                 if  search_val.partner_name in partner.name  ] 

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                 

            elif search_val.partner_name and search_val.domain==False and search_val.email and search_val.odoo_id==False :
                ###################CASE 1.2############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and name like %s and email like %s and is_company=True ''',\
                           ('%'+search_val.partner_name+'%','%'+search_val.email+'%'))
                vals=cr.fetchall()  
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where email like %s ''',\
                           ('%'+search_val.email+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line)\
                                                 if  search_val.partner_name in partner.name  ] 

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                      


            elif search_val.partner_name and search_val.domain==False and search_val.email==False and search_val.odoo_id :
                ###################CASE 1.3############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and name like %s and partner_sequence=%s and is_company=True ''',\
                           ('%'+search_val.partner_name+'%',search_val.odoo_id))
                vals=cr.fetchall()                                           
                
            elif search_val.partner_name==False and search_val.domain and search_val.email and search_val.odoo_id==False :
                ###################CASE 1.4############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and domain like %s and email like %s and is_company=True ''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                vals=cr.fetchall()  
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s and email like %s ''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in \
                                        partner_obj.browse(cr,SUPERID,vals_line)] 
                                                   

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                               

            elif search_val.partner_name==False and search_val.domain and search_val.email==False and search_val.odoo_id :
                ###################CASE 1.5############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and domain like %s and partner_sequence=%s and is_company=True ''',\
                           ('%'+search_val.domain+'%',search_val.odoo_id))
                vals=cr.fetchall()      
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where domain like %s ''',\
                           ('%'+search_val.domain+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line)\
                                                 if  partner.partner_sequence == search_val.odoo_id  ] 

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                   
                                                                    
            elif search_val.partner_name==False and search_val.domain==False and search_val.email and search_val.odoo_id :
                ###################CASE 1.6############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and email like %s and partner_sequence=%s and is_company=True ''',\
                           ('%'+search_val.email+'%',search_val.odoo_id))
                vals=cr.fetchall()                                                                        
                ###check secondary contact details
                
                primary_vals=[partner_id[0] for partner_id in vals if vals]
                
 
                cr.execute(''' select partner_id from res_partner_contact_line where email like %s ''',\
                           ('%'+search_val.email+'%',))
                
                vals_line=map(lambda x:x[0],cr.fetchall())
                if vals_line : 
                    secondary_detail_partner_id=[ partner.id for partner in partner_obj.browse(cr,SUPERID,vals_line)\
                                                 if  partner.partner_sequence == search_val.odoo_id  ] 

                    if not secondary_detail_partner_id : 
                        vals=vals
                        
                    else : 
                        
                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id in %s''',\
                                   (tuple( set(secondary_detail_partner_id +primary_vals) ),))
                        vals=cr.fetchall()                                  
            
                
            else : 
                
                raise osv.except_osv(_('Sorry!'),_("Invalid Criteria"))
            

            cr.execute(''' delete  from routsms_partner_filter''')
                
            if vals :
                for values in vals :
                    partner_record=partner_obj.browse(cr,SUPERID,values[0])
                    partner_is_active='YES' if partner_record.active else 'NO' 
                    partner_type=user_obj.browse(cr,SUPERID,values[1]).partner_type
                    
                    partner_display_name=partner_obj.browse(cr,SUPERID,values[0]).name
                    crm_lead_state=partner_obj.browse(cr,SUPERID,values[0]).crm_lead_state
                    current_partner_type=user_obj.browse(cr,uid,uid).partner_type
                    creation_date=self.get_creation_date(cr,uid,partner_record)
                    if not partner_type or not current_partner_type: 
                        raise osv.except_osv(_('Validation Error!'),_("Partner Type Not Set\nContact HR Department"))
                    
                    if partner_type==current_partner_type :
                            
                        cr.execute(''' insert into routsms_partner_filter(name,user_id,lead_status,is_active,creation_date) VALUES(%s,%s,%s,%s,%s)''',(partner_display_name,values[1],crm_lead_state,partner_is_active,creation_date))
           
                    else : 
                        raise osv.except_osv(_('Restricted!'),_("Client Belongs To Other Department"))

                result = mod_obj.get_object_reference(cr, uid, 'routesms', 'action_routesms_partner_filter')
                id = result and result[1] or False
                result = act_obj.read(cr, uid, [id], context=context)[0]
                return result
                        
                
            else :
    #            
                raise osv.except_osv(_('Sorry!'),_("No Record Found")) 

        raise osv.except_osv(_('Sorry!'),_("No Record Found"))


class pnr_report_wizard(osv.osv_memory):
    _name = 'pnr.report.wizard'
    _description = 'Print PNR report from Wizard'

    def print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        context={}
        if context is None:
            
            context = {}
        
        
        
        datas= {
                  'model':'pnr.report',
                  'id': ids and ids[0] or False,
                 
                  
                 },
        
        return {'type': 'ir.actions.report.xml', 'report_name': 'routesms.report_pnr', 'datas': datas,'nodestroy': True}


class origin_report_wizard(osv.osv_memory):
    _name = 'origin.report.wizard'
    _description = 'Print ORIGIN report from Wizard'

    def print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        context={}
        if context is None:
            
            context = {}
        
        
        
        datas= {
                  'model':'source.document.report',
                  'id': ids and ids[0] or False,
                 
                  
                 },
        
        return {'type': 'ir.actions.report.xml', 'report_name': 'routesms.report_source', 'datas': datas,'nodestroy': True}



class crm_make_sale(osv.osv_memory):
    _name = "crm.make.sale"
    _inherit = "crm.make.sale"
    _description = "Accounting Report"

    def generate_auto_pricelist(self,cr,uid,partner): 
        ''' auto generate pricelist'''
        product_pricelist_obj=self.pool.get('product.pricelist')
        user_obj=self.pool.get('res.users')
        if partner : 
            user=user_obj.browse(cr,uid,uid)
            pricelist=product_pricelist_obj.search(cr,uid,[('company_id','=',user.company_id.id),\
                                                 ('currency_id','=',user.company_id.currency_id.id)])
            
            if pricelist : 
                if len(pricelist) >1 : 
                    raise osv.except_osv(_('Invalid Action!'), _('Mulitple Pricelist configured  for same currency!'))
                return pricelist[0]
            
        raise osv.except_osv(_('Invalid Action!'), _('No Pricelist Found!'))
    


    def makeOrder(self, cr, uid, ids, context=None):
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        # update context: if come from phonecall, default state values can make the quote crash lp:1017353
        context = dict(context or {})
        context.pop('default_state', False)        
        
        case_obj = self.pool.get('crm.lead')
        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        data = context and context.get('active_ids', []) or []
        for make in self.browse(cr, uid, ids, context=context):
            partner = make.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                    ['default', 'invoice', 'delivery', 'contact'])
            
            ########custom method for auto pricelist selection##########
            
            #pricelist = partner.property_product_pricelist.id
            pricelist=self.generate_auto_pricelist(cr,uid,partner)
            
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            for case in case_obj.browse(cr, uid, data, context=context):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    payment_term = partner.property_payment_term and partner.property_payment_term.id or False
                    partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                            ['default', 'invoice', 'delivery', 'contact'])
                    ########custom method for auto pricelist selection##########    
                    #pricelist = partner.property_product_pricelist.id
                    
                    pricelist=self.generate_auto_pricelist(cr,uid,case.partner_id)
                if False in partner_addr.values():
                    raise osv.except_osv(_('Insufficient Data!'), _('No address(es) defined for this customer.'))

                vals = {
                    'origin': _('Opportunity: %s') % str(case.id),
                    'section_id': case.section_id and case.section_id.id or False,
                    'categ_ids': [(6, 0, [categ_id.id for categ_id in case.categ_ids])],
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.datetime.now(),
                    'fiscal_position': fpos,
                    'payment_term':payment_term,
                }
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or uid
                new_id = sale_obj.create(cr, uid, vals, context=context)
                sale_order = sale_obj.browse(cr, uid, new_id, context=context)
                case_obj.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
                new_ids.append(new_id)
                message = _("Opportunity has been <b>converted</b> to the quotation <em>%s</em>.") % (sale_order.name)
                case.message_post(body=message)
            if make.close:
                case_obj.case_mark_won(cr, uid, data, context=context)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids)<=1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids
                }
            return value


class sale_purchase_report_wizard(osv.osv_memory):
    _name = 'sale.purchase.report.wizard'
    _description = 'Print Sale Purchase report from Wizard'

    _columns = {
        'report_type': fields.selection([('sale','Sale Invoice'), ('sale_refund','Sale Refund'),('purchase','Purchase Invoice'),('purchase_refund','Purchase Refund')] ,'Report Type'),
        'type': fields.selection([('india','India'),('int','International'), ('all','All')] ,'Type'),
        'date_from':fields.date('Date From'),
        'date_to':fields.date('Date To'),
        }


    def print_report(self, cr, uid, ids, context):
        if context is None:
            context = {}
        
   #     import ipdb;ipdb.set_trace()
        if context.get('date_from') and context.get('date_to')==False : 
            raise osv.except_osv(_('Invalid Action!'), _('Please Select Date To '))

        elif context.get('date_to') and context.get('date_from')==False : 
            raise osv.except_osv(_('Invalid Action!'), _('Please Select Date From '))
        
        elif context.get('date_from')==False and context.get('date_to')==False:
            pass
        
        elif context.get('date_from') >=context.get('date_to') : 
            raise osv.except_osv(_('Invalid Action!'), _('Invalid Date Selection '))

        else : 
            pass
        
        
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'routesms.report_sale_purchase'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]

        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.pool['report'].get_action(cr, uid, [], 'routesms.report_sale_purchase', data=datas, context=context)





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
