from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttendanceStatusMixin(models.AbstractModel):
    _name = 'attendance.status.mixin'
    _description = 'Attendance Status Mixin'

    name = fields.Char(
        string='Description')

    code = fields.Integer(
        string='Status Code',
        required=True,
        help="The status code of the attendance status. Examples:\n"
            "0: Normal Check-in\n"
            "1: Normal Check-out\n"
            "255: Unknown")

    type = fields.Selection(
        [
            ('checkin', 'Check-in'),
            ('checkout', 'Check-out'),
            ('unknown', 'Unknown'),
        ],
        string='Status Type',
        default='checkin',
        required=True)

    @api.constrains('code')
    def _constrains_code(self):
        for r in self:
            if r.code < 0 or r.code > 255:
                raise ValidationError("The status code must be between 0 and 255!")

class AttendanceStatusTemplate(models.Model):
    _name = 'attendance.status.template'
    _inherit = 'attendance.status.mixin'
    _description = 'Attendance Status Template'

    _sql_constraints = [
        ('unique_code',
        'UNIQUE(code)',
        "The status code must be unique!"),
    ]

class AttendanceStatus(models.Model):
    _name = 'attendance.status'
    _inherit = 'attendance.status.mixin'
    _description = 'Attendance Status'
    _rec_name = 'type'

    device_id = fields.Many2one(
        'attendance.device',
        string='Device',
        required=True,
        ondelete='cascade',
        help="The device that this attendance status is applied to")

    _sql_constraints = [
        ('unique_code_device',
        'UNIQUE(code, device_id)',
        "The status code must be unique per device!"),
    ]
