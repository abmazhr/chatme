.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

prepare-env-locally: ## Install the service's dependencies
	@echo -e "\e[1;34mInstalling dependencies ...\e[0m" && \
		yarn install


run-tests-native-locally: prepare-env-locally ## Running the service's tests natively locally
	@echo -e "\e[1;34mRunning tests native locally ...\e[0m" && \
		yarn run test

run-server-native-locally: prepare-env-locally ## Running the service's server natively locally
	@echo -e "\e[1;34mRunning server native locally ...\e[0m" && \
		echo -e "\e[1;33mTo exit press CTRL+C ...\e[0m" && \
		yarn run start

run-server-on-docker-locally: ## Running the service's server on docker locally
	@echo -e "\e[1;34mRunning server on docker locally ...\e[0m" && \
		echo -e "\e[1;33mTo exit press CTRL+C ...\e[0m" && \
		docker-compose up --build -d --scale web-socket-server=5 nginx