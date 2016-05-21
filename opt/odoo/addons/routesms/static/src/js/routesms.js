openerp.routesms = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    
    local.PartnerAuction = instance.Widget.extend({
        //template: "HomePage",
        start: function () {
            return $.when(
                new local.InstructionPage(this).appendTo(this.$el)
            );
        }
    });
    

    local.InstructionPage = instance.Widget.extend({
        template: "InstructionPage",
        init: function() {

        },
    });

    instance.web.client_actions.add(
        'routesms.partnerauction', 'instance.routesms.PartnerAuction');
}    