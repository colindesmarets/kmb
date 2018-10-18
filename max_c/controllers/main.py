# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.http import request
from odoo import http

class maxController(http.Controller):
	@http.route(['/CYSTR_start'], type='http', auth='public', website=True)
	def CYSTR_(self, **kw):
		error = ""
		if kw:
			if 'answer' in kw.keys():
				solver_id = request.env['puzzle.solver'].search([('password','=',str(kw['answer']))])
				if solver_id:
					print("---->")
					return request.redirect("/CYSTR_main")
				else:
					solver_id = request.env['puzzle.solver'].search([('password','=',"le mot de passe qui vous a été donné")])
					if solver_id:
						n = solver_id.login_tries + 1
						solver_id.login_tries = n
						if n == 1:
							error = "1ère erreur - Je suis un peu perplexe.. Je vous croyais meilleur"
						elif n == 2:
							error = "2ème erreur - Je viens de maudir toute votre famille"
						elif n == 3:
							error = "Et une troisème ! - Ok vous venez d'officiellement perdre tout mon respect"
						elif n == 4:
							error = "S'il vous plait arrêtez d'être mauvais, je ne sais plus quoi dire"
						elif n == 5:
							error = "..........."
						elif n == 6:
							error = "Wow vous avez quand même réussi à faire " + str(n) + " erreurs. Pas mal !"
						elif n == 7:
							error = "...........OK"
						else:
							error = "Tapez juste ''le mot de passe qui vous a été donné'' sans les guillemets..."
		return request.render("max_c.pretest", {'error': error})

	@http.route(['/CYSTR_main'], type='http', auth='public', website=True)
	def CYSTR(self, **kw):
		solver_id = request.env['puzzle.solver'].search([('password','=','le mot de passe qui vous a été donné')])		
		values = {
			'solver_id': solver_id,
		}
		if kw:
			if 'answer' in kw.keys():
				if kw['answer'].lower() == solver_id.solution.lower():
					solver_id.solved = True
					return request.render("max_c.posttest", values)
				else:
					values['error'] = "wrong solution"
		return request.render("max_c.test", values)

	@http.route(['/CYSTR/<int:test>'], type="http", auth="public", website=True)
	def CYSTR_test(self, test, **kw):
		if not test:
			return request.redirect('/CYSTR_main')
		test_id = request.env['puzzle.part.test'].search([('id','=', int(test))])
		part_id = request.env['puzzle.part'].search([('test_id','=',test_id.id)])
		values = {
			'test_id': test_id,
			'part_id': part_id,
		}
		if kw:
			if 'answer' in kw.keys():
				if kw['answer'].lower() == test_id.answer.lower():
					part_id = request.env['puzzle.part'].search([('test_id','=',test_id.id)])
					part_id.solved = True
					solver_id = request.env['puzzle.solver'].search([('password','=','le mot de passe qui vous a été donné')])		
					values = {
						'solver_id': solver_id,
					}
					return request.redirect('/CYSTR_main')
				else:
					if test_id.name == "Test 05":
						values['error'] = "va_mal"
					elif test_id.name == "Test 06":
						values['error'] = "wow"
					elif test_id.name == "Test 02":
						values['error'] = "glouglou"
					else:
						values['error'] = "wrong answer"

		return request.render("max_c.part_test", values)

	@http.route(['/CYSTR_solved'], type='http', auth='public', website=True)
	def CYSTR_solved(self, **kw):
		solver_id = None
		if kw:
			if 'answer' in kw.keys():
				solver_id = request.env['puzzle.solver'].search([('password','=',str(kw['answer']))])
			else:
				solver_id = request.env['puzzle.solver'].search([('password','=',"le mot de passe qui vous a été donné")])
		else:
			solver_id = request.env['puzzle.solver'].search([('password','=',"le mot de passe qui vous a été donné")])
		values = {
			'solver_id': solver_id,
		}
		if solver_id.solved:
			return request.render("max_c.posttest")
		else:
			return request.render("max_c.test", values)