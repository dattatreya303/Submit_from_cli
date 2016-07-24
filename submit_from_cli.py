#!/usr/bin/python

import argparse, getopt, requests, os, sys, mechanize, time, getpass
from bs4 import BeautifulSoup as BS

def signIn(br, userid, pwd):
	br.open('https://www.spoj.com/login')
	br.select_form(nr = 0)
	br.form['login_user'] = userid
	br.form['password'] = pwd
	# br.form['autologin'] = True
	page = br.submit()
	s = BS(page.read(), 'html.parser')
	err = s.select('.text-danger span')
	if len(err) > 0:
		print('Invalid User name or password')
		sys.exit(2)
	print "Signed in."

def submitSol(br, prob_code, lang, path_toGlory):
	# dictionary of codes for languages
	lang_dict = {'C++':'1', 'Python':'4', 'Java':'10', 'C':'11', 'Python3':'116'}

	br.open('https://www.spoj.com/submit/' + prob_code)
	br.select_form(nr = 0)
	br.form['lang'] = [lang_dict[lang]]
	br.form.add_file(open(path_toGlory), 'text/plain', path_toGlory)
	print "Running judge...",
	br.submit(name='submit')
	time.sleep(3)
	# print(br.geturl())

def seeResult(br, userid):
	page = br.open('https://www.spoj.com/status/' + userid)
	print "Done"
	html = BS(page.read(), 'html.parser')
	props = html.tbody.tr
	
	status_code = {'11': 'Compilation Error', '12':'Runtime Error', '13':'Time Limit Exceeded', '14':'Wrong Answer', '15':'Accepted'}

	st = props.select('td:nth-of-type(5)')
	print 'Status:', status_code[str(st[0].get('status'))]
	tm = props.select('td:nth-of-type(6)')
	print 'Time:', tm[0].a.getText().encode("utf-8").strip()
	mem = props.select('td:nth-of-type(7)')	
	print 'Memory:', mem[0].getText().encode("utf-8").strip()

def main():
	prob_code = raw_input("Problem code: ")
	# instantiate browser
	br = mechanize.Browser(factory=mechanize.RobustFactory())
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(mechanize.HTTPRedirectHandler)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	# br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Firefox'), ('Accept-Encoding','gzip')]

	# checking if problem exists
	submit_url = 'https://www.spoj.com/problems/' + prob_code
	res = br.open(submit_url)
	# print(res.geturl())
	soup = BS(res.read(), 'html.parser')
	pr = soup.select('#problem-name')
	if pr == []:
		print("Wrong problem code!")
		sys.exit(2)
	print "Found problem statement."
	
	lang = raw_input("Language: ")
	
	# sign in with SPOJ account
	userid = raw_input("User name: ")
	pwd = getpass.getpass("Password: ")
	signIn(br, userid, pwd)

	# submit the solution
	# all problem codes on spoj are in upper characters
	path_toGlory = raw_input("Enter full filepath: ")
	
	submitSol(br, prob_code.upper(), lang, path_toGlory)

	# show result status
	seeResult(br, userid)

if __name__ == "__main__":
	main()