<html>
    <head>
        <style type="text/css">
            ${css}
        </style>
    </head>
    <body>
        %for o in objects :
        <table width = '100%' class='td_company_title'>
            <tr>
                <td style="vertical-align: top;max-height: 45px;">
                    ${helper.embed_image('jpeg',str(o.company_id.logo),180, 85)}
                </td>
                <td>
                    <div>${o.company_id.name or ''|entity}</div>
                    <br>${o.company_id.partner_id.street or ''|entity} No. 
                                                ${o.company_id.partner_id.street2 or ''|entity}
                                                ${o.company_id.partner_id.zip or ''|entity}
                                                <br/>${o.company_id.partner_id.city or ''|entity}
                                                , ${o.company_id.partner_id.state_id.name or ''|entity}
                                                , ${o.company_id.partner_id.country_id.name or ''|entity}
                </td>
                <td>
                    <div><b>${_("Printing Date:")}</b> ${time.strftime('%Y-%m-%d %H:%M:%S')}</div>
                </td>
            </tr>
        </table>                                   

        <table class='celdaDetailTitulo'>
            <tr>
                <div>
                    <td><b>${_("Journal Entries: ")} </b>${o.name or '' |entity}</td>
                </div>
            </tr>
            <tr>
                <div>
                    <td><b>${_("Reference: ")}</b> ${o.ref or '' |entity}</td>
                </div>
            </tr>
            <tr width= '100%'>
                <div>
                    <td width= '50%'>
                        <b>${_("Period: ")}</b> ${o.period_id.name or '' |entity}
                    </td>
                    <td width= '50%'>
                        <b>${_("Date: ")}</b> ${o.date or '' |entity}
                    </td>  
                </div>
            </tr>
            <tr>
                <div>
                    <tr>
                        <td>
                            <b>${_("To Review: ")}</b> 
                        </td>
                        <td>
                            %if o.to_check:
                                <p>&#10004;</p>
                            %endif
                        </td>
                    </tr>
                </div>
            </tr>
        </table>
        
        <table width= '100%' style="border-collapse: collapse;">
            <tr class='celdaTituloTabla'>
                <td width='5%'>
                    <div>${_("Invoice")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Name")}</div>
                </td>
                <td width='7%'>
                    <div>${_("Partner")}</div>
                </td>
                <td width='8%'>
                    <div>${_("Account")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Due date")}</div>
                </td>
                <td width='5%'>
                    <div>${_("Debit")}</div>
                </td>
                <td width='5%'>
                    <div>${_("Credit")}</div>
                </td>
               <!--<td width='6%'>
                    <div>${_("Analytic Account")}</div>
                </td>-->
                <td width='6%'>
                    <div>${_("Amount Currency")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Currency")}</div>
                </td>
                <!--<td width='6%'>
                    <div>${_("Tax Account")}</div>
                </td>-->
                <td width='6%'>
                    <div>${_("Tax Amount")}</div>
                </td>
                <!--<td width='6%'>
                    <div>${_("Tax Secondary")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Status")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Reconcile")}</div>
                </td>
                <td width='6%'>
                    <div>${_("Partial Reconcile")}</div>
                </td>-->

                
            </tr>
            %for line in o.line_id:
            <tr class='celdaDetail' style="font-size:medium">
                <td width='5%'>
                    <div>${line.invoice.number or '' |entity}</div>
                </td>
                <td width='6%' style="word-wrap: break-word">
                    <div>${line.name or '' |entity}</div>
                </td>
                <td width='7%'>
                    <div>${line.partner_id.name or ''}</div>
                </td>
                <td width='8%'>
                    <div>${line.account_id.code or '' |entity} - ${line.account_id.name or '' |entity}</div>
                </td>
                <td width='6%'>
                    <div>${line.date_maturity or '' |entity}</div>
                </td>
                <td width='5%' style="text-align:right;">
                    <div>${formatLang(line.debit or 0.0) |entity}</div>
                </td>
                <td width='5%' style="text-align:right;">
                    <div>${formatLang(line.credit or 0.0) |entity}</div>
                </td>
                <!--<td width='6%'>
                    <div>${line.analytic_account_id.name or '' |entity}</div>
                </td>-->
                <td width='6%' style="text-align:right;">
                    <div>${formatLang(line.amount_currency or 0.0) |entity}</div>
                </td>
                <td width='6%'>
                    <div>${line.currency_id.name or '' |entity}</div>
                </td>
                <!--<td width='6%'>
                    <div>${line.tax_code_id.name or '' |entity}</div>
                </td>-->
                <td width='6%' style="text-align:right;">
                    <div>${formatLang(line.tax_amount or 0.0) |entity}</div>
                </td>

                <!--<td width='6%' style="text-align:center;">
                    %if line.state == "valid":
                        ${_("Balanced")}
                    %elif line.state == "draft":
                        ${_("Unbalanced")}
                    %endif
                </td>
                <td width='6%'>
                    <div>${line.reconcile_id.name or '' |entity}</div>
                </td>
                <td width='6%'>
                    <div>${line.reconcile_partial_id.name or '' |entity}</div>
                </td>-->
            </tr>
            %endfor
            <tr class='celdaTotal'>
                <td colspan="5"></td>
                <td>
                    <div width='6%' >${formatLang(get_total_debit_credit(o.line_id)['sum_tot_debit'] or 0.0) |entity}</div>
                </td>
                <td>
                    <div width='6%'>${formatLang(get_total_debit_credit(o.line_id)['sum_tot_credit'] or 0.0) |entity}</div>
                </td>
                <td colspan="9"></td>
            </tr>
            
        </table>
        <p>
        	%if o.narration:
        	<b>${_("Internal Note: ")}</b> ${o.narration or '' }
        	%endif
        </p>
        
        <table style="border:1px solid black" align="center">
        
        
			  <tr>
			    <td style="border:1px solid black;font-size: smaller">Date</td>
			    <td style="border:1px solid black;font-size: smaller">${o.date or '' }</td>
			  </tr>
			  <tr>
			    <td style="border:1px solid black;font-size: smaller">Ch.No./Cash</td>
			    <td style="border:1px solid black;font-size: smaller">${o.ref or '' }</td>
			  </tr>
			  <tr>
			    <td style="border:1px solid black;font-size: smaller">Odoo Vo.No</td>
			    <td style="border:1px solid black;font-size: smaller">${o.name or '' }</td>
			  </tr>        

			  <tr>
			    <td style="border:1px solid black;font-size: smaller">Name</td>
			    <td style="border:1px solid black;font-size: smaller">${get_responsible_person(o)}</td>	
			  </tr> 
		</table>		

			  
        
        %if len(loop._iterable) != 1 and loop.index != len(loop._iterable)-1:
            <p style="page-break-after:always"></p>
        %endif
    %endfor
    </body>
</html>
