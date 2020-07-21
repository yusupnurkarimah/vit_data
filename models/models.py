# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta, date
from odoo.exceptions import Warning
from dateutil.relativedelta import relativedelta

class data(models.Model):
	_name = 'vit.data'

	name 	= fields.Char(string="Nama Komponen")
	waktu 	= fields.Integer(string="Waktu Pengerjaan")

class item(models.Model):
	_name = 'vit.item'

	name 			= fields.Char(string="Nama Item")
	data_line_ids 	= fields.One2many('vit.data_line', 'data_line_id', string='Components')
	total_bobot		= fields.Float(string="Bobot Presentase", compute="_calc_bobot", store=True,)

	@api.depends('data_line_ids')
	def _calc_bobot(self):
		am_total = 0.0
		for amou in self:
			for am in amou.data_line_ids:
				am_total += am.bobot
			amou.total_bobot = am_total
			if amou.total_bobot > 100:
				raise Warning('Total Bobot tidak boleh lebih dari 100 %')

class data_line(models.Model):
	_name = 'vit.data_line'

	comp_id 	= fields.Many2one('vit.data', string='Components')
	waktu_kerja	= fields.Integer(string="Waktu Pengerjaan")
	bobot 		= fields.Float(string="Bobot Presentase")
	data_line_id 	= fields.Many2one('vit.item', string='Components')
	tanggal_start 	= fields.Date(string="Tanggal Pengerjaan", default=fields.Date.today) #required=False, default=lambda self:time.strftime("%Y-%m-%d")
	tanggal_end 	= fields.Date(string="Ekspektasi Tanggal Selesai")
	tanggal_real 	= fields.Date(string="Real Tanggal Selesai")

	@api.onchange('comp_id')
	def _onchange_comp_id(self):
		self.waktu_kerja = self.comp_id.waktu
		self.tanggal_end = self.tanggal_start + relativedelta(days=+int(self.waktu_kerja))
	
