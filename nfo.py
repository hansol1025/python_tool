#!/usr/bin/env python

import os, sys, optparse
import xml.etree.cElementTree as ET

template_fn = "/volume2/Download/TBE/xbmc_movie.nfo"

def main() :
	p = optparse.OptionParser(description="Movie NFO Standalize program",
					prog="nfo.py",
					version="1.0a 2014/04/16",
					usage="%prog [nfo_filename]")
	p.add_option("-i", action="store_true", help="Update ID field with nfo filename", default=False, dest="updateid")
	p.add_option("-k", action="store_true", help="Backup before changing nfo", default=False, dest="backup")
	p.add_option("--rating", "-r", action="store", help="Rating to be set", dest="rating", nargs=1)
	p.add_option("--update", "-u", action="store", help="Update field indicated", dest="updateparam", nargs=2)
	p.add_option("--verbose", "-v", action="store_true", help="Enable verbose output", default=False)
	options, arguments = p.parse_args()
	if len(arguments) == 1 :
		nfo_fn = arguments[0]
		if not os.path.isfile(nfo_fn) or not os.path.exists(nfo_fn) :
			print "Invalid nfo file"
			sys.exit(1)
		source_tree = ET.ElementTree(file=nfo_fn)
	
		if options.updateid or options.rating :
			if options.updateid :
				update_id(source_tree, nfo_fn)
			if options.rating :
				update_node_text(source_tree, "rating", options.rating)
			res_tree = source_tree
		elif options.updateparam :
			field, param = options.updateparam
			print "Unimplemented feature, field="+field+", param="+param
			sys.exit(2)
			
		else :
			res_tree = transform_tree(template_fn, source_tree)
			update_id(res_tree, nfo_fn)
			
		if options.verbose :
			res_tree.write(sys.stdout)
		if options.backup :
			os.rename(nfo_fn, nfo_fn+'.bk')
		res_tree.write(nfo_fn, encoding='utf-8', xml_declaration=True)

		print "Execution done on: " + nfo_fn
	else :
		p.print_help()
		
def update_id(x_tree, filename) :
	id_elem = x_tree.find('id')
	# Unicode the filename if neccessary.
	if not isinstance(filename, unicode) :
		filename = filename.decode('utf-8')
	# TODO: should filter the characters except [-0-9a-zA-Z]
	short, extension = os.path.splitext(os.path.basename(filename))
	id_elem.text = short.upper()

def update_node_text(x_tree, node_tag, node_text) :
	elem = x_tree.find(node_tag)
	elem.text = node_text

# Convert XBMC generated nfo to the format of template nfo.
def transform_tree(template, src_tree) :
	t_tree = ET.ElementTree(file=template)

	for elem in src_tree.iter() :
		if elem.tag == u"title" :
			title = elem.text
		if elem.tag == u"year" :
			year = elem.text
		if elem.tag == u"runtime" :
			runtime = elem.text
		if elem.tag == u"set" :
			set = elem.text
		if elem.tag == u"director" :
			director = elem.text
		if elem.tag == u"studio" :
			studio = elem.text
		if elem.tag == u"company" :
			company = elem.text
		if elem.tag == u"plot" :
			plot = elem.text

	for elem in t_tree.iter() :
		if elem.tag == u"title" and ('title' in dir()) and title :
			elem.text = title
		if elem.tag == u"year" and ('year' in dir()) and year :
			elem.text = year
		if elem.tag == u"runtime" and ('runtime' in dir()) and runtime :
			elem.text = runtime
		if elem.tag == u"set" and ('set' in dir()) and set :
			elem.text = set
		if elem.tag == u"director" and ('director' in dir()) and director :
			elem.text = director
		if elem.tag == u"studio" and ('studio' in dir()) and studio :
			elem.text = studio
		if elem.tag == u"company" and ('company' in dir()) and company :
			elem.text = company
		if elem.tag == u"plot" and ('plot' in dir()) and plot:
			elem.text = plot	
			
	t_root = t_tree.getroot()
	for elem in src_tree.findall('actor') :
		role = elem.find('role')
		role.text = u'Herself'
		t_root.append(elem);

	for elem in src_tree.findall('genre') :
		elem.tag = u'tag'
		t_root.insert(23, elem);	# hardcode the insert position as no plan to reorg the nfo template structure.
	return t_tree

if __name__ == "__main__" :
	main()
