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

SUPERUSERID=1

class res_users(osv.osv):
    _inherit = 'res.users'
    
    
    _columns={
              
              #'employee_id':fields.function(default_emp_id,string='Employee User',type='many2one',relation='hr.employee',store=True),
              'partner_type': fields.selection([('india','India'), ('international','International')] ,'Type'),
              'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('other','Other'), ], 'Verticals', required=False),
                
#               'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('tour','TOURS & PACKAGES'), ('hotel','HOTEL BOOKING'), ('visa','VISA SERVICE'),\
#                 ('rent','RENT A CAB SERVICE'),('insurance','INSURANCE SERVICE')], 'Verticals', required=False),
              
              }
    
#     _defaults={
#                
#                'partner_type':'india'
#                }



    def preference_save(self, cr, uid, ids, context=None):
        ''' Overide method to hide/unhide travel menu from accounting'''
        #import ipdb;ipdb.set_trace()
        if self.browse(cr,uid,uid).company_id.id == 3 :
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday user',))
            group_id=cr.fetchall()
            cr.execute(''' select id from res_groups where name=%s''',('Activate Invoice Line',))
            active_invoice_line_group=cr.fetchall()
            
            if group_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(group_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(group_id[0],uid))
            
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))            
                    
            if active_invoice_line_group :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(active_invoice_line_group[0],uid))
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                    
                    

                
        else :
            
            cr.execute(''' select id from res_groups where name=%s''',('Activate Invoice Line',))
            active_invoice_line_group=cr.fetchall()
            if active_invoice_line_group :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(active_invoice_line_group[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(active_invoice_line_group[0],uid))
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                    
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users AIR Ticket',))
            air_ticket_group=cr.fetchall()
            
            if air_ticket_group :
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_ticket_group[0],uid))

            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                
                
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users Others',))
            non_air_ticket_group=cr.fetchall()
            if non_air_ticket_group :
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(non_air_ticket_group[0],uid))

            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday user',))
            group_id=cr.fetchall()
            if group_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(group_id[0],uid))
            
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.')) 
            

        
        #report baner loop
        
        if self.browse(cr,uid,uid).company_id.id in [8,9,10,11] :

            #active report baner
            cr.execute(''' select id from res_groups where name=%s''',('Activate Report Baner',))
            baner_active_id=cr.fetchall()
            if baner_active_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_active_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(baner_active_id[0][0],uid))
                    
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))

            cr.execute(''' select id from res_groups where name=%s''',('Deactivate Report Baner',))
            baner_deactive_id=cr.fetchall()
            if baner_deactive_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_deactive_id[0],uid))
            
                                    
                
        else : 
            
            #deactive report baner
            cr.execute(''' select id from res_groups where name=%s''',('Deactivate Report Baner',))
            baner_deactive_id=cr.fetchall()
            if baner_deactive_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_deactive_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(baner_deactive_id[0][0],uid))
                    
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))  


            cr.execute(''' select id from res_groups where name=%s''',('Activate Report Baner',))
            baner_active_id=cr.fetchall()
            if baner_active_id :                      
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_active_id[0],uid))
            
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }


    def send_mail_to_confirm_user(self, cr, uid,user_id ):
        ''' send notification email to accounts team once new user created'''
        partner_obj=self.pool.get('res.partner')
        routesms_email_config_obj=self.pool.get('send.email.with.attactment')
        try : 
            
            assert user_id,'No User Account Record Found\nContact Odoo Team' 
            user=self.browse(cr,uid,user_id)
            FROM_MAIL='sandhya@routesms.com' #odoo user will receive email from HR EMAIL ID
            TO_BCC=['sandhya@routesms.com']
            ##check receiver mail addres
            email_validation=partner_obj.email_validation(cr,uid,[FROM_MAIL])
            assert email_validation,"Invalid Sender's Email Id \n Contact HR Team"
            TO_MAIL=['anc@routesms.com','internalauditorvendor@routesms.com','internalauditor@routesms.com']
            email_validation=partner_obj.email_validation(cr,uid,TO_MAIL)
            assert email_validation,"Invalid Receiver's Email Id \n Contact HR Team"

            SUBJECT = '''Validate Odoo User Account For {}'''.format(user.name)    
            MESSAGE = '''Hello Accounts Team,\n\nKindly Validate Odoo User Account\nNew Odoo account details as follows: \n\nName: {}\nUsername: {}\nAllowed Companies:{}\nPartner Type:{}\n\nThanks & Regards \n\n{}
            ''' .format(user.name,user.login,[str(user_rec.name) for user_rec in user.company_ids],user.partner_type,'HR DEPARTMENT') 
                          
            ###############ATTACHED FILES########################
            attachment,binary,extension='','','' 
            ###get server details#################################
            server=routesms_email_config_obj.get_mailserver_details(cr,uid)
            ####################send mail to account users#####################
            
            notification=routesms_email_config_obj.send_mail(FROM_MAIL, TO_MAIL,TO_BCC ,\
                    attachment,SUBJECT,MESSAGE,extension,\
                     server,binary,'plain')
            
            assert notification,'Email Sending Failed! \n Contact Odoo Team'
            return {'type': 'ir.actions.act_window_close'}

        except Exception as E : 
            
            if not E.message : 
                E.message=E.value
                
            raise osv.except_osv(_('Error'),
                                _('{}').format(E.message))            

        return True



    def create(self,cr,uid,vals,context): 
        
        partner_obj=self.pool.get('res.partner')
        ind_user_obj=self.pool.get('ind.user')
        int_user_obj=self.pool.get('int.user')
        
        #########login has to be email address
        try : 
            
            if vals.get('login') :
                email_validation=partner_obj.email_validation(cr,uid,[vals.get('login')])
                assert email_validation,'Invalid Email Address'
                assert vals.get('partner_type'),'Select Partner Type'
                user_id=super(res_users,self).create(cr,uid,vals,context)
                if vals.get('partner_type')=='india' : 
                    ind_user_obj.create(cr,uid,{'username':vals['name'],'name':user_id,'active':vals.get('active',False)})
                    
                else : 
                    int_user_obj.create(cr,uid,{'username':vals['name'],'name':user_id,'active':vals.get('active',False)})
                    #####notify accounts team to validate account###############
                    self.send_mail_to_confirm_user(cr,SUPERUSERID,user_id) 
                    
                return user_id                       
                    
        except Exception as E :
            
            if not E.message : 
                E.message=E.value             
            raise osv.except_osv(_('Error'), _('{}').format(E.message))
   
    
    
    def write(self,cr,uid,ids,vals,context): 
        
        
        
        ind_user_obj=self.pool.get('ind.user')
        int_user_obj=self.pool.get('int.user')
    #	import ipdb;ipdb.set_trace()    
        user_val=self.browse(cr,uid,ids[0])    
        if vals.has_key('partner_type') :
            if not vals.get('partner_type') :
                raise osv.except_osv(_('Error!'), _('Select Partner Type.'))

            else : 
                if vals.get('partner_type')=='india' : 
                    ind_user_obj.create(cr,uid,{'username':user_val.name,'name':ids[0],'active':vals.get('active',True)})
                    int_user_obj.unlink(cr,uid,int_user_obj.search(cr,uid,[('name','=',ids[0])]))
                    
                else : 
                    int_user_obj.create(cr,uid,{'username':user_val.name,'name':ids[0],'active':vals.get('active',True)})
                    ind_user_obj.unlink(cr,uid,ind_user_obj.search(cr,uid,[('name','=',ids[0])]))
                        
                
    
        return super(res_users,self).write(cr,uid,ids,vals,context)
    

