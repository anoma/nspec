# BlockResponse


## Purpose


<!-- --8<-- [start:purpose] -->
Response to a block request.
<!-- --8<-- [end:purpose] -->

## Structure


| Field     | Type                            | Description         |
|-----------|---------------------------------|---------------------|
| `id`      | *[[BlockId#blockid]]*           | Block ID            |
| `content` | *Vec\<u8\>*                     | Block content       |
| `prefs`   | *[[StoragePrefs#storageprefs]]* | Storage preferences |
