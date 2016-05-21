import time

from openerp import models, fields, api
import time
from openerp.osv import osv

class AccountFiscalPositionRule(models.Model):
#class AccountFiscalPositionRule(osv.osv):
    
    _inherit = 'account.fiscal.position.rule'
    
#     
#     invoice_line_tax_id = fields.Many2many('account.tax',
#         'account_invoice_line_tax', 'invoice_line_id', 'tax_id',string='Taxes')    

    rule_country_group_id=fields.Many2one('res.country.group', 'Country Group', help="Apply when the shipping or invoicing country is in this country group, and no position matches the country directly.")
    country_ids_line=fields.Char('Country')
    
    def myonchange(self,cr,uid,ids,country_group_id,context=None):
        
        vals={}
        country_li=''
        if country_group_id:
            
            cr.execute(''' select res_country_id from res_country_res_country_group_rel where res_country_group_id=%s''',(country_group_id,))
            
            res=[i[0] for i in cr.fetchall()]
            
            for jj in res:
                country_li+=str(jj)+','
            
            vals.update({'country_ids_line':country_li})
            
            
        return {'value':vals}
    
    def _map_domain(self, partner, addrs, company, **kwargs):
        
        self.env.cr.execute('select * from res_partner')
        res = self.env.cr.fetchall()
        result=super(AccountFiscalPositionRule,self)._map_domain( partner, addrs, company, **kwargs)
        
        
        print 'wpp'
        from_country = company.partner_id.country_id.id
        from_state = company.partner_id.state_id.id

        document_date = self.env.context.get(
            'date', time.strftime('%Y-%m-%d'))
        use_domain = self.env.context.get(
            'use_domain', ('use_sale', '=', True))

        domain = [
            '&', ('company_id', '=', company.id), use_domain,
            '|', ('from_country', '=', from_country),
            ('from_country', '=', False),
            '|', ('from_state', '=', from_state),
            ('from_state', '=', False),
            '|', ('date_start', '=', False),
            ('date_start', '<=', document_date),
            '|', ('date_end', '=', False),
            ('date_end', '>=', document_date),
        ]
        if partner.vat:
            domain += [('vat_rule', 'in', ['with', 'both'])]
        else:
            domain += [
                '|', ('vat_rule', 'in', ['both', 'without']),
                ('vat_rule', '=', False)]

        for address_type, address in addrs.items():
            #key_country = 'to_%s_country' % address_type
            key_country='country_ids_list'
            key_state = 'to_%s_state' % address_type
            to_country = address.country_id.id or False
            domain += [
                '|', (key_country, 'in', to_country),
                (key_country, '=', False)]
            to_state = address.state_id.id or False
            domain += [
                '|', (key_state, '=', to_state),
                (key_state, '=', False)]
        
        return domain    
    