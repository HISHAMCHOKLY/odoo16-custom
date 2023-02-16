from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "pos.refund"
    _description = "Patient Records"

    reason=fields.Text(string="Reason")
