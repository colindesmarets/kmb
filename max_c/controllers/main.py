# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.http import request
from odoo import http

class maxController(http.Controller):
	@http.route(['/CYSTR_'], type='http', auth='user', website=True)
	def CYSTR_(self, **kw):
		error = ""
		if kw:
			if 'answer' in kw.keys():
				solver_id = request.env['puzzle.solver'].search([('password','=',str(kw['answer']))])
				if solver_id:
					print("---->")
					return request.redirect("/CYSTR")
				else:
					solver_id = request.env['puzzle.solver'].search([('password','=','the password that was given to you')])
					if solver_id:
						n = solver_id.login_tries + 1
						solver_id.login_tries = n
						if n == 1:
							error = "1st mistake - I'm a bit disapointed.. thought you were smarter"
						elif n == 2:
							error = "2nd mistake - I placed a curse on your family"
						elif n == 3:
							error = "And a 3rd one - Ok you definitely lost all my respect now"
						elif n == 4:
							error = "Please stop being wrong I have no more custom messages to put here"
						elif n == 5:
							error = "..........."
						elif n == 6:
							error = "Wow you actually managed to make " + str(n) + " mistakes"
						elif n == 7:
							error = "...........OK"
						else:
							error = "Just type 'the password that was given to you' without the quotes jeez"
		return request.render("max.pretest", {'error': error})

	@http.route(['/CYSTR'], type='http', auth='user', website=True)
	def CYSTR(self, **kw):
		solver_id = request.env['puzzle.solver'].search([('password','=','the password that was given to you')])
		values = {
			'solver_id': solver_id,
		}
		return request.render("max.test", values)
