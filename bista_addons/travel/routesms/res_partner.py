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
SUPERUSERID=1
SUPERACCOUNTUSER=[327,321]#sushma & shailesh##

class res_partner(osv.osv):
    _inherit = 'res.partner'


    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        user_obj=self.pool.get('res.users')
          
        res = super(res_partner, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form': 
            if uid ==SUPERUSERID or uid in SUPERACCOUNTUSER: 
                return res
             
            doc = etree.XML(res['arch'])
            
            for node in doc.xpath("//field[@name='email']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]] ,"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)

            for node in doc.xpath("//field[@name='phone']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]],"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)

            for node in doc.xpath("//field[@name='mobile']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]],"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)
                
            for node in doc.xpath("//field[@name='partner_line']"):
                user_id=str(uid)
                
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ],["state","!=","initial"]] ,"readonly": [["state","!=","initial"]] }'
                node.set('modifiers',modifier)                
            
            
            
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
        pattern='[^@]+@[^@]+\.[^@]+'
        
        for email_val in vals : 
            
            if not re.match(pattern, email_val) : 
                return False

        return True
    
    def collect_email_data(self,cr,uid,email,additional_email): 
        '''reformat email and additional email data '''
        
        email_list=[ x['email'] for x in map(lambda x:x[2],additional_email) ]
        email_list.append(email)
        
        for email_val in  email_list :
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
                              
              
              #'flag':fields.boolean('FLag'),
            #  'flag_function':fields.function(_restricted_view, string='Restricted View', type='char'),
              }

    _defaults = {
                
           #    'vertical':default_vertcal_id,
               'state': 'initial',
               'is_company':True,
               
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
                                return partner
                    
                            elif postpaid :
                                vals.update({'postpaid':True})
                                
                                partner = super(res_partner, self).create(cr, 1, vals, context)
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
                            return partner
                
                        elif postpaid :
                            vals.update({'postpaid':True})
                            
                            partner = super(res_partner, self).create(cr, 1, vals, context)
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


    def write(self, cr, uid, ids, vals, context=None):
#         vals['vertical']=self.pool.get('res.users').browse(cr, uid, uid).company_id.vertical.id

        ###############email validation############
        
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
            
        res_set = super(res_partner, self).write(cr, uid, ids,vals, context)
        '''Overide method to do assign saleperson & account type automatically '''
        res={}
    
        
        if vals :
            ###############check if BM,Account type is empty#####################
            
#             for key in vals.iterkeys(): 
#                 if vals.has_key('user_id') : 
#                     if not vals[key] : 
#                         raise osv.except_osv(_('Error!'), _('Record cannot be updated without Saleperson.'))
#                 elif vals.has_key('prepaid') : 
#                      
                        
            
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

# Copy functionality


    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        ''' Restrict Users to duplicate partners'''
#        res= super(res_partner, self).copy(cr, uid, id, default, context=context)
        raise osv.except_osv(_('Validation Error!'), _('Partner Cannot Be Duplicated.'))




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
        #connection =check_internet_connection('http://erp.routesms.com')  
        connection =check_internet_connection('http://192.168.0.12:8069')
        if not connection : 
            raise osv.except_osv(_('No Internet Connection'),
                                _(' Contact IT Team')) 
        
        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = [To_MAIL],
            cc_addr_list = ['avinash@29threeholidays.com'], 
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




    def validate_partner(self,cr,uid,ids,context): 
        ''' Confirm Partner'''
         
        obj_sequence=self.pool.get('ir.sequence')
        #obj_sequence.search(cr,uid,[('name','=',name)])
        vals={}
        ###check dublicate email id#####
        partner=self.browse(cr,uid,ids[0])
        
        if partner.email : 

            not_unique_email=self.check_partner_email(cr,uid,[partner.email])
            if not not_unique_email : 
                raise osv.except_osv(_('Error!'), _('Email Id Already Exist !!'))               


        seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
        if vals.get('partner_sequence', False) == False:
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
            self.write(cr,uid,ids,{'state':'confirm','partner_sequence':vals['partner_sequence']})
             
        contact_id=self.search(cr,uid,[('parent_id','=',ids[0])])
        if contact_id :
             
     
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
            self.write(cr,uid,contact_id,{'state':'confirm','partner_sequence':vals['partner_sequence']})            
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
                self.unlink(cr,uid,[contact_id],context)
                 
            self.unlink(cr,uid,ids,context)
            
         
        except Exception as E : 
        
            raise osv.except_osv(_('ERROR'),
                                _('Deleting  Partner Document Failed ! \n Contact Odoo Team'))
            

        notification=sendmail(
            from_addr    = FROM_MAIL,                               
            to_addr_list = [To_MAIL],
            cc_addr_list = ['avinash@29threeholidays.com'], 
            subject      = SUBJECT, 
            message      = MESSAGE, 
            login        = 'ar@routesms.com', 
            password     = 'Routesms@05r'
              
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


    def reject_partner(self,cr,uid,ids,context): 
        ''' Reject Partner'''
        if not self.browse(cr,uid,ids[0]).comment : 
            raise osv.except_osv(_('Validation Error'),
                                _('Kindly specify reason for rejection'))             
        self.write(cr,uid,ids,{'state':'cancel'})            
        
        notification=self.send_cancel_mail(cr, uid, ids, context=None)
        
        if notification : 
            return True
        
        ''' Sending fail'''
        
        raise osv.except_osv(_('ERROR'),
                            _('Email Sending Failed! \n Contact Odoo Team'))        
    



class res_partner_contact_line(osv.osv): 
    
    _name='res.partner.contact.line'
    _description='Add Multiple Email Details'
    
    _columns={
              'partner_id': fields.many2one('res.partner', 'Additional Contact Information', ondelete='cascade'),
              'email':fields.char('Email'),
              'domain':fields.char('Domain'),
              'send_email':fields.boolean('Send Email'),
                                          
              }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
