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

	@http.route(['/CYSTR'], type='http', auth='user', website=True)
	def CYSTR(self, **kw):
		solver_id = request.env['puzzle.solver'].search([('password','=','le mot de passe qui vous a été donné')])		
		values = {
			'solver_id': solver_id,
		}
		if kw:
			if 'answer' in kw.keys():
				if kw['answer'] == solver_id.solution:
					solver_id.solved = True
					return request.render("max_c.posttest", values)
				else:
					values['error'] = "wrong solution"
		return request.render("max_c.test", values)

	@http.route(['/CYSTR/<int:test>'], type="http", auth="user", website=True)
	def CYSTR_test(self, test, **kw):
		if not test:
			return request.redirect('/CYSTR')
		test_id = request.env['puzzle.part.test'].search([('id','=', int(test))])
		values = {
			'test_id': test_id,
		}
		if kw:
			if 'answer' in kw.keys():
				if kw['answer'].lower() == test_id.answer.lower():
					part_id = request.env['puzzle.part'].search([('test_id','=',test_id.id)])
					part_id.solved = True
				else:
					values['error'] = "wrong answer"

		return request.render("max_c.part_test", values)

	@http.route(['/CYSTR_solved'], type='http', auth='user', website=True)
	def CYSTR_solved(self, **kw):
		return request.render("max_c.posttest")