# coding: utf-8
#
# author: https://github.com/vladiscripts
#
from scripts.db import session, Page, Ref, WarningTpls, queryDB
from config import *


def save_listpages_to_remove_warning_tpl():
	query = session.query(WarningTpls.title) \
		.select_from(WarningTpls) \
		.outerjoin(Ref, WarningTpls.page_id == Ref.page_id) \
		.filter(Ref.page_id.is_(None))

	list_to_remove_warning_tpl = (str(title[0]) for title in queryDB(query))
	file_savelines(filename_list_to_remove_warning_tpl, sorted(list_to_remove_warning_tpl))


def save_listpages_to_add_warning_tpl():
	"""Список куда предупреждение ещё не поставлено."""
	query = session.query(Page.title).select_from(Page) \
		.outerjoin(WarningTpls) \
		.join(Ref, Page.page_id == Ref.page_id) \
		.filter(WarningTpls.page_id.is_(None), Ref.page_id.isnot(None)) \
		.group_by(Page.title)

	errpages_without_warning_tpl = (str(title[0]) for title in queryDB(query))
	file_savelines(filename_listpages_errref_where_no_yet_warning_tpl, errpages_without_warning_tpl)


def file_savelines(filename, strlist, append=False):
	mode = 'a' if append else 'w'
	text = '\n'.join(strlist)
	with open(filename, mode, encoding='utf-8') as f:
		f.write(text)


def file_savetext(filename, text):
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(text)
