.PHONY: all build push deploy run

TAG:=dev-$(shell date +%s)

all: build run

build:
	docker build --pull -t quay.io/wisvch/userman2:${TAG} -t quay.io/wisvch/userman2:latest .

push:
	@docker push quay.io/wisvch/userman2:${TAG}

deploy:
	@kubectl set image deployment -n beheer userman2 userman2=quay.io/wisvch/userman2:${TAG}

run:
	@docker run --rm -it -p 127.0.0.1:8000:8001 -v $(CURDIR)/userman2/local.py:/config/local.py:ro --name userman2 quay.io/wisvch/userman2:latest gunicorn -b 0.0.0.0:8001
