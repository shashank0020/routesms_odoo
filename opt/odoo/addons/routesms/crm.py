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

class crm_case_stage(osv.osv):   
    _inherit = "crm.case.stage"
    _description = "Stage of case"
    
    _columns = {
        'is_dnd': fields.boolean('Is DND'),
        }

    _defaults={
        'is_dnd': False,
               }
    
    def unlink(self, cr, uid, ids, context=None):
        ''' Restrict user to delete stage'''
        raise osv.except_osv(_('Error!'), _('CRM Stages Cannot Be Deleted\nContact Odoo Team'))

class crm_lead2opportunity_partner(osv.osv_memory):
  #  _name = 'crm.lead2opportunity.partner'
    _description = 'Lead To Opportunity Partner'
    _inherit = 'crm.lead2opportunity.partner'


    def check_crm_for_duplicate_opportunity(self,cr,uid,ids,context):
        '''If opportunity already created then throw exception  '''
        
        lead_obj = self.pool.get('crm.lead')
        partner_vals=lead_obj.browse(cr,uid,context.get('active_id'))
        ###search for all partner whose state !=fresh lead
        if partner_vals.partner_id.state !='confirm' : 
            return 'pending partner'
        
        cr.execute ('''select id from crm_lead where partner_id=%s and stage_id is NOT NULL ''',(partner_vals.partner_id.id,))
        partner_ids_with_stages=map(lambda x:x[0],cr.fetchall())
        if partner_ids_with_stages : 
            
            #partner_ids_with_stages=lead_obj.search(cr,uid,[('stage_id','!=',False),('partner_id','=',partner_vals.partner_id.id)])
            not_fresh_lead=[x for x in lead_obj.browse(cr,uid,partner_ids_with_stages) if x.stage_id.id !=1 ] 
            if not_fresh_lead :

#            if len(partner_ids_with_stages) > 1 : 
                return False
        return True

       

    def action_apply(self, cr, uid, ids, context=None):
        """
        Convert lead to opportunity or merge lead and opportunity and open
        the freshly created opportunity view.
        """
        
#         
#	import ipdb;ipdb.set_trace()
        check_crm_status=self.check_crm_for_duplicate_opportunity(cr,uid,ids,context)
        if not check_crm_status : 
            raise osv.except_osv(_('Error!'), _('Partner has been already converted to opportunity'))

        if check_crm_status=='pending partner' : 
            raise osv.except_osv(_('Error!'), _('Odoo Id not generated!! Contact Accounts Team'))

        if context is None:
            context = {}

        lead_obj = self.pool['crm.lead']
        

        w = self.browse(cr, uid, ids, context=context)[0]
        opp_ids = [o.id for o in w.opportunity_ids]
        vals = {
            'section_id': w.section_id.id,
        }
        if w.partner_id:
            vals['partner_id'] = w.partner_id.id
        if w.name == 'merge':
            lead_id = lead_obj.merge_opportunity(cr, uid, opp_ids, context=context)
            lead_ids = [lead_id]
            lead = lead_obj.read(cr, uid, lead_id, ['type', 'user_id'], context=context)
            if lead['type'] == "lead":
                context = dict(context, active_ids=lead_ids)
                vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
                self._convert_opportunity(cr, uid, ids, vals, context=context)
            elif not context.get('no_force_assignation') or not lead['user_id']:
                vals.update({'user_id': w.user_id.id})
                lead_obj.write(cr, uid, lead_id, vals, context=context)
        else:
            lead_ids = context.get('active_ids', [])
            vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
            self._convert_opportunity(cr, uid, ids, vals, context=context)

        return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, lead_ids[0], context=context)



