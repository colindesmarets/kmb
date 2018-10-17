# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.http import request
from odoo import http

class klyController(http.Controller):
	@http.route(['/TSRGIST3000_'], type='http', auth='user', website=True)
	def TSRGIST3000_(self, **kw):
		return request.render("kly.pretest")

	@http.route(['/TSRGIST3000'],type='http', auth='user', website=True)
	def TSRGIST3000(self, **kw):
		return request.render("kly.home")

	@http.route(['/TSRGIST3000/new'],type='http', auth='user', website=True)
	def TSRGIST3000_new(self, **kw):
		inventory_id = request.env['inventory.inventory'].create({
			'name': "Inventory - Kelly",
			})
		story_id = request.env['story.story'].search([('name','=','Kly')], limit=1)
		session_id = request.env['story.session'].create({
			'partner_id': request.env.user.partner_id.id,
			'story_id': story_id.id,
			'date': datetime.today(),
			'inventory_id': inventory_id.id,
			'code': str(request.env.user.partner_id.id)+str(story_id.id)+str(inventory_id.id),
		})
		item_01 = request.env['inventory.item'].create({
			'inventory_id': inventory_id.id,
			'name': "Fancy pyjama with flamingos",
			'code': "pyjama",
		})
		item_02 = request.env['inventory.item'].create({
			'inventory_id': inventory_id.id,
			'name': "Canon EF-M 18-55mm f/3.5-5.6 IS STM",
			'code': "canon",
		})
		item_03 = request.env['inventory.item'].create({
			'inventory_id': inventory_id.id,
			'name': "Password: "+str(session_id.code),
			'code': "password",
		})
		values = {
			'session_id': session_id,
		}
		return request.redirect("/TSRGIST3000/"+str(session_id.id))

	@http.route(['/TSRGIST3000/<int:session>'],type='http', auth='user', website=True)
	def TSRGIST3000_event(self, session, **kw):
		if not session:
			return request.redirect("/")
		session_id = request.env['story.session'].search([('id','=',session)])
		chapter_id = session_id.story_id.chapter_ids.filtered(lambda c:c.sequence == session_id.chapter)
		values = {
			'session_id': session_id,
			'chapter_id': chapter_id,
			'event_id': chapter_id.event_ids.filtered(lambda e:e.sequence == session_id.event),
		}
		return request.render("kly.story", values)

