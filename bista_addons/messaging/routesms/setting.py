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




class int_user(osv.osv):
    _name = 'int.user'
    _description='List of International users'
    _rec_name = 'username'
    _order = "username"
    
    _columns={
              
            'name':fields.many2one('res.users','International Users'),
            'active':fields.boolean('Active'),
            'username':fields.char('UserName'),
            'password':fields.char('Password'),
            'access_token':fields.char('Access Token'),
            'password_reset':fields.boolean('Password Reset ?'),
            
            }
    _defaults={
               'password_reset':False,
               } 
           

int_user()



class ind_user(osv.osv):
    _name = 'ind.user'
    _description='List of Indian users'
    _rec_name = 'username'
    _order = "username"
    
    _columns={
              
            'name':fields.many2one('res.users','Indian User'),
            'active':fields.boolean('Active'),
            'username':fields.char('UserName'),
            'password':fields.char('Password'),
            'access_token':fields.char('Access Token'),
            'password_reset':fields.boolean('Password Reset ?'),            
           

    }
    _defaults={
               'password_reset':False,
               }                

ind_user()


class settings(osv.osv):
    _name = 'settings'
    _description='List of custom settings'

    
    _columns={
              
            'name':fields.char('Name',size=30,required=True),
            'code':fields.char('Code',size=10,required=True),
            'active':fields.boolean('Active'),
            }
    
    _defaults={
               'active':True
               
               }
    
#     def create(self,cr,uid,vals,context): 
#         
#         if vals.get('name') :
#             cr.execute('''select name from settings ''')
#             settings_name=map(lambda x:x[0],cr.fetchall())
#             if vals.get('name') in settings_name : 
#                 raise osv.except_osv(_('Validation Error !'), _("%s Already Exist")%vals.get('name'))
#         
#         if vals.get('code') :
#             cr.execute('''select code from settings ''')
#             settings_code=map(lambda x:x[0],cr.fetchall())
#             if vals.get('code') in settings_code : 
#                 raise osv.except_osv(_('Validation Error !'), _("Code %s Already Exist")%vals.get('code'))
#             
#         return super(settings,self).create(cr,uid,vals,context)
# 
# 
#     def write(self,cr,uid,ids,vals,context): 
#         
#         if vals.get('name') :
#             cr.execute('''select name from settings where id!=%s''',(ids[0],))
#             settings_name=map(lambda x:x[0],cr.fetchall())
#             if vals.get('name') in settings_name : 
#                 raise osv.except_osv(_('Validation Error !'), _("%s Already Exist")%vals.get('name'))
#         
#         if vals.get('code') :
#             cr.execute('''select code from settings where id!=%s''',(ids[0],))
#             settings_code=map(lambda x:x[0],cr.fetchall())
#             if vals.get('code') in settings_code : 
#                 raise osv.except_osv(_('Validation Error !'), _("Code %s Already Exist")%vals.get('code'))
#             
#         return super(settings,self).create(cr,uid,vals,context)
# 
#     def unlink(self,cr,uid,ids,context): 
#         raise osv.except_osv(_('Restricted !'), _('Settings Cannot Be Removed \nContact Odoo Team.'))
# 
#     def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
#         ''' Restrict Users to duplicate settings'''
# #        res= super(res_partner, self).copy(cr, uid, id, default, context=context)
#         raise osv.except_osv(_('Restricted !'), _('Settings Cannot Be Duplicated \nContact Odoo Team.'))



class user_settings(osv.osv):
    _name = 'user.settings'
    _description='Assign rules to system users'

    
    def _store_name(self,cr, uid, ids, name, args, context=None):
       
        ''' store odoo user name'''

        res={}
        
        
        for user_settings in self.browse(cr, uid, ids) :
            
            
            
            if user_settings.user_id : 
                
                
                res[user_settings.id]=user_settings.user_id.name

            else : 
                
                res[user_settings.id]='No User Found'
        return res

    
    _columns={
              
            'name':fields.function(_store_name,string='Name',size=30,type='char',store=True),
            'user_id':fields.many2one('res.users','User'),
            'active':fields.boolean('Active'),
            'rule': fields.many2many('settings', 'settings_user_rel',
                      'user_settings_id', 'settings_id', 'Rule'),
            'count_flag':fields.boolean('Count Flag'),
            'count':fields.integer('Count',help='Count Limit To Add Users On Partner Page'),
            'readonly_flag':fields.boolean('Readonly Flag'),
            
            }
    
    _defaults={
               'active':True,
               'count_flag':False,
               'count':5,
               'readonly_flag':False,
               
               }

    def onchange_rule(self,cr,uid,ids,rule,context):
        settings_obj=self.pool.get('settings')
        vals={}

        if rule[-1][-1] :
            for rule_id in rule[-1][-1] : 
                if settings_obj.browse(cr,uid,rule_id).name == 'Add User Limit' : 
                    vals.update({'count_flag':True})
        
        else : 
            vals.update({'count_flag':False})
            
        return {'value':vals}

