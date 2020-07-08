# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartners(models.Model):
    _inherit = 'res.partner'

    # How to OverRide Create Method Of a Model
    # https://www.youtube.com/
    # watch?v=AS08H3G9x1U&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=26
    @api.model
    def create(self, vals_list):
        res = super(ResPartners, self).create(vals_list)
        print("yes working")
        # do the custom coding here
        return res

class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string=" Patient Name")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    #chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'Patient record'
    _rec_name = 'patient_name'

    @api.model
    def test_cron_job(self):
        for rec in self:
            print("Abcd")

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq, rec.patient_name)))
        return res


    @api.constrains('patient_age')
    def _check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The age must be greater than 5'))

    # compute function in Odoo
    # https://www.youtube.com/
    # watch?v=Mg80GxrKDOc&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=11
    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    # Making compute field editable using inverse function
    # https://www.youtube.com/
    # watch?v=NEr6hUTrn84&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=47
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    def open_patient_appoint(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': "{'create': False}"
        }
    def get_appoint_count(self):
        count = self.env['hospital.appointment'].search_count([
            ('patient_id', '=', self.id)])
        self.appoint_count = count

    # Print PDF Report From Button Click in Form
    # https://www.youtube.com/
    # watch?v=Dc8GDj7ygsI&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=67
    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(
            self)

    # How to Write Onchange Functions
    # https://www.youtube.com/watch?v=qyRhjyp1MeE&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=39
    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    # Sending Email in Button Click
    # https://www.youtube.com/
    # watch?v=CZVRmtv6re0&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=44
    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    patient_name = fields.Char(string="Name", required=True,
                       help="Name of the patient")
    patient_age = description = fields.Integer(string="Age",
                                               track_visibility="always")
    notes = fields.Text(string="Registration note")
    image = fields.Binary(string="Image")
    name = fields.Char(string="Test")
    appoint_count = fields.Integer(string='Appointment',
                                       compute='get_appoint_count')
    active = fields.Boolean("Active", default=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    email_id = fields.Char(string="Email")
    name = fields.Char(string="Contact Number")
    user_id = fields.Many2one('res.users', string="PRO")
    name_seq = fields.Char(string='Order Reference',
                           required=True,
                           copy=False,
                           readonly=True,
                           index=True,
                           default='New')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Doctor Gender")
    patient_name_upper = fields.Char(compute='_compute_upper_name',
                                     inverse='_inverse_upper_name')
    gender = fields.Selection([('male', 'Male'),('fe_male','Female'),],
                              default='male', string='Gender')

    age_group = fields.Selection([('major', 'Major'), ('minor','Minor'),
    ], string="Age Group", compute='set_age_group', store=True)

    @api.model
    def create(self, vals):
       if vals.get('name_seq', 'New') == 'New':
           vals['name_seq'] = self.env['ir.sequence'].next_by_code(
               'hospital.patient.sequence') or 'New'
       result = super(HospitalPatient, self).create(vals)
       return result