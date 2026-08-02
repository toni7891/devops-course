.DEFAULT_GOAL := create

create:
	eksctl create cluster -f eks.yaml

delete:
	eksctl delete cluster -f eks.yaml

.PHONY: create delete
