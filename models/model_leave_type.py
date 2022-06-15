from odoo import models,fields


class HRLeaveType(models.Model):
    _name = 'hr.leave.type'

    _rec_name = 'leave_name'

    leave_name = fields.Char("Leave Name", required=True)
