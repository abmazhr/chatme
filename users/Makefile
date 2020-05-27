.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

prepare-env-locally: ## Install the service's dependencies
	@echo -e "\e[1;34mmaking new virtual environment and installing dependencies ...\e[0m" && \
		pipenv install


run-tests-native-locally: prepare-env-locally ## Running the service's tests natively locally
	@echo -e "\e[1;34mrunning tests native locally ...\e[0m" && \
		pipenv run py.test \
			-r s \
			-vvs \
			--cov . test \
			--cov-report term-missing \
			--cov-report html:cov_html \
			--cov-report xml:cov.xml \
			--cov-config .coveragerc && \
		echo -e "\e[1;34mcleaning directory ...\e[0m" && \
		rm -r ./.pytest_cache/ 2> /dev/null && \
		rm ./.coverage 2> /dev/null

run-server-native-locally: prepare-env-locally ## Running the service's server natively locally
	@echo -e "\e[1;34mrunning server native locally ...\e[0m" && \
		echo -e "\e[1;33mTo exit press CTRL+C ...\e[0m" && \
		pipenv run python src/main.py

run-server-on-docker-locally: ## Running the service's server on docker locally
	@echo -e "\e[1;34mrunning server on docker locally ...\e[0m" && \
		echo -e "\e[1;33mTo exit press CTRL+C ...\e[0m" && \
		docker-compose up --build