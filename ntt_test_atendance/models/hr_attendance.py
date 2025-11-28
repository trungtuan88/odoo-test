from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    checkin_device_id = fields.Many2one(
        'attendance.device',
        string='Checkin Device',
        readonly=True,
        index=True,
        help="This is the device that the user used to checkin.")

    checkout_device_id = fields.Many2one(
        'attendance.device',
        string='Checkout Device',
        readonly=True,
        index=True,
        help="This is the device that the user used to checkout.")

    in_mode = fields.Selection(
        selection_add=[('device', 'Device Attendance')],
        ondelete={'manual': 'set default'})

    out_mode = fields.Selection(
        selection_add=[('device', 'Device Attendance')],
        ondelete={'manual': 'set default'})

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        sync_from_device = self.env.context.get('sync_from_device', False)
        if not sync_from_device:
            super(HrAttendance, self)._check_validity()
