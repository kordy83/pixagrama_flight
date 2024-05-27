# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if not self.env.user.has_group('pixagrama_flight.group_edit_invoice'):
            raise UserError(_("Sorry, you don't have privileges to edit invoice."))
        return res


class Insurance(models.Model):
    _name = "insurance.order"

    name = fields.Char("الاسم")
    address = fields.Char("العنوان")
    mobile1 = fields.Char("رقم الموبايل 1")
    mobile2 = fields.Char("رقم الموبايل 2")
    country = fields.Char("الدوله")
    q_number = fields.Char("رقم القسيمه")
    q_code = fields.Char("كود القسيمه")
    traveling_date = fields.Date("تاريخ السفر")
    arrival_date = fields.Date("تاريخ العوده")
    number_of_days = fields.Integer("عدد الايام")
    responsible_employee = fields.Char("الموظف المسئول")


class ProjectTask(models.Model):
    _inherit = "project.task"

    child_group_id = fields.Many2one('child.travel.group', string='child Group',)


class ChildTravel(models.Model):
    _name = "child.travel.group"

    name = fields.Char("الاسم")
    coordinator = fields.Char("المنسق")
    address = fields.Char("العنوان")
    mobile1 = fields.Char("رقم الموبايل 1")
    mobile2 = fields.Char("رقم الموبايل 2")
    region = fields.Char("الجهه")
    program_price = fields.Float("سعر البرنامج")
    sale_price = fields.Float("سعر البيع")
    profit = fields.Float("الربح")
    child_ids = fields.Many2many('res.partner', 'child_travel_group_id', string='عملاء')
    active = fields.Boolean(default=True)
    image = fields.Binary()
    # partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_id', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.child_ids:
                if line.total_invoiced > 0:
                    line.child_travel_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'الاطفال',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('child_travel_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('child_group_id', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.child_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('child_group_id', '=', partner.id)])


class ResPartnerFlight(models.Model):
    _name = "res.partner.flight"

    name = fields.Char("الاسم")
    address = fields.Char("العنوان")
    mobile1 = fields.Char("رقم الموبايل 1")
    mobile_fly = fields.Char("رقم الموبايل 2")
    reservation_date_fly = fields.Date("تاريخ الحجز")
    travel_date_fly = fields.Date("تاريخ السفر")
    transient_time_fly = fields.Datetime("مده الترانزيت")
    leaving_time_fly = fields.Datetime("تاريخ المغادره")
    transient_period_fly = fields.Datetime("مده الترانزيت عوده")
    reference_number_fly = fields.Char("رقم الرجع")
    ticket_number_fly = fields.Char("رقم التزكره")
    visa_name_fly = fields.Char("الاسم الاخير فى الجواز")
    ticket_price_fly = fields.Float("سعر التذكره")
    sale_price_fly = fields.Float("سعر البيع")
    profit_fly = fields.Float("صافي الربح")
    walking_line_fly = fields.Char("خط السير")
    country_id_fly = fields.Many2one(comodel_name="res.country", string="دوله الترانزيت")
    transient_visa_fly = fields.Char("فيزا ترانزيت")
    state_fly = fields.Selection(string="نوع العميل", selection=[('vip', 'Vip'), ('local', 'local'), ])
    commission_line_fly = fields.Float("عموله الخطوط")
    weight_fly = fields.Float("وزن الامتعه")
    degree_fly = fields.Char("الدرجه")
    flight_type_fly = fields.Char("نوع الطيران")
    time_difference_fly = fields.Datetime("فرق التوقيت")


class ResPartner(models.Model):
    _inherit = "res.partner"

    child_travel_group_id = fields.Many2one('child.travel.group')
    is_child = fields.Boolean()
    is_insurance = fields.Boolean()
    is_flight = fields.Boolean()
    coordinator = fields.Char("المنسق")
    mobile2_child = fields.Char("رقم الموبايل 2")
    region = fields.Char("الجهه")
    program_price = fields.Float("سعر البرنامج")
    sale_price = fields.Float("سعر البيع")
    profit = fields.Float("الربح")
    #flight
    mobile_fly = fields.Char("رقم الموبايل 2")
    reservation_date_fly = fields.Date("تاريخ الحجز")
    travel_date_fly = fields.Date("تاريخ السفر")
    transient_time_fly = fields.Datetime("مده الترانزيت")
    leaving_time_fly = fields.Datetime("تاريخ المغادره")
    transient_period_fly = fields.Datetime("مده الترانزيت عوده")
    reference_number_fly = fields.Char("رقم الرجع")
    ticket_number_fly = fields.Char("رقم التزكره")
    visa_name_fly = fields.Char("الاسم الاخير فى الجواز")
    ticket_price_fly = fields.Float("سعر التذكره")
    sale_price_fly = fields.Float("سعر البيع")
    profit_fly = fields.Float("صافي الربح")
    walking_line_fly = fields.Char("خط السير")
    country_id_fly = fields.Many2one(comodel_name="res.country", string="دوله الترانزيت")
    transient_visa_fly = fields.Char("فيزا ترانزيت")
    state_fly = fields.Selection(string="نوع العميل", selection=[('vip', 'Vip'), ('local', 'local'), ])
    commission_line_fly = fields.Float("عموله الخطوط")

    weight_fly = fields.Char("وزن الذهاب")
    back_weight_fly = fields.Char("وزن العوده")
    going_degree = fields.Char("درجه الذهاب")
    back_degree = fields.Char("درجه العوده")
    time_difference_fly2 = fields.Char("فرق التوقيت")
    trip_time = fields.Char("مده الرحله")

    degree_fly = fields.Char("الدرجه")
    flight_type_fly = fields.Char("نوع الطيران")
    time_difference_fly = fields.Datetime("فرق التوقيت")

    #insurance
    mobile2_insurance = fields.Char("رقم الموبايل 2")
    country_insurance = fields.Char("الدوله")
    q_number_insurance = fields.Char("رقم القسيمه")
    q_code_insurance = fields.Char("كود القسيمه")
    traveling_date_insurance = fields.Date("تاريخ السفر")
    arrival_date_insurance = fields.Date("تاريخ العوده")
    number_of_days_insurance = fields.Integer("عدد الايام")
    responsible_employee_insurance = fields.Char("الموظف المسئول")
    show_in_flights = fields.Boolean('إنشاء بتذاكر الطيران')
    related_flight = fields.Many2one(comodel_name="res.partner", string='تذاكر الطيران', compute='_compute_related_flight')

    @api.depends('show_in_flights')
    def _compute_related_flight(self):
        for rec in self:
            if rec.show_in_flights:
                rec.related_flight = self.env['res.partner'].search([('is_flight', '=', True),('name', '=', rec.name)],limit=1)
            else:
                rec.related_flight = False

    @api.onchange('show_in_flights')
    def onchange_show_in_flights(self):
        for rec in self:
            if rec.show_in_flights == True:
               self.env['res.partner'].create({  
                                                'name': rec.name,
                                                'is_flight': True,
                                                'is_external': False,
                                                'notify_email': rec.notify_email,
                                                'invoice_warn': rec.invoice_warn,
                                                'sale_warn': rec.sale_warn,
                                                'company_id': rec.company_id.id,
                                                })

