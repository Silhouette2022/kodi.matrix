#!/usr/bin/python
# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by tknorris:
# *  https://offshoregit.com/tknorris/tknorris-release-repo/raw/master/addons_xml_generator2.py
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
# *
# *  Changes since v2:
# *  - (assumed) zips reside in folder "download"
# *  - md5 checksum creation added for zips
# *  - Skip moving files and zip creation if zip file for the same version already exists
# *  - alphabetical sorting

""" addons.xml generator """

import os
import sys
import time
import re
import xml.etree.ElementTree as ET
try:
    import shutil, zipfile
except Exception as e:
    print('An error occurred importing module!\n%s\n' % e)
 
# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
print(sys.version)
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x
 
class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__(self):
        # generate files
        self._generate_zips_md5()
        self._generate_addons_file()
        self._generate_md5_file("addons.xml")
        # notify user
        print("Finished updating addons xml and md5 files\n")
 
    def _generate_addons_file(self):
        # addon list
        addons = sorted(os.listdir("./source/"))
        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                addon = "./source/"+addon
                # skip any file or .svn folder or .git folder
                if (not os.path.isdir(addon) or addon == ".svn" or addon == ".git" or addon == ".github" or addon == "download"): continue
                # create path
                _path = os.path.join(addon, "addon.xml")
                # split lines for stripping
                xml_lines = open(_path, "r").read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if (line.find("<?xml") >= 0): continue
                    # add line
                    if sys.version < '3':
                        addon_xml += unicode(line.rstrip() + "\n", "UTF-8")
                    else:
                        addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print("Excluding %s for %s" % (_path, e))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        # save file
        self._save_file(addons_xml.encode("UTF-8"), file="addons.xml")
 
    def _generate_md5_file( self, fname ):
        # create a new md5 hash
        try:
            import md5
            m = md5.new(open(fname, "r").read()).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5(open(fname, "r", encoding="UTF-8").read().encode("UTF-8")).hexdigest()
 
        # save file
        try:
            self._save_file(m.encode("UTF-8"), file=fname + ".md5")
        except Exception as e:
            # oops
            print("An error occurred creating %s.md5 file!\n%s" % (fnam, e))
 
    def _save_file(self, data, file):
        try:
            # write data to the file (use b for Python 3)
            open(file, "wb").write(data)
        except Exception as e:
            # oops
            print("An error occurred saving %s file!\n%s" % (file, e))
 
    def _generate_zips_md5( self ):
        # addon list
        addons = os.listdir( "./source/repo/" )
        #print addons
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                addon = "./source/repo/"+addon
                #print addon
                if ( not os.path.isdir( addon ) or addon == ".svn" ): continue
                # create path
                zips = os.listdir( addon )
                #print zips
                for zip in zips:
                    #print zip
                    if zip.endswith(".zip"):
                      md5f = addon + "/" + zip
                      #print md5f
                      self._generate_md5_file(md5f)
            except Exception, e:
                # missing or poorly formatted addon.xml
                print "Error creating md5 for zip %s : %s" % ( zip, e, ) 
 
def zipfolder(foldername, target_dir, zips_dir, addon_dir):
    zipobj = zipfile.ZipFile(zips_dir + foldername, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for f in files:
            fn = os.path.join(base, f)
            zipobj.write(fn, os.path.join(addon_dir, fn[rootlen:]))
    zipobj.close()


                     
if (__name__ == "__main__"):
    # start
    Generator()
    print('Done')
