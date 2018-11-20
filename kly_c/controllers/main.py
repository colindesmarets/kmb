# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.http import request
from odoo import http

class klyController(http.Controller):
	@http.route(['/TSRGIST3000_'], type='http', auth='user', website=True)
	def TSRGIST3000_(self, **kw):
		return request.render("kly_c.pretest")

	@http.route(['/TSRGIST3000'],type='http', auth='user', website=True)
	def TSRGIST3000(self, **kw):
		return request.render("kly_c.home")

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
		# item_03 = request.env['inventory.item'].create({
		# 	'inventory_id': inventory_id.id,
		# 	'name': "Password: "+str(session_id.code),
		# 	'code': "password",
		# })
		code_6 = request.env['story.answer'].search([('code','=','6')])
		if code_6:
			code_6.unlink()
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
		return request.render("kly_c.story", values)

	def get_next(self, chapter_id, event_id):
		next_event_seq = event_id.sequence + 1
		next_chapter_id = None
		next_event_id = None
		if chapter_id.event_ids.filtered(lambda e:e.sequence == event_id.sequence + 1):
			next_chapter_id = chapter_id
			next_event_id = chapter_id.event_ids.filtered(lambda e:e.sequence == event_id.sequence + 1)
		else:
			next_chapter_id = chapter_id.story_id.chapter_ids.filtered(lambda c:c.sequence == chapter_id.sequence + 1)
			next_event_id = next_chapter_id.event_ids.filtered(lambda e:e.sequence == 1)
		return next_chapter_id, next_event_id

	@http.route(['/TSRGIST3000/answer'],type='http', auth='user', website=True)
	def TSRGIST3000_answer(self, **kw):
		chapter_id = request.env['story.chapter'].search([('id','=',int(kw['chapter_id']))])
		event_id = request.env['story.event'].search([('id','=',int(kw['event_id']))])
		session_id = request.env['story.session'].search([('id','=',int(kw['sess_id']))])

		next_chapter_id, next_event_id = self.get_next(chapter_id=chapter_id, event_id=event_id)
		next_next_chapter_id, next_next_event_id = self.get_next(chapter_id=next_chapter_id, event_id=next_event_id)
		next_next_next_chapter_id, next_next_next_event_id = self.get_next(chapter_id=next_next_chapter_id, event_id=next_next_event_id)

		if event_id.question_id.name == "partner name":
			session_id.partner_name = kw['answer']
			if 'colin' in session_id.partner_name.lower():
				session_id.partner_name = "Maxime"
				next_event_id.text = "Unfortunately he's living too far away so we'll say it's Maxime for the realism of the story"
			elif 'maxime' in session_id.partner_name.lower() or 'max' in session_id.partner_name.lower():
				next_event_id.text = "Of course we all know he's not your real beloved one but he's not living at the end of the world..."
			else:
				next_event_id.text = "Ok ... Thought you'd choose somebody else but it's your story after all"
			next_next_event_id.text = "Okay. Let me start again then:\nHere you are, lying next to "+ str(session_id.partner_name) +", trying to sleep, closing your eyes and ...\nWAIT ?! Don't actually close them or we'll be in trouble as i didn't record an audio version..."
			next_next_next_event_id.text = "OK for the last time ! Let's do this right.\nSo you're in your bed with "+ str(session_id.partner_name) +", feeling sleepy and so on, blablabla.\nWhen SUDDENLY you here strange noises from the attic.\n(Yeah you have a attic in this story because you're rich !)"
			
		elif event_id.question_id.name == "pick shiny":
			if 'yes' in kw['answer'].lower():
				next_event_id.text = "Verry wise choice !\n----Broadsword added to inventory----"
			elif 'no' in kw['answer'].lower():
				next_event_id.text = "Ok, I'll take it for you then. It could be usefull.... who knows...\n----Broadsword added to inventory----"
			else:
				next_event_id.text = "Thought you could fool me with a meaningless answer ?\n I'll just force you to pick it up then.\n----Broadsword added to inventory----"
			broadsword = request.env['inventory.item'].create({
				'inventory_id': session_id.inventory_id.id,
				'name': "Broadsword",
				'code': "broadsword",
			})

		elif event_id.question_id.name == "feeling":
			feeling = request.env['inventory.item'].create({
				'inventory_id': session_id.inventory_id.id,
				'name': str(kw['answer'])+" feeling",
				'code': "feeling",
			})
			next_event_id.text = "----"+str(kw['answer'])+" feeling added to inventory----"
			feeling_answer = request.env['story.answer'].create({
				'question_id': request.env['story.question'].search([('name','=','reaction')]).id,
				'name': "6) Use your "+str(kw['answer'])+" feeling to make a scene",
				'code': '6',
			})

		elif event_id.question_id.name == "reaction":
			answer_id = event_id.question_id.answer_ids.filtered(lambda a:a.code == kw['answer'])
			if not answer_id:
				values = {
					'error_answer': "The answer '"+str(kw['answer'])+"' does not exist...",
					'session_id': session_id,
					'chapter_id': chapter_id,
					'event_id': event_id,
				}
				return request.render("kly_c.story", values)
			else:

				if answer_id.code == "27":
					# fight
					print("27")
					chapter_id = request.env['story.chapter'].search([('sequence','=',2)])
				elif answer_id.code == "31":
					# destiny
					print("31")
					chapter_id = request.env['story.chapter'].search([('sequence','=',2)])
				elif answer_id.code == "42":
					# nothing
					print("42")
					chapter_id = request.env['story.chapter'].search([('sequence','=',2)])
				elif answer_id.code == "54":
					# dog noises
					print("54")
					chapter_id = request.env['story.chapter'].search([('sequence','=',2)])
				elif answer_id.code == "6":
					# feeling
					print("6")
					chapter_id = request.env['story.chapter'].search([('sequence','=',2)])
				event_id = chapter_id.event_ids.filtered(lambda e:e.sequence == int(answer_id.code))
				if answer_id.code == "6":
					feeling_item = request.env['inventory.item'].search([('code','=','feeling')])
					event_id.text = "Your "+str(feeling_item.name)+" does not seem to affect her.\nYou could think robots can't understand feelings but actually she's a dog..."
					if feeling_item:
						feeling_item.unlink()
					feeling_answer = request.env['story.answer'].search([('code','=','6')])
					if feeling_answer:
						feeling_answer.unlink()

				session_id.chapter = chapter_id.sequence
				session_id.event = event_id.sequence
				values = {
					'session_id': session_id,
					'chapter_id': chapter_id,
					'event_id': event_id,
				}
				return request.render("kly_c.story", values)

		session_id.chapter = next_chapter_id.sequence
		session_id.event = next_event_id.sequence
		values = {
			'session_id': session_id,
			'chapter_id': next_chapter_id,
			'event_id': next_event_id,
		}
		return request.render("kly_c.story", values)

	@http.route(['/TSRGIST3000/<int:session>/next'],type='http', auth='user', website=True)
	def TSRGIST3000_next(self, session, **kw):
		session_id = request.env['story.session'].search([('id','=',session)])
		chapter_id = session_id.story_id.chapter_ids.filtered(lambda c:c.sequence == session_id.chapter)
		event_id = chapter_id.event_ids.filtered(lambda e:e.sequence == session_id.event)

		if session_id.chapter == 4 and session_id.event == 6:
			values = {
				'session_id': session_id,
			}
			return request.render("kly_c.ending", values)

		next_chapter_id, next_event_id = self.get_next(chapter_id=chapter_id, event_id=event_id)
		if chapter_id.sequence == 2:
			if event_id.sequence in [6,42,54,27]:
				next_chapter_id = chapter_id
				next_event_id = next_chapter_id.event_ids.filtered(lambda e:e.sequence == 5)

		session_id.chapter = next_chapter_id.sequence
		session_id.event = next_event_id.sequence

		if next_chapter_id.sequence == 2 and next_event_id.sequence == 1:
			next_event_id.text = "Back to your room you find Aïki in the exact same spot (Yes she was there all along. No it's not a glitch.)\nSo you decide to give her a HUGE hug."
		values = {
			'session_id': session_id,
			'chapter_id': next_chapter_id,
			'event_id': next_event_id,
		}
		return request.render("kly_c.story", values)

	@http.route(['/TSRGIST3000/end'], type='http', auth='user', website=True)
	def TSRGIST3000_end(self, **kw):
		return request.render("kly_c.ending")
