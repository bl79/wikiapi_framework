#!/usr/bin/env python3
# coding: utf8
#
# author: https://github.com/vladiscripts
#
from config import *
from make_list_pages_with_referrors import *
import make_list_pages_with_referrors
import db

# Сканирование и обновление базы данных
if not only_save_lists_no_generation:
	lists = MakeLists()
	pwb_format = True
	if make_wikilist:
		saved_filenames = MakeWikiList()


import os
python_and_path = r'python scripts/'
pwb_cfg = r' -dir:~/.pywikibot/'
# python_and_path = r'python3 scripts/'

# логин
os.system(python_and_path + 'login.py' + pwb_cfg)

# Запись списков
if do_post_list:
	sim = ' -simulate' if do_post_list_simulate else ''  # "-simulate" параметр для тестирования записи pwb
	params = [
		'-file:' + filename_part + '.txt',
		'-begin:"' + marker_page_start + '"', '-end:"' + marker_page_end + '"', '-notitle',
		'-summary:"обновление списка"',
		'-pt:1 -maxlag:15', pwb_cfg,
		'-force', sim,
	]
	# cmd = python_and_path + 'pagefromfile.py -force' + sim + ' -file:' + filename_part + '.txt' + ' -start:"{{-start-}}" -end:"{{-end-}}" -notitle -summary:"обновление списка" -maxlag:15'
	os.system(python_and_path + 'pagefromfile.py' + ' ' + ' '.join(params))

# Простановка в статьях шаблона про ошибки
if do_post_template:
	sim = ' -simulate' if do_post_template_simulate else ''
	params = [
		'-file:' + filename_listpages_errref_where_no_yet_warning_tpl,
		'-text:"{{' + warning_tpl_name + '}}"',
		# '-except:"' + warning_tpl_regexp + '"',
		u'-summary:"+шаблон: некорректные викиссылки в сносках"',
		'-pt:1 -maxlag:15', pwb_cfg,
		'-always', sim,
	]
	# cmd = python_and_path + 'add_text.py' + sim + ' -file:' + filename_listpages_errref_where_no_yet_warning_tpl + ' -text:"{{' + warning_tpl_name + '}}" -except:"' + warning_tpl_regexp + '" -summary:"+шаблон: некорректные викиссылки в сносках" -pt:1 -maxlag:15'
	os.system(python_and_path + 'add_text.py' + ' ' + ' '.join(params))


# Удаление шаблона из статей
if do_remove_template:
	sim = '-simulate' if do_remove_template_simulate else ''
	params = [
		'-regex "' + warning_tpl_regexp + '.*?}}" ""', '-nocase', '-dotall',
		'-file:' + filename_list_to_remove_warning_tpl, '-ns:0',
		'-summary:"-шаблон: ошибочных викиссылок в сносках не найдено"',
		'-pt:1 -maxlag:15', pwb_cfg,
		'-always', sim,
	]
	# cmd = python_and_path + 'replace.py' + sim + ' -file:' + filename_list_to_remove_warning_tpl + ' -ns:0 -nocase -dotall -regex "' + warning_tpl_regexp + '.*?}}" "" -summary:"-шаблон: викиссылки в сносках исправны" -pt:1 -maxlag:15'
	os.system(python_and_path + 'replace.py' + ' ' + ' '.join(params))
