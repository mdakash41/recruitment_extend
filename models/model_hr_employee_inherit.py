from odoo import models,api,fields,_
from odoo.exceptions import UserError



class HREmployeeLeaveLine(models.Model):
    _name = 'hr.employee.leave.line'

    _rec_name = 'leave_type_id'

    leave_type_id = fields.Many2one('hr.leave.type',"Leave Type",required=True)
    leave_day = fields.Integer('Leave Day', default=0,required=True)
    this_year = fields.Integer('Year',compute='_compute_this_year',readonly=True,default=fields.Date.today().year)


    def _compute_this_year(self):
        for record in self:
            record.this_year = fields.Date.today().year



    @api.constrains('leave_day')
    def _check_leave_day(self):
        for record in self:
            if record.leave_day<0:
                raise UserError(_("Leave Days cannot be negative "))




class HREmployee(models.Model):
    _inherit = 'hr.employee'

    mulitple_emergency_contact = fields.Many2many('emergency.contact')
    mulitple_education_information = fields.Many2many('education.information')

    leave_line_ids = fields.Many2many('hr.employee.leave.line',string="Employee Leave", required=True)


    has_leave_record = fields.Char("Employee Leave Details",compute='_has_any_leave_record',required=True)

    @api.onchange('leave_line_ids')
    def _has_any_leave_record(self):
        for record in self:
            if not any(record.leave_line_ids):
                record.has_leave_record = False
            else:
                record.has_leave_record = "1"



