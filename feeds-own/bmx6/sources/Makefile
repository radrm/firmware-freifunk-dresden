# Copyright (c) 2010  BMX protocol contributors
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA


  GIT_REV = $(shell ( [ "$(REVISION_VERSION)" ] && echo "$(REVISION_VERSION)" ) || ( [ -d .git ] && git --no-pager log -n 1 --oneline|cut -d " " -f 1 ) ||  echo 0)
  CFLAGS += -pedantic -Wall -W -Wno-unused-parameter -Os -g3 -std=gnu99 -DGIT_REV=\"$(GIT_REV)\"
#-DHAVE_CONFIG_H

# optinal defines:
# CFLAGS += -static
# CFLAGS += -pg   # "-pg" with openWrt causes "gcrt1.o: No such file"! Needs ld -o myprog /lib/gcrt0.o myprog.o utils.o -lc_p, grep: http://www.cs.utah.edu/dept/old/texinfo/as/gprof.html


# paranoid defines (helps bug hunting during development):
# CFLAGS += -DEXTREME_PARANOIA -DEXIT_ON_ERROR -DPROFILING 

# Some test cases:
# CFLAGS += -DTEST_LINK_ID_COLLISION_DETECTION
# CFLAGS += -DTEST_DEBUG          # (testing syntax of __VA_ARGS__ dbg...() macros)
# CFLAGS += -DTEST_DEBUG_MALLOC   # allocates a never freed byte which should be reported at bmx6 termination
# CFLAGS += -DAVL_DEBUG -DAVL_TEST

# optional defines (you may disable these features if you dont need them)
CFLAGS += -DNO_DEBUG_ALL
CFLAGS += -DNO_DEBUG_DUMP
CFLAGS += -DNO_DEBUG_TRACK
CFLAGS += -DNO_DEBUG_SYS
# CFLAGS += -DLESS_OPTIONS
CFLAGS += -DNO_TRAFFIC_DUMP
CFLAGS += -DNO_DYN_PLUGIN
CFLAGS += -DNO_TRACE_FUNCTION_CALLS
CFLAGS += -DNO_DEBUG_MALLOC
CFLAGS += -DNO_MEMORY_USAGE

# experimental or advanced defines (please dont touch):
CFLAGS += -DNO_ASSERTIONS       # (disable syntax error checking and error-code creation!)
# CFLAGS += -DEXTREME_PARANOIA    # (check difficult syntax errors)
# CFLAGS += -DEXIT_ON_ERROR       # (exit and return code due to unusual behavior)
# CFLAGS += -DTEST_DEBUG
# CFLAGS += -DWITH_UNUSED	  # (includes yet unused stuff and buggy stuff)
# CFLAGS += -DEXPORT_UNUSED       # (export only locally used stuff)
# CFLAGS += -DPROFILING           # (no static functions -> better profiling and cores)
# CFLAGS += -DNO_DEPRECATED	  # (for backward compatibility)

#EXTRA_CFLAGS += 
#EXTRA_LDFLAGS +=

#for profiling:
#EXTRA_CFLAGS="-DPROFILING -pg"

#for embedded stuff (reducing binary size and cpu footprint):
#EXTRA_CFLAGS="-DNO_DEBUG_ALL -DNO_DEBUG_TRACK -DNO_TRAFFIC_DUMP -DNO_DEBUG_MALLOC -DNO_MEMORY_USAGE -DNO_TRACE_FUNCTION_CALLS -DNO_ASSERTIONS"


LDFLAGS += -g3

LDFLAGS += $(shell echo "$(CFLAGS) $(EXTRA_CFLAGS)" | grep -q "DNO_DYNPLUGIN" || echo "-Wl,-export-dynamic -ldl" )
LDFLAGS += $(shell echo "$(CFLAGS) $(EXTRA_CFLAGS)" | grep -q "DPROFILING" && echo "-pg -lc" )




SBINDIR =       $(INSTALL_PREFIX)/usr/sbin

SRC_FILES= "\(\.c\)\|\(\.h\)\|\(Makefile\)\|\(INSTALL\)\|\(LIESMICH\)\|\(README\)\|\(THANKS\)\|\(./posix\)\|\(./linux\)\|\(./man\)\|\(./doc\)"

SRC_C =  bmx.c msg.c metrics.c tools.c plugin.c list.c allocate.c avl.c iid.c hna.c control.c schedule.c ip.c cyassl/sha.c cyassl/random.c cyassl/arc4.c
SRC_H =  bmx.h msg.h metrics.h tools.h plugin.h list.h allocate.h avl.h iid.h hna.h control.h schedule.h ip.h cyassl/sha.h cyassl/random.h cyassl/arc4.h

SRC_C += $(shell echo "$(CFLAGS) $(EXTRA_CFLAGS)" | grep -q "DNO_TRAFFIC_DUMP" || echo dump.c )
SRC_H += $(shell echo "$(CFLAGS) $(EXTRA_CFLAGS)" | grep -q "DNO_TRAFFIC_DUMP" || echo dump.h )

OBJS=  $(SRC_C:.c=.o)

#
#


PACKAGE_NAME=	bmx6
BINARY_NAME=	bmx6


all:	
	$(MAKE) $(BINARY_NAME)
	# further make targets: help, libs, build_all, strip[_libs|_all], install[_libs|_all], clean[_libs|_all]

libs:	all
	$(MAKE)  -C lib all CORE_CFLAGS='$(CFLAGS)'



$(BINARY_NAME):	$(OBJS) Makefile
	$(CC)  $(OBJS) -o $@  $(LDFLAGS) $(EXTRA_LDFLAGS)

%.o:	%.c %.h Makefile $(SRC_H)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) -c $< -o $@

%.o:	%.c Makefile $(SRC_H)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) -c $< -o $@


strip:	all
	strip $(BINARY_NAME) 

strip_libs: all libs
	$(MAKE) -C lib strip




install:	all
	mkdir -p $(SBINDIR)
	install -m 0755 $(BINARY_NAME) $(SBINDIR)

install_libs:   all
	$(MAKE) -C lib install CORE_CFLAGS='$(CFLAGS)'


	
clean:
	rm -f $(BINARY_NAME) *.o posix/*.o linux/*.o cyassl/*.o

clean_libs:
	$(MAKE) -C lib clean


clean_all: clean clean_libs
build_all: all libs
strip_all: strip strip_libs
install_all: install install_libs


help:
	# further make targets:
	# help					show this help
	# all					compile  bmx6 core only
	# libs			 		compile  bmx6 plugins
	# build_all				compile  bmx6 and plugins
	# strip / strip_libs / strip_all	strip    bmx6 / plugins / all
	# install / install_libs / install_all	install  bmx6 / plugins / all
	# clean / clean_libs / clean_all	clean    bmx6 / libs / all

