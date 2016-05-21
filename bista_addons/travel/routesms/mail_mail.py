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

from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.tools.translate import _


class mail_mail(osv.Model):
    """ Update of mail_mail class, to add the signin URL to notifications. """
    _inherit = 'mail.mail'

    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
        """ Generate URLs for links in mails:
            - partner is not an user: signup_url
            - partner is an user: fallback on classic URL
        """
        if context is None:
            context = {}
        partner_obj = self.pool.get('res.partner')
        if partner and not partner.user_ids:
            contex_signup = dict(context, signup_valid=True)
            signup_url = partner_obj._get_signup_url_for_action(cr, SUPERUSER_ID, [partner.id],
                                                                action='mail.action_mail_redirect',
                                                                model=mail.model, res_id=mail.res_id,
                                                                context=contex_signup)[partner.id]
                      
            model_name, record_name ='',''                                                    
            return ", <span class='oe_mail_footer_access'><small>%(access_msg)s <a style='color:inherit' href='%(portal_link)s'>%(portal_msg)s</a></small></span>" % {
                'access_msg': _(''),
                'portal_link': '',
                'portal_msg': '%s %s' % (model_name, record_name) if mail.record_name else _('your messages '),
            }
        else:
            return super(mail_mail, self)._get_partner_access_link(cr, uid, mail, partner=partner, context=context)
        


class mail_notification(osv.Model):
    ''' Stop auto notification mail for invocing'''
    _inherit = 'mail.notification'
    
    def _notify(self, cr, uid, message_id, partners_to_notify=None, context=None,
                force_send=False, user_signature=True):
        """ Send by email the notification depending on the user preferences

            :param list partners_to_notify: optional list of partner ids restricting
                the notifications to process
            :param bool force_send: if True, the generated mail.mail is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
            :param bool user_signature: if True, the generated mail.mail body is
                the body of the related mail.message with the author's signature
        """
        
        notif_ids = self.search(cr, SUPERUSER_ID, [('message_id', '=', message_id), ('partner_id', 'in', partners_to_notify)], context=context)

        # update or create notifications
        new_notif_ids = self.update_message_notification(cr, SUPERUSER_ID, notif_ids, message_id, partners_to_notify, context=context)

        # mail_notify_noemail (do not send email) or no partner_ids: do not send, return
        if context and context.get('mail_notify_noemail'):
            return True
       
        if context.get('type') in ['out_invoice','in_invoice','out_refund','in_refund','receipt','payment'] :
             
            return True

        # browse as SUPERUSER_ID because of access to res_partner not necessarily allowed
        self._notify_email(cr, SUPERUSER_ID, new_notif_ids, message_id, force_send, user_signature, context=context)
            
                
        
