#################################################################################
# GLOBALS                                                                       #
#################################################################################

BOKEH_SERVER_APP_NAME = bokeh-server-apps
FLASK_APP_NAME = owd-flask-app

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Get data
get-data:
	@echo "+ $@"
	@tox -e get-data
.PHONY: get-data

## Remove Python artifacts
clean-py:
	@echo "+ $@"
	@find ./$(BOKEH_SERVER_APP_NAME) -type f -name "*.py[co]" -delete
	@find ./$(BOKEH_SERVER_APP_NAME) -type d -name "__pycache__" -delete
	@find ./$(FLASK_APP_NAME) -type f -name "*.py[co]" -delete
	@find ./$(FLASK_APP_NAME) -type d -name "__pycache__" -delete
.PHONY: clean-py

## Run build with tox
build:
	@echo "+ $@"
	@tox -e build
.PHONY: build

## Run Flask app
flask:
	@echo "+ $@"
	@tox -e flask
.PHONY: flask

## Run multi-app Bokeh server
bokeh:
	@echo "+ $@"
	@tox -e bokeh
.PHONY: bokeh

## Create Heroku Bokeh Server app
heroku-create-bokehserver:
	@echo "+ $@"
	@heroku create $(BOKEH_SERVER_APP_NAME)
.PHONY: heroku-create-bokeh

## Create Heroku Flask app
heroku-create-flask:
	@echo "+ $@"
	@heroku create $(FLASK_APP_NAME)
.PHONY: heroku-create-flask

## Add a remote to local repository of existing Bokeh Server app
heroku-add-bokehserver-remote:
	@echo "+ $@"
	@heroku git:remote -a $(BOKEH_SERVER_APP_NAME)
.PHONY: heroku-add-bokehserver-remote

## Add a remote to local repository of existing Flask Server app
heroku-add-flask-remote:
	@echo "+ $@"
	@heroku git:remote -a $(FLASK_APP_NAME)
.PHONY: heroku-add-flask-remote

## Deploy Bokeh Server app from sub-directory to Heroku
heroku-deploy-bokehserver-app:
	@echo "+ $@"
	@git subtree push --prefix $(BOKEH_SERVER_APP_NAME) heroku main
.PHONY: heroku-deploy-bokehserver-app

## Deploy Flask app from sub-directory to Heroku
heroku-deploy-flask-app:
	@echo "+ $@"
	@git subtree push --prefix $(FLASK_APP_NAME) heroku main
.PHONY: heroku-deploy-flask-app

## Heroku workflow to push to existing Flask-embedded Bokehserver app
.PHONY: heroku-push-bokehserver
heroku-push-bokehserver: heroku-add-bokehserver-remote heroku-deploy-bokehserver-app

## Heroku workflow to push to existing Flask-embedded Bokehserver app
.PHONY: heroku-push-flask
heroku-push-flask: heroku-add-flask-remote heroku-deploy-flask-app

## Heroku workflow to create new Flask-embedded Bokehserver app
.PHONY: heroku-create
heroku-create: heroku-create-bokehserver heroku-create-flask heroku-push-bokehserver heroku-push-flask

## Heroku workflow to update existing Flask-embedded Bokehserver app
.PHONY: heroku-update
heroku-update: heroku-push-bokehserver heroku-push-flask

## Delete single Heroku app
heroku-stop:
	@echo "+ $@"
	@heroku apps:destroy --app $(HD_APP_NAME) --confirm $(HD_APP_NAME)
.PHONY: heroku-delete

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
