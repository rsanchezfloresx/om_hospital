# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    # Moving the State Of the Record To Confirm State in Button Click
    # How to Add States/Statusbar for Records in Odoo
    # https://www.youtube.com/
    # watch?v=lPHWsw3Iclk&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=21
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thanks You',
                    'type': 'rainbow_man',
                }
            }

    def delete_lines(self):
        for rec in self:
            print("rec", rec)
            rec.appointment_lines = [(5, 0, 0)]

    def action_done(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def create(self, vals):
       if vals.get('name', 'New') == 'New':
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'hospital.patient.sequence') or 'New'
       result = super(HospitalAppointment, self).create(vals)
       return result

    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        return res

    def _get_default_note(self):
        return "Subscribe our youtube channel"

    # Give Domain For A field dynamically in Onchange
    # How To Give Domain For A Field Based On Another Field
    # https://www.youtube.com/
    # watch?v=IpXXYCsK2ow&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=65
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=',
                                             rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        #res[patient_id] = 1
        #res[notes] = 'Like and Subscribe our channel To Get Notified'
        #return res
        appointment_lines = []
        product_rec = self.env['product.product'].search([])
        for pro in product_rec:
            line = (0, 0, {
                'product_id': pro.id,
                'product_qty': 1,
            })
            appointment_lines.append(line)
        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'Like and Subscribe our channel To Get Notified'
        })
        return res

    name = fields.Char(string='Appointment ID', required=True, copy=False,
                       readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient',
                                 required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note", default=_get_default_note)
    appointment_date = fields.Date(string='Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    doctor_note = fields.Text(string="Dr. Note")
    appointment_lines = fields.One2many('hospital.appointment.lines',
                                        'appointment_id',
                                        string='Appointment Lines')
    pharmacy_note = fields.Text(string="Pharm.Note")
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    product_id = fields.Many2one('product.template', string="Product Template")
    amount = fields.Float(string="Total Amount")

    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, default='draft')

    class HospitalAppointmentLines(models.Model):
        _name = 'hospital.appointment.lines'
        _description = 'Appointment Lines'

        product_id = fields.Many2one('product.product', string='Medicine')
        product_qty = fields.Integer(string="Quantity")
        #sequence = fields.Integer(string="Sequence")
        appointment_id = fields.Many2one('hospital.appointment',
                                         string='Appointment ID')

