from odoo import models,fields,api,_
from odoo.exceptions import UserError


class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    mulitple_emergency_contact = fields.Many2many('emergency.contact')
    mulitple_education_information = fields.Many2many('education.information')

    manager_id = fields.Many2one('hr.employee',compute='_get_department_manager')

    @api.depends('department_id.manager_id')
    def _get_department_manager(self):
        for record in self:
            record.manager_id = record.department_id.manager_id

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        if not (any(self.mulitple_emergency_contact) and any(self.mulitple_education_information)):
            raise UserError(_("You should Enter At least one record of emergency contact and education information"))
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                applicant.partner_id = new_partner_id
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee_data = {
                    'default_name': applicant.partner_name or contact_name,
                    'default_job_id': applicant.job_id.id,
                    'default_job_title': applicant.job_id.name,
                    'default_address_home_id': address_id,
                    'default_department_id': applicant.department_id.id or False,
                    'default_address_id': applicant.company_id and applicant.company_id.partner_id
                                          and applicant.company_id.partner_id.id or False,
                    'default_work_email': applicant.department_id and applicant.department_id.company_id
                                          and applicant.department_id.company_id.email or False,
                    'default_work_phone': applicant.department_id.company_id.phone,
                    'form_view_initial_mode': 'edit',
                    'default_applicant_id': applicant.ids,
                    'default_mulitple_emergency_contact': [(0,0,{'name':record.name,'address':record.address,'phone':record.phone}) for record in self.mulitple_emergency_contact],
                    'default_mulitple_education_information':[(0,0,{'institute':record.institute,'degree':record.degree.id,'passing_year':record.passing_year}) for record in self.mulitple_education_information],
                    'default_parent_id': self.manager_id.id
                }

        dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
        dict_act_window['context'] = employee_data
        return dict_act_window
