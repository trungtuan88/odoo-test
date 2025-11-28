from odoo import models, fields, _
from odoo.exceptions import ValidationError
from odoo import tools


class SelectDeviceWizard(models.TransientModel):
    _name = 'select.device.wizard'
    _description = 'Select Device Wizard'

    device_ids = fields.Many2many(
        'attendance.device',
        'select_device_wizard_attendance_device_rel',
        'wizard_id',
        'device_id',
        string='Devices')

    def action_select_device(self):
        employees = self._context.get('default_employee_ids', [])
        return {
            'type': 'ir.actions.act_window',
            'name': _('Upload Employees'),
            'res_model': 'upload.employee.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_ids': employees,
                'default_device_ids': self.device_ids.ids,
            }
        }

class UploadEmployeeLine(models.TransientModel):
    _name = 'upload.employee.wizard.line'
    _description = 'Upload Employee Wizard Line'

    wizard_id = fields.Many2one(
        'upload.employee.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade')

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        ondelete='cascade')

    device_ids = fields.Many2many(
        'attendance.device',
        'upload_employee_wizard_line_attendance_device_rel',
        'line_id',
        'device_id',
        string='Devices',
        required=True,
        ondelete='cascade')

    def upload_employee_to_device(self):
        self.ensure_one()
        for device in self.device_ids:
            self.employee_id.upload_employee_to_device(device)

class UploadEmployeeWizard(models.TransientModel):
    _name = 'upload.employee.wizard'
    _description = 'Upload Employee Wizard'

    device_ids = fields.Many2many(
        'attendance.device',
        'upload_employee_wizard_attendance_device_rel',
        'wizard_id',
        'device_id',
        string='Devices')
    
    employee_lines = fields.One2many(
        'upload.employee.wizard.line',
        'wizard_id',
        string='Employee Lines',
        default=lambda self: self._default_get_employee_lines())

    def _default_get_employee_lines(self):
        employees = self._context.get('default_employee_ids', [])
        devices = self._context.get('default_device_ids', [])
        if employees:
            return [(0, 0, {
                'employee_id': employee,
                'device_ids': devices,
            }) for employee in employees]
        return [(5, 0, 0)]

    def action_upload_employee(self):
        self.ensure_one()
        error_msg = ""
        employee_lines = self.employee_lines
        employees_without_barcode = self.env['hr.employee'].search([
            ('id', 'in', self.employee_lines.employee_id.ids),
            ('barcode', '=', False),
            ('user_on_device_ids', '=', False),
        ])

        if employees_without_barcode:
            for employee in employees_without_barcode:
                try:
                    with self.env.cr.savepoint(flush=False), tools.mute_logger('odoo.sql_db'):
                        employee.generate_random_barcode()
                except Exception as e:
                    employee_lines = employee_lines - employee_lines.filtered(lambda line: line.employee_id == employee.id)
                    error_msg.append(employee)

        for employee_line in self.employee_lines:
            employee_line.upload_employee_to_device()
    
        if error_msg:
            msg = _("Could not generate Badge ID for the following employees:")
            msg += "\n" + "\n".join([employee.display_name for employee in error_msg])
            raise ValidationError(msg)
