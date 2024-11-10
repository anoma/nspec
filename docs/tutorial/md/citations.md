---
icon: simple/latex
search:
  exclude: false
tags:
  - references
  - bibtex
todos: False
---

# Bibliography

Place your `.bib` files within the `refs` directory. For convenience,
we have included all the ART published papers in the `refs/art.bib`
file.

Any new `.bib`
file added to this folder will automatically be processed.

## Citing in Markdown

Use the citation key from your `.bib` files to cite references in your markdown
files. The syntax is as follows:

```text
This statement requires a citation [@citation_key].
```

!!! info

    We have `refs/update_repo_bibtexs.py` script that can be used to
    update the `refs/anoma_repos.bib` file to cite Anoma repositories
    in the documentation.

## References available


??? quote "Anoma Research Topics (ART) papers"

    ```bibtex
    --8<-- "refs/art.bib"
    ```

??? quote "Anoma Public GitHub repositories"

    ```bibtex
    --8<-- "refs/anoma_repos.bib"
    ```

??? quote "Other literature"

    ```bibtex
    --8<-- "refs/ref.bib"
    ```
