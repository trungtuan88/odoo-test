from odoo import models, fields, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    user_bio_ids = fields.One2many(
        'user.bio.template',
        'employee_id',
        string='User Biometric Template',
        groups='hr.group_hr_user',
        readonly=True)

    user_bio_count = fields.Integer(
        compute='_compute_user_bio_count',
        groups='hr.group_hr_user,to_attendance_device.group_attendance_devices_manager')

    user_on_device_ids = fields.One2many(
        'user.on.device',
        'employee_id',
        string='Mapped Device Users',
        groups='hr.group_hr_user')
    
    device_ids = fields.Many2many(
        'attendance.device',
        string='Devices',
        compute='_compute_device_ids',
        help="List of devices that the employee is mapped to")

    def _compute_device_ids(self):
        for r in self:
            r.device_ids = [(6, 0, r.user_on_device_ids.device_id.ids)]

    def _compute_user_bio_count(self):
        data = self.env['user.bio.template']._read_group(
            [('employee_id', 'in', self.ids)], ['employee_id'], ['__count'])
        mapped_data = {employee.id: count for employee, count in data}
        for r in self:
            r.user_bio_count = mapped_data.get(r.id, 0)

    def upload_employee_to_device(self, device):
        self.ensure_one()
        if self.user_on_device_ids:
            user_on_device_copy = self.user_on_device_ids.filtered(lambda user: user.device_id.state == 'confirmed')[0]
            if not user_on_device_copy:
                user_on_device_copy = self.user_on_device_ids[0]
            user_on_device = user_on_device_copy.copy({
                'device_id': device.id,
            })
        else:
            if not self.barcode:
                self.generate_random_barcode()
            user_on_device = self.create_user_on_device_if_not_exist(device)
        user_on_device.upload_user_to_device()

    def create_user_on_device_if_not_exist(self, device):
        self.ensure_one()
        return self.env['user.on.device'].create({
                'employee_id': self.id,
                'device_id': device.id,
                'pin': self.barcode,
                'name': self.name,
            })

    def action_upload_employee(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Select Devices'),
            'res_model': 'select.device.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_ids': self.ids,
            }
        }