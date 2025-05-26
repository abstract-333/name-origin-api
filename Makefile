DC = docker compose
EXEC = docker exec -t
LOGS = docker logs
ENV = --env-file .env
ENV_PROD = --env-file .env.prod
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = main-app
PROD_CONTAINER = main-app-prod
PROD=--profile prod
DEV=--profile dev

.PHONY: all
all:
	${DC} ${DEV} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d


.PHONY: all-prod
all-prod:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV_PROD} ${PROD} up --build -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} ${DEV} up --build -d

.PHONY: app-prod
app-prod:
	${DC} -f ${APP_FILE} ${ENV_PROD} ${PROD} up --build -d


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${DEV} down


.PHONY: app-prod-down
app-prod-down:
	${DC} -f ${APP_FILE} ${PROD} down


.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down


.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${DEV} down


.PHONY: all-prod-down
all-prod-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${PROD} down


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: migrations-prod
migrations-prod:
	${EXEC} ${PROD_CONTAINER} alembic upgrade head