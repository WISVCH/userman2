.PHONY: all build push deploy run

TAG:=dev-$(shell date +%s)

all: build run

build:
	docker build --pull -t userman2 .

run:
	@docker run --rm -it -p 127.0.0.1:8000:8001 -v $(CURDIR)/userman2/local.py:/config/local.py:ro --name userman2 userman2 gunicorn -b 0.0.0.0:8001
