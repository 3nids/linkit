####################################################
# Ultimate QGIS plugin Makefile
####################################################

# REQUIREMENTS
# 1. Folder name is the plugin name
# 2. Resource file is at ./resources.qrc

# TIPS
# 1. If .ui files are in a subfolder
#     create a file resources_rc.py with:
#     from ..resources_rc import *

####################################################
# CONFIGURATION

# QGIS DIR
QGISDIR = $(HOME)/.qgis2

# ICONS FOLDER
ICONS_DIR = icons

# UI FILES FOLDER
UI_DIR = ui

# TRANSLATION FILES FOLDER
LN_DIR = i18n

# COMMAND TO RUN DEFAULT APPLICATION (launch a URL)
# Linux 'open' or 'xdg-open' / OSX: 'open' / Win: 'start'
OPEN = xdg-open



###################################################
# DO NOT EDIT BELOW !

PLUGINNAME =$(shell basename $(CURDIR))
VERSION = `cat $(PLUGINNAME)/metadata.txt | grep version | sed 's/version=//'`

PY_FILES = $(find . -name '*.py' ! -name "ui_*.py")
EXTRAS = metadata.txt resources.qrc

UI_SOURCES=$(wildcard $(UI_DIR)/*.ui)
UI_FILES=$(join $(dir $(UI_SOURCES)), $(notdir $(UI_SOURCES:%.ui=%.py)))

RC_SOURCES=$(wildcard *.qrc)
RC_FILES=$(join $(dir $(RC_SOURCES)), $(notdir $(RC_SOURCES:%.qrc=%_rc.py)))

LN_SOURCES=$(wildcard $(LN_DIR)/*.ts)
LN_FILES=$(join $(dir $(LN_SOURCES)), $(notdir $(LN_SOURCES:%.ts=%.qm)))

GEN_FILES = ${UI_FILES} ${RC_FILES}

all: $(GEN_FILES)
ui: $(UI_FILES)
resources: $(RC_FILES)

$(UI_FILES): ui/%.py: ui/%.ui
	pyuic4 -o $@ $<

$(RC_FILES): %_rc.py: %.qrc
	pyrcc4 -o $@ $<

$(LN_FILES): i18n/%.qm: i18n/%.ts
	lrelease-qt4 $<

clean:
	rm -f $(GEN_FILES) *.pyc
	find $(CURDIR) -iname "*.pyc" -delete

compile: $(UI_FILES) $(RC_FILES) $(LN_FILES)

transup:
	pylupdate4 -noobsolete $(UI_SOURCES) $(PY_FILES) -ts i18n/$(PLUGINNAME)_fr.ts

deploy: compile transup
	mkdir -p $(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -rvf * $(QGISDIR)/python/plugins/$(PLUGINNAME)/
	rm -f $(QGISDIR)/python/plugins/$(PLUGINNAME)/$(PLUGINNAME).zip

# The dclean target removes compiled python files from plugin directory
dclean:
	find $(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	rm -f $(QGISDIR)/python/plugins/$(PLUGINNAME)/$(PLUGINNAME).zip

# The derase deletes deployed plugin
derase:
	rm -Rf $(QGISDIR)/python/plugins/$(PLUGINNAME)

zip: clean deploy dclean
	rm -f $(PLUGINNAME)-$(VERSION).zip
	cd $(QGISDIR)/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME)

publish: zip
	$(OPEN) http://plugins.qgis.org/plugins/$(PLUGINNAME)/version/add/ &


