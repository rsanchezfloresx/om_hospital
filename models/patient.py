# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string=" Patient Name")

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    #chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'Patient record'
    _rec_name = 'patient_name'

    @api.constrains('patient_age')
    def _check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The age must be greater than 5'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    patient_name = fields.Char(string="Name", required=True,
                       help="Name of the patient")
    patient_age = description = fields.Integer(string="Age",
                                               track_visibility="always")
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image")
    name = fields.Char(string="Test")

    name_seq = fields.Char(string='Order Reference',
                           required=True,
                           copy=False,
                           readonly=True,
                           index=True,
                           default='New')

    gender = fields.Selection([('male', 'Male'),('fe_male','Female'),],
                              default='male', string='Gender')

    age_group = fields.Selection([('major', 'Major'), ('minor','Minor'),
    ], string="Age Group", compute='set_age_group')

    @api.model
    def create(self, vals):
       if vals.get('name_seq', 'New') == 'New':
           vals['name_seq'] = self.env['ir.sequence'].next_by_code(
               'hospital.patient.sequence') or 'New'
       result = super(HospitalPatient, self).create(vals)
       return result