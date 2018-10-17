# -*- coding: utf-8 -*-
from odoo import models,fields,api

class PuzzleSolver(models.Model):
	_name = "puzzle.solver"

	name = fields.Char(string="Name")
	solved = fields.Boolean(string="Solved")
	part_ids = fields.One2many("puzzle.part", "solver_id", string="Parts")
	solution = fields.Char(string="Solution")
	password = fields.Char(string="Password")
	login_tries = fields.Integer(string="Login tries")

class PuzzlePart(models.Model):
	_name = "puzzle.part"
	_order = "solver_id, sequence"

	name = fields.Char(string="Name")
	solver_id = fields.Many2one("puzzle.solver", string="Puzzle Solver")
	sequence = fields.Integer(string="Sequence")
	code = fields.Char(string="Code", help="Binary piece of the solver's solution")
	text_origin = fields.Text(string="Text")
	alphabet = fields.Char(string="Encryption Alphabet")
	key = fields.Integer(string="Encryption Key")
	text_encrypted = fields.Text(string="Encrypted text", compute="_encrypt_text", store=True)
	solved = fields.Boolean(string="Solved")
	test_id = fields.Many2one("puzzle.part.test", string="Test")

	@api.multi
	@api.depends("text_origin","key","alphabet")
	def _encrypt_text(self):
		for record in self:
			if record.key and record.alphabet and record.text_origin:
				encryption = ""
				for c in record.text_origin:
					if c in record.alphabet:
						position = record.alphabet.find(c)
						position += record.key
						position = position % len(record.alphabet)
						encryption += record.alphabet[position]
					elif c.lower() in record.alphabet:
						position = record.alphabet.find(c.lower())
						position += record.key
						position = position % len(record.alphabet)
						encryption += record.alphabet[position].upper()
					else:
						encryption += c
				record.text_encrypted = encryption
			else:
				record.text_encrypted = ""

class PuzzlePartTest(models.Model):
	_name = "puzzle.part.test"

	name = fields.Char(string="Name")
	question = fields.Text(string="Question")
	answer = fields.Char(string="Answer")
