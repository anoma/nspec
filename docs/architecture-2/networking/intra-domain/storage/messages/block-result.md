# BlockResponse

## Purpose

<!-- ANCHOR: purpose -->
Response to a block request.
<!-- ANCHOR_END: purpose -->

## Structure

| Field     | Type                            | Description         |
|-----------|---------------------------------|---------------------|
| `id`      | *[[BlockId#blockid]]*           | Block ID            |
| `content` | *Vec\<u8\>*                     | Block content       |
| `prefs`   | *[[StoragePrefs#storageprefs]]* | Storage preferences |
