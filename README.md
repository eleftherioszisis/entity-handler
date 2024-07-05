

### Clone an existing ModelBuildinConfig

```
entity-handler ModelBuildingConfig clone $REF_ID --name "foo" --description "bar"
```


## CellCompositionConfig

### base_cell_composition id

```
entity-handler CellCompositionConfig update base-cell-composition-id $CONFIG_ID --new-id $NEW_BASE_CELL_COMPOSITION_ID
```

### variantDefinition

```
entity-handler CellCompositionConfig update variant-definition $CONFIG_ID --version v2 --algorithm foo
```