class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def dnd_stage(self,cr,uid,ids,context): 
        '''push lead to Do not disturb stage '''
        crm_stage_obj=self.pool.get('crm.case.stage')
        
        if ids :
            dnd_stage_id= crm_stage_obj.search(cr,uid,[('is_dnd','=',True)] )
            if not dnd_stage_id : 
                raise osv.except_osv(_('Error '), _('Do Not Disturb Stage Not Found '))

            for crm in self.browse(cr,uid,ids) : 
                self.write(cr,uid,[crm.id],{'stage_id':dnd_stage_id[0],'hide_dnd_button':True})
                return True
        
        raise osv.except_osv(_('Error '), _('Technical Issue\nContact Odoo Team '))
        

    def _partner_email(self,cr, uid, ids, name, args, context):
        ''' store email based on BM login '''
        res={}
        
        for crm in self.browse(cr, uid, ids) :
            if context.get('tree_view_attrs') and context.get('login_id') : 
                
                
                ##BM can only see his own client mail address
                if crm.user_id.id==context.get('login_id') : 
                    email_address=crm.email_from
                    if email_address : 
                        res[crm.id]=email_address
                    else: 
                        res[crm.id]=''
                else : 
                    res[crm.id]=''                 
            
            else : 
                email_address=crm.email_from
                if email_address : 
                    res[crm.id]=email_address
    
                else :
                    res[crm.id]=''
        
        return res      



    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False): 
        user_obj=self.pool.get('res.users')
          
        res = super(crm_lead, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form': 
            if uid ==SUPERUSERID : 
                return res
            
            doc = etree.XML(res['arch'])
            
            for node in doc.xpath("//field[@name='mobile']"):
                user_id=str(uid)
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ]]}'
                node.set('modifiers',modifier)

            for node in doc.xpath("//field[@name='phone']"):
                user_id=str(uid)
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ]]}'
                node.set('modifiers',modifier)

            for node in doc.xpath("//field[@name='email_from']"):
                user_id=str(uid)
                modifier='{"invisible": [["user_id", "!=",' +user_id +' ]]}'
                node.set('modifiers',modifier)


            res['arch'] = etree.tostring(doc)
            return res            

        return res    
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        
        if context is None:
            context = {}
        
        emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
        if emp_id :
            if len(emp_id) >1 :
                raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
            
            return emp_id[0]
        
    def on_change_user(self, cr, uid, ids, user_id, context=None):
        ''' Inherited function to Get employee id if User manually change the Saleperson'''
        user_obj=self.pool.get('res.users')

        vals=super(crm_lead,self).on_change_user(cr, uid, ids, user_id, context)
        if user_id:
            user=user_obj.browse(cr,uid,user_id)
            emp_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',user_id)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                vals.update({'employee_id':emp_id[0],'salesperson_alias':user.name})
                return {'value':vals}
            else:
                raise osv.except_osv(_('Error'), _("Employee Record Not Found\nContact HR Department"))
        else:
            
            return vals        

    def check_partner_unique(self,cr,uid,vals): 
        '''Do not create crm if lead exist '''
         
        partner_obj=self.pool.get('res.partner')
        if vals.get('partner_id') and vals.get('state') : 
            cr.execute(''' select lead_status from res_partner where id=%s''',(vals.get('partner_id'),))
            lead_status=cr.execute(lambda x:x[0],cr.fetchall())            
            if lead_status : 
                return False
                                
            else : 
                ##############update lead status on partner#########
                partner_obj.write(cr,uid,[vals.get('partner_id')],{'lead_status':vals.get('state')})
                print '-----------Lead Updated On Partner-----------'
                
        return True

    def get_latest_note(self,cr,uid,crm):  
        '''store latest note '''
        if not crm.log_note_line : 
            cr.execute(''' update crm_lead set current_note='' where id=%s''',(crm.id,))
        else:
            lastest_datetime=max([datetime.datetime.strptime(dt.date, "%Y-%m-%d %H:%M:%S") for dt in crm.log_note_line ])
            note=[note.name for note in crm.log_note_line if note.date==lastest_datetime.strftime("%Y-%m-%d %H:%M:%S") ]
            if note and len(note)==1 : 
                cr.execute(''' update crm_lead set current_note=%s where id=%s''',(note[0],crm.id))
                print '-----NOTE ADDED-----'
            else :
                raise osv.except_osv(_('Error!'), _(' Logging Note Failed\nContact Odoo Team'))
            
        return True

    def update_partner_crm_status(self,cr,uid,ids,context): 
        '''update crm status for partner '''

        crm=self.browse(cr,uid,ids[0])
        if crm.partner_id : 
            crm_ids_for_partner=self.search(cr,uid,[('partner_id','=',crm.partner_id.id),('stage_id','in',[6,10])])
            if len(crm_ids_for_partner) > 1: 
                lead_status='Duplicate Lead'
            else : 
                
                if crm.stage_id : 
                    lead_status=crm.stage_id.name
                else:
                    lead_status='Fresh Lead'
                        
            cr.execute('''update res_partner set crm_lead_state=%s where id=%s ''',(lead_status,crm.partner_id.id))
            print '------PARTNER   LEAD  STATUS  UPDATED-----------------'
        
        else : 
            print '------NO  PARTNER  FOUND !!!-----------------'            

        return True       
        

    def create(self, cr, uid, vals, context=None):
        ''' Overide create method to do validation'''
        
        
        #############write lead status########
