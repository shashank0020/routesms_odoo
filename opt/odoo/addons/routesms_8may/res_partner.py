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

class res_partner(osv.osv):
    _inherit = 'res.partner'

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
        
        
        

    _columns = {
              
              'partner_sequence':fields.char('Customer ID', size=15),
              'prepaid':fields.boolean('Prepaid',required=False),
              'postpaid':fields.boolean('Postpaid',required=False),
              'tan':fields.char('TAN', size=10),
              'pan':fields.char('PAN', size=10),
              'vat': fields.char('VAT', help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
              'vertical':fields.many2one('vertical.business', 'Vertical',readonly=True),
              'email_1':fields.char('Email 1'),
              'email_2':fields.char('Email 2'),
              'email_3':fields.char('Email 3'),
              'email_4':fields.char('Email 4'),
              'crm_lead_state':fields.function(_partner_lead, string='Lead Status', type='char'),
              'partner_type': fields.selection([('india','India'), ('international','International')] ,'Type'),
              'routesms_cust_id':fields.char('Routesms Customer Id'),
              'routesms_remark':fields.char('Routesms Remark'),
              'company_registery':fields.char('Service Tax Reg.'),
              
              #'flag':fields.boolean('FLag'),
            #  'flag_function':fields.function(_restricted_view, string='Restricted View', type='char'),
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
        
        obj_sequence=self.pool.get('ir.sequence')
        #obj_sequence.search(cr,uid,[('name','=',name)])
        seq_no = obj_sequence.next_by_id(cr, uid, 162, context=context)
        if vals.get('partner_sequence', False) == False:
            vals['partner_sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
        
        
###################################CUSTOMER VALIDATIONS#########################  
        if vals['customer'] :
            if vals.has_key('parent_id'):
                if vals.get('parent_id') :
                    partner_val=self.browse(cr,uid,vals['parent_id'])
                    user_id=partner_val.user_id.id
                    prepaid=partner_val.prepaid
                    postpaid=partner_val.postpaid
                    
                    if user_id :
                        vals.update({'user_id':user_id})
                        if prepaid and postpaid :
                            raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))
                        
                        elif prepaid :
                            vals.update({'prepaid':True})
                            partner = super(res_partner, self).create(cr, uid, vals, context)
                            return partner
                
                        elif postpaid :
                            vals.update({'postpaid':True})
                            partner = super(res_partner, self).create(cr, uid, vals, context)
                            return partner
                            
                        else :
                            raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                    raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))


                else :
                    
                    prepaid=vals.get('prepaid')
                    postpaid=vals.get('postpaid')                
                    
                    if vals.has_key('user_id'):
                        if vals.get('user_id') :
                            if prepaid and postpaid :
                                raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
    
                            elif prepaid :
                            
                                partner = super(res_partner, self).create(cr, uid, vals, context)
                                return partner                        
                            
                            
                            elif postpaid :
                                partner = super(res_partner, self).create(cr, uid, vals, context)
                                return partner      
    
                            else :
                                raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.'))
                            
                    raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))                                          
    
                
            
            else :
                
                prepaid=vals.get('prepaid')
                postpaid=vals.get('postpaid')       
                      
                if vals.has_key('user_id'):
                    if vals.get('user_id') :
    
                        if prepaid and postpaid :
                            raise osv.except_osv(_('Error!'), _('Partner can either be Prepaid or Postpaid.'))                        
        
                        elif prepaid :
                        
                            partner = super(res_partner, self).create(cr, uid, vals, context)
                            return partner                        
                        
                        
                        elif postpaid :
                            partner = super(res_partner, self).create(cr, uid, vals, context)
                            return partner      
        
                        else :
                            raise osv.except_osv(_('Error!'), _('Plese select Prepaid/Postpaid.')) 
    
    
                
                raise osv.except_osv(_('Error!'), _('Record cannot be created without Saleperson.'))
                #partner = super(res_partner, self).create(cr, uid, vals, context)
        else :
            
            partner = super(res_partner, self).create(cr, uid, vals, context)
            return partner             
            
            ##################################CUSTOMER VALIDATIONS STOPS##########


    def write(self, cr, uid, ids, vals, context=None):
        
        res_set = super(res_partner, self).write(cr, uid, ids,vals, context)
        '''Overide method to do assign saleperson & account type automatically '''
        res={}
    
        
        if vals :
            if vals.get('user_id') :
                
                contact_id=self.search(cr,uid,[('parent_id','=',ids[0])])
                
                if contact_id :
                    for val in vals.iterkeys() :
                        if val in ['user_id','prepaid','postpaid'] :
                            res.update({val:vals[val]})
                    #cr.execute('''update res_partner set name='pppp' where id=%s''',(contact_id[0],))
                    
                    return self.write(cr,uid,contact_id,res)
        
        return res_set


    
    _defaults = {
                
               'vertical':default_vertcal_id,
               } 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
