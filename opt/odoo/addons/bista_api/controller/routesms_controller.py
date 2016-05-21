
#import web.http as http
##from http import request
#import openerp.pooler as pooler
#        {'params': {'a': 65765, 'b': 213},{'a': 65765, 'b': 213},{'a': 65765, 'b': 213}} calling data format  su openerp -c 'python openerp-server --db-filter=odoo_demo'

#headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import module_boot, login_redirect
import openerp.pooler as pooler
from openerp import SUPERUSER_ID


class routesmscontrollertest(http.Controller):
    @http.route('/api_url_test', type='json', auth="public")
    def api_url_test(self, **req):
        #{'params': {'partner_id': 'your_customer_id', 'invoice_date': 'yy-mm-dd','due_date':'yy-mm-dd','currency_id':'INR','company_id':'Company Name','user_id':'Saleperson','partner_bank_id':'Account Number','product_detail':[{'product_id':'product name','quantity':1,'price_unit':0.0}]}}
#        osv_pool = pooler.get_pool('odoo_demo')
       
        print "fields-------------",req
        
        inv_obj = request.registry.get('account.invoice').search(request.cr, SUPERUSER_ID, [])
        
        
        
        

#        params = dict(map(operator.itemgetter('name', 'value'), fields))
#        print "params--------------",params
##        print "users+++++++++++++++",cert_type
#        user = osv_pool.get('res.users')
#        print "users------------",user
##        return "<h1>This is a test</h1>"
        return {'odoo_response':'API Successfull!!!'}