#         if not self.check_partner_unique(cr,uid,vals) : 
#             raise osv.except_osv(_('Error!'), _('Email Address Already Exist !!'))
#         
        if vals.get('partner_id')==False or vals.has_key('partner_id')==False : 
            raise osv.except_osv(_('Error!'), _('Select Partner/Client'))
#         

        crm_id=super(crm_lead, self).create(cr, uid, vals, context)
        self.get_latest_note(cr,uid,self.browse(cr,uid,crm_id))
        return crm_id  	
            
    def write(self, cr, uid, ids, vals, context=None):     
        ''' Overide create method to do validation'''

        #############write lead status########
        crm=self.browse(cr,uid,ids[0])
        self.update_partner_crm_status(cr,uid,ids,context)
	crm_id= super(crm_lead, self).write(cr, uid, ids,vals, context)        
	self.get_latest_note(cr,uid,crm)
	return crm_id

    def unlink(self, cr, uid, ids, context=None):
        ''' Restrict user to delete leads other than fresh lead'''
        try :
             
            for crm in self.browse(cr,uid,ids[0]) : 
                
                assert crm.user_id.id ,'Salesperson Not Assigned To Lead'
                assert crm.user_id.id ==uid or uid==SUPERUSERID,'You Cannot Delete Lead of {}\nDeleting Lead of Other Salesperson Restricted'.format(crm.user_id.name)
                assert crm.stage_id.id in [1,False],'You Can Only Delete Fresh Lead'
                return super(crm_lead,self).unlink(cr,uid,[crm.id],context)
        except Exception as E  :
            raise osv.except_osv(_('Error'), _('{} ').format(E.message))


    _columns={
              
              #'employee_id':fields.function(default_emp_id,string='Employee User',type='many2one',relation='hr.employee',store=True),
              'employee_id':fields.many2one('hr.employee','Employee User'),
              'client_ip':fields.char('Client IP'),
              'qms_crm':fields.boolean('Via Website'),
              'odoo_script_lead':fields.boolean('Odoo Script(Lead) ?'),
              'odoo_script_converted':fields.boolean('Odoo Script(Converted) ?'),
              'odoo_script_new_partner_lead':fields.boolean('Odoo Script(NEW PARTNER-LEAD) ?'),
              'odoo_script_new_partner_opportunity':fields.boolean('Odoo Script(NEW PARTNER-OPPORTUNITY) ?'),
     #         'partner_email':fields.function(_partner_email,string='Email Address', type='char',store=True),
              'odoo_script_new_crm_opportunity_existing_partner':fields.boolean('Existing Partner Missing CRM(Opportunity/Converted Client) ?'),              
              'odoo_script_new_crm_fresh_existing_partner':fields.boolean('Existing Partner Missing CRM(Fresh Lead) ?'),
              'log_note_line': fields.one2many('crm.lead.log.notes', 'crm_id', 'Add Internal Notes'),              
              'current_note':fields.char('Note'),
              'salesperson_alias':fields.char('Salesperson Alias'),

              }

    _defaults={
               'salesperson_alias':lambda s, cr, uid, c: s.pool.get('res.users').browse(cr, uid,uid).name,		               
               'employee_id':default_emp_id,
               'qms_crm':False,
               'odoo_script_lead':False,
               'odoo_script_converted':False,
               'odoo_script_new_partner_lead':False,
               'odoo_script_new_partner_opportunity':False,
               'odoo_script_new_crm_opportunity_existing_partner':False,
               'odoo_script_new_crm_fresh_existing_partner':False,

               }





class crm_lead_log_notes(osv.osv): 
    
    _name='crm.lead.log.notes'
    _description='Add Notes On CRM'

    _columns={
              'crm_id': fields.many2one('crm.lead', 'Log CRM Notes', ondelete='cascade'),
              'name':fields.char('Description'),
              'date':fields.datetime('Date', readonly=False)
                                          
              }       
    
    _defaults={
               'date':lambda self,cr,uid,context=None:(datetime.datetime.now() + datetime.timedelta(hours=0,minutes=0)).strftime('%Y-%m-%d %H:%M:%S')
               }    
