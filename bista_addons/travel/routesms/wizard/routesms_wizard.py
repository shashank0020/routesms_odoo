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
SUPERID=1

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
        
    }

    def submit(self,cr,uid,ids,context):
        #uid=1
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window') 
        user_obj=self.pool.get('res.users')
        partner_obj=self.pool.get('res.partner')
        partner_dashboard_obj=self.pool.get('routsms.partner.filter')
                
        if ids :
            search_val=self.browse(cr,uid,ids[0])
            
            if search_val.partner_name and search_val.domain and search_val.email :
                ###################CASE 1############
                
                cr.execute(''' select id,user_id from res_partner where name like %s and domain=%s and email=%s and is_company=True''',('%'+search_val.partner_name,search_val.domain,search_val.email))
                vals=cr.fetchall()
                if not vals : 

                    cr.execute(''' select partner_id from res_partner where name like %s and domain=%s and email=%s''',('%'+search_val.partner_name,search_val.domain,search_val.email))
                    vals_line=cr.fetchall()
                    if vals_line : 

                        cr.execute(''' select id,user_id from res_partner where id=%s''',(vals_line[0],))
                        vals=cr.fetchall()                        
                                            
                    
            
            elif search_val.partner_name and search_val.domain and search_val.email==False :
                ###################CASE 2############
                cr.execute(''' select id,user_id from res_partner where name like %s and domain=%s and is_company=True''',\
                           ('%'+search_val.partner_name +'%',search_val.domain))
                vals=cr.fetchall()  
                


            elif search_val.partner_name and search_val.domain==False and search_val.email :
                ###################CASE 1############
                cr.execute(''' select id,user_id from res_partner where name like %s and email=%s and is_company=True''',\
                           ('%'+search_val.partner_name+'%',search_val.email))
                vals=cr.fetchall()          

            elif search_val.partner_name==False and search_val.domain and search_val.email :
                ###################CASE 4############
                
                cr.execute(''' select id,user_id from res_partner where  state='confirm' and domain like %s and email like %s and is_company=True''',\
                           ('%'+search_val.domain+'%','%'+search_val.email+'%'))
                vals=cr.fetchall()   
                
                if not vals : 

                    cr.execute(''' select partner_id from res_partner_contact_line where domain like %s and email like %s''',('%'+search_val.domain+'%','%'+search_val.email+'%'))
                    vals_line=map(lambda x:x[0],cr.fetchall())
                    if vals_line : 

                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id=%s''',(vals_line[0],))
                        vals=cr.fetchall()                  
                
            elif search_val.partner_name and search_val.domain==False and search_val.email==False :
                ###################CASE 5############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and name like %s and is_company=True''',\
                           ('%'+search_val.partner_name+'%',))
                vals=cr.fetchall()                       


            elif search_val.partner_name==False and search_val.domain==False and search_val.email : 
                ###################CASE 6############
                cr.execute(''' select id,user_id from res_partner where state='confirm' and email like %s and is_company=True''',\
                           ('%'+search_val.email+'%',))
                vals=cr.fetchall()

                if not vals : 

                    cr.execute(''' select partner_id from res_partner_contact_line where email like %s''',('%'+search_val.email+'%',))
                    vals_line=map(lambda x:x[0],cr.fetchall())
                    if vals_line : 

                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id=%s''',(vals_line[0],))
                        vals=cr.fetchall()                 

            
            elif search_val.partner_name==False and search_val.domain and search_val.email==False :
                ###################CASE 7############ 
                cr.execute(''' select id,user_id from res_partner where state='confirm' and domain like %s and is_company=True ''',\
                           ('%'+ search_val.domain +'%',))
                vals=cr.fetchall()
                
                
                if not vals : 

                    cr.execute(''' select partner_id from res_partner_contact_line where domain like %s''',('%'+search_val.domain+'%',))
                    vals_line=map(lambda x:x[0],cr.fetchall())
                    if vals_line : 

                        cr.execute(''' select id,user_id from res_partner where state='confirm' and id=%s''',(vals_line[0],))
                        vals=cr.fetchall()                  
                
                
#             elif search_val.partner_name==False and search_val.domain==False and search_val.email : 
#                 cr.execute(''' select id,user_id from res_partner where email=%s ''',(search_val.email,))
#                 vals=cr.fetchall()
                
            
                
            else : 
                
                raise osv.except_osv(_('Sorry!'),_("Invalid Criteria"))
            

            cr.execute(''' delete  from routsms_partner_filter''')
                
            if vals :
                for values in vals :
                    partner_type=user_obj.browse(cr,SUPERID,values[1]).partner_type
                    
                    partner_display_name=partner_obj.browse(cr,SUPERID,values[0]).name
                    crm_lead_state=partner_obj.browse(cr,SUPERID,values[0]).crm_lead_state
                    current_partner_type=user_obj.browse(cr,uid,uid).partner_type
                    if not partner_type or not current_partner_type: 
                        raise osv.except_osv(_('Validation Error!'),_("Partner Type Not Set\nContact HR Department"))
                    
                    if partner_type==current_partner_type :
                            
                        cr.execute(''' insert into routsms_partner_filter(name,user_id,lead_status) VALUES(%s,%s,%s)''',(partner_display_name,values[1],crm_lead_state))

                result = mod_obj.get_object_reference(cr, uid, 'routesms', 'action_routesms_partner_filter')
                id = result and result[1] or False
                result = act_obj.read(cr, uid, [id], context=context)[0]
                return result
                        
                
            else :
    #            import ipdb;ipdb.set_trace()
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
