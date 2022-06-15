from odoo import models, fields, api,_
from odoo.exceptions import UserError


class EmergencyContact(models.Model):
    _name = 'emergency.contact'

    name = fields.Char("Name", required=True)
    address = fields.Text("Address", required=True)
    phone = fields.Char("Phone", required=True)



    @api.model
    def create(self, vals_list):
        vals_list['name'] = vals_list['name'].title()
        result = super(EmergencyContact, self).create(vals_list)
        return result
