from odoo import models,fields,api,_

from odoo.exceptions import  UserError


class EducationInformation(models.Model):
    _name = 'education.information'

    institute = fields.Char("Institute",required=True)
    degree = fields.Many2one("hr.recruitment.degree")
    passing_year = fields.Integer("Passing Year")


    @api.constrains('passing_year')
    def _les_than_this_year(self):
        for record in self:
            if record.passing_year > fields.Date.today().year or record.passing_year < 1980:
                raise UserError(_("Passing Is cannot be less than 1980 or greater that this year"))