# 
#     
#     def create(self,cr,uid,vals,context): 
#         user_obj=self.pool.get('res.users')
#         if vals.get('user_id') :
#             cr.execute('''select user_id from user_settings ''')
#             user_list=map(lambda x:x[0],cr.fetchall())
#             if vals.get('user_id') in user_list : 
#                 raise osv.except_osv(_('Validation Error !'), _("This User Already Exist"))
#             
#         if vals.get('user_id') : 
#             vals.update({'name':user_obj.browse(cr,uid,vals.get('user_id')).name})  
#             
#         vals.update({'readonly_flag':True})  
#         return super(user_settings,self).create(cr,uid,vals,context)
# 
# 
#     def write(self,cr,uid,ids,vals,context): 
#         
#         if vals.get('user_id') :
#             cr.execute('''select user_id from user_settings where id!=%s''',(ids[0],))
#             user_list=map(lambda x:x[0],cr.fetchall())
#             if vals.get('name') in user_list : 
#                 raise osv.except_osv(_('Validation Error !'), _("This User Already Exist"))
#         
#  
#         return super(user_settings,self).create(cr,uid,vals,context)
# 
#     def unlink(self,cr,uid,ids,context): 
#         raise osv.except_osv(_('Restricted !'), _('User Settings Cannot Be Removed \nContact Odoo Team.'))
# 
#     def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
#         ''' Restrict Users to duplicate settings'''
# #        res= super(res_partner, self).copy(cr, uid, id, default, context=context)
#         raise osv.except_osv(_('Restricted !'), _('User Settings Cannot Be Duplicated \nContact Odoo Team.'))


class server(osv.osv):
    _name = 'server'
    _description='List of servers'
    _rec_name = 'server'
    
    _columns={
              
            'name':fields.char('URL',required=True),
            'server':fields.char('Server Name',required=True),
            'active':fields.boolean('Active'),
            'locality':fields.selection([('local','Local'),('international','International')],'Server Locality'),
            'type':fields.selection([('general','General'),('reseller','Reseller'),\
                                     ('distributor','Distributor')],'Server Type'),
            
            }
    
    _defaults={
               'active':True
               }



   
#     def create(self,cr,uid,vals,context): 
#         
#         if vals.get('url') :
#             cr.execute('''select url from server ''')
#             url=map(lambda x:x[0],cr.fetchall())
#             if vals.get('url') in url : 
#                 raise osv.except_osv(_('Validation Error !'), _("%s Already Exist")%vals.get('url'))
# 
#             
#         return super(server,self).create(cr,uid,vals,context)
# 
# 
#     def write(self,cr,uid,ids,vals,context): 
#         
#         if vals.get('url') :
#             cr.execute('''select url from server where id!=%s''',(ids[0],))
#             url=map(lambda x:x[0],cr.fetchall())
#             if vals.get('url') in url : 
#                 raise osv.except_osv(_('Validation Error !'), _("%s Already Exist")%vals.get('url'))
#             
#         return super(settings,self).create(cr,uid,vals,context)
# 
#     def unlink(self,cr,uid,ids,context): 
#         raise osv.except_osv(_('Restricted !'), _('Settings Cannot Be Removed \nContact Odoo Team.'))
# 
#     def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
#         ''' Restrict Users to duplicate settings'''
# #        res= super(res_partner, self).copy(cr, uid, id, default, context=context)
#         raise osv.except_osv(_('Restricted !'), _('Settings Cannot Be Duplicated \nContact Odoo Team.'))
