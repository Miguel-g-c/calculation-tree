.PHONY = test

test:
	PYTHONPATH=. poetry run pytest