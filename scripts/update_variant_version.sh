
set -e

entity-handler \
	variant \
	clone https://bbp.epfl.ch/data/bbp/mmb-point-neuron-framework-model/488e70c6-7163-414b-9e91-cae58bad9545 \
	-e env_type:MODULE \
	-e modulepath:/gpfs/bbp.cscs.ch/ssd/apps/bsd/pulls/2315/config/modules/_meta \
	-e modules:unstable,py-cwl-registry,py-bba-data-push \
	--version v1-tst

entity-handler \
	model-building-config https://bbp.epfl.ch/data/bbp/mmb-point-neuron-framework-model/db0dcc6c-3bef-4760-88d9-4ef1b2642da4 \
	update
	variant-version \
	-c cellCompositionConfig \
	-v v1-tst

