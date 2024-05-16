from odoo import http   
from datetime import datetime
class EstateControllers(http.Controller):
    @http.route(['/estate/properties','/estate/properties/page/<int:page>'],auth='public',website=True)
    def index(self,page=1,**kw):
        properties=http.request.env['estate.property'].search([
            ('state','!=','sold'),
            ('state','!=','canceled'),
            ('state','!=','achived'),
        ])
        total=len(properties)
        pager=http.request.website.pager(
            url='estate/properties',
            total=total,
            page=page,
            step=3,
        )
        offset=(page-1)*3
        properties_on_page=properties[offset:offset+3]
        values={
            'properties':properties_on_page,
            'pager':'pager',
        }
        return http.request.render('estate.index',values)

    @http.route('/estate/filter_properties',auth='public',website=True,csrf=False)
    def filter_properties(self,**kw):
        date=kw.get('datepicker') or datetime.now().date()
        properties=http.request.env['estate.property'].search([
            ('create_date','>=',date)
        ])
        return http.request.render('estate.filter_property',{
            'properties':properties,
        })

    @http.route('/estate/properties/<int:property_id>',auth='public',website=True)
    def property_details(self,property_id,**kw):
        property=http.request.env['estate.property'].browse(property_id)
        return http.request.render('estate.property_detail_template',{
            'property':property,
        })