.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

prepare-env: ## Install the service's dependencies
	@echo -e "\e[1;34mmaking new virtual environment and installing dependencies ...\e[0m" && \
		pipenv install


run-tests-locally: prepare-env ## Running the service's tests locally
	@echo -e "\e[1;34mrunning tests locally ...\e[0m" && \
		pipenv run py.test \
			-r s \
			-vvs \
			--cov . test \
			--cov-report term-missing \
			--cov-report html:cov_html \
			--cov-report xml:cov.xml && \
		echo -e "\e[1;34mcleaning directory ...\e[0m" && \
		rm -r ./.pytest_cache/ 2> /dev/null && \
		rm ./.coverage 2> /dev/null
