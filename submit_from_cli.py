import argparse, getopt, requests, os, sys, mechanize, time
from bs4 import BeautifulSoup as BS

def signIn(br, userid, pwd):
	print "Signing in...",
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
	print "Done"

def submitSol(br, prob_code, path_toGlory):
	br.open('https://www.spoj.com/submit/' + prob_code)
	br.select_form(nr = 0)
	br.form['lang'] = ['1']
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
	
	st = props.select('td:nth-of-type(5)')
	print 'Status:', st[0].strong.getText().encode("utf-8").strip()
	tm = props.select('td:nth-of-type(6)')
	print 'Time:', tm[0].a.getText().encode("utf-8").strip()
	mem = props.select('td:nth-of-type(7)')
	print 'Memory:', mem[0].getText().encode("utf-8").strip()

def main():
	# prob_code, path_toGlory = get_arguments(sys.argv[1:])
	prob_code = 'AGGRCOW'
	path_toGlory = '/home/dattatreya/Desktop/C, CPP Files/AGGRCOW.cpp'
	# default prob_code is name of the solution file
	# submit_url = 'https://www.codechef.com/submit/' + prob_code.upper()
	
	userid = 'dattatreya_98'
	pwd = 'Chiku@1998'

	# dictionary of codes for languages
	lang_dict = ['C++':'1', 'C':'11', 'Java':'10', 'Python':'4', 'Python3':'116']

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
	soup = BS(res.read(), 'html.parser')
	err = soup.center.h1
	if err != None:
		print(err.getText())
		sys.exit(2)

	# sign in with SPOJ account
	signIn(br, userid, pwd)

	# submit the solution
	# all problem codes on spoj are in upper characters
	submitSol(br, prob_code.upper(), path_toGlory)

	# show result status
	seeResult(br, userid)

if __name__ == "__main__":
	main()