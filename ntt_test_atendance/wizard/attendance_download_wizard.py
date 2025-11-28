from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AttendanceDownloadWizard(models.TransientModel):
    _name = 'attendance.download.wizard'
    _description = 'Attendance Download Wizard'

    device_id = fields.Many2one(
        'attendance.device',
        string='Attendance Device',
        help="The attendance device to download the attendance data.")

    date_from = fields.Datetime(
        string='Date From',
        required=True,
        help="The start date of the attendance data.")
        
    date_to = fields.Datetime(
        string='Date To',
        default=fields.Datetime.now(),
        required=True,
        help="The end date of the attendance data.")
    
    @api.onchange('date_from', 'date_to')
    def _onchange_date_from_date_to(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            return {
                'warning': {
                    'title': _('Invalid Date Range'),
                    'message': _('The date from must be before the date to.')
                }
            }

    def action_download_attendance(self):
        self.ensure_one()
        if self.date_from > self.date_to:
            raise UserError(_('The date from must be before the date to.'))

        self.device_id.date_from = self.date_from
        self.device_id.date_to = self.date_to
        start_time_local = self.device_id._convert_datetime_utc_to_local(self.date_from, self.device_id.timezone)
        end_time_local = self.device_id._convert_datetime_utc_to_local(self.date_to, self.device_id.timezone)

        # Date format: YYYY-MM-DD HH:MM:SS
        start_time = start_time_local.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_time_local.strftime("%Y-%m-%d %H:%M:%S")
        data = "StartTime={}\t".format(start_time)
        data += "EndTime={}\t".format(end_time)
        self.device_id._create_cmd_to_device(command="DATA QUERY ATTLOG", data=data)
