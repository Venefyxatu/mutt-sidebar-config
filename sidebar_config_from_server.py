#!/usr/bin/env python

# sidebar_config_from_server.py
#
############################################################################
# Script to populate a mutt sidebar configuration file
# File will be written to ~/.mutt/sidebar - you're the one who'll have to 
# include it in your mutt configuration.
#
# Configuration : 
#  * hiddenDirs : directories that you do not wish to show in the sidebar
#  * hiddenPatterns : patterns you wish to hide (currently just substrings)
#        TODO : make this more advanced.  Something with regexes.
#  * accounts : a dict containing your account information.  Format :
#                {server:(login, password)}
#  * fc : the other sidebar configuration.  Make sure the "mailboxes" 
#         directive remains unaltered and the list item of the list!
#
############################################################################
#
# Copyright (c) 2009, Erik Heeren
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.
# * Neither the name of the owner nor the names of its contributors may be used 
#   to endorse or promote products derived from this software without specific 
#   prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

import os
from Folderlist import FolderList

hiddenDirs = [ "Mail", "Drafts", "outbox", "Sent Mail", "Trash", 
               "Sync", "Calendar", "Contacts", "Journal", "Notes", "Tasks", "/",
               "RSS", "Junk", "Public", "Sent", "sent", "Shared", "Deleted Items"]

hiddenPatterns = [ "[Gmail]" ]

homeDir = os.getenv("HOME")
muttDir = os.path.join(homeDir, ".mutt")
# Accounts to check for folders.  {server:(login, password)}
accounts = {"imap.server1.com":("user@server1.com", "password"), "imap.server2.com":("user@server2.com", "password")}

fc = [ "set sidebar_width=30", 
       "set sidebar_visible=yes", 
       "set sidebar_delim=\"|\"", 
       "color sidebar_new yellow default", 
       "bind index \CP sidebar-prev", 
       "bind index \CN sidebar-next", 
       "bind index \CO sidebar-open", 
       "bind pager \CP sidebar-prev", 
       "bind pager \CN sidebar-next", 
       "bind pager \CO sidebar-open", 
       " ", 
       "mailboxes \\" ]

dirs = []

for account, authData in accounts.iteritems():
    fl = FolderList()
    folders = fl.retrieveFolders(account, authData[0], authData[1])
    for folder in folders:
        if folder in hiddenDirs or folder in accounts:
            continue
        patternFound = False
        for pattern in hiddenPatterns:
            if pattern in folder:
                patternFound = True
                continue
        if not patternFound:
            dirs.append("    imaps://%s/%s \\" % (account, folder))

dirs.sort()
fc = fc + dirs

fc = "\n".join(fc).rstrip("\\")

f = open(os.path.join(muttDir, "sidebar"), "w")
f.write(fc)
f.close()
