UV ?= uv
NAME ?=

.PHONY: sync validate test new-skill package

sync:
	$(UV) sync

validate:
	$(UV) run validate

test:
	$(UV) run pytest

new-skill:
	test -n "$(NAME)"
	$(UV) run new-skill $(NAME)

package:
	test -n "$(NAME)"
	$(UV) run package-skill $(NAME)

