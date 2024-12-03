def on_page_markdown(markdown: str, page, config, **kwargs):
    if page.file.src_path.endswith("changelog.md"):
        return (
            markdown.replace("[Node architecture](node)", "Node architecture")
            .replace(
                "[Repository maintenance and CI](.)", "Repository maintenance and CI"
            )
            .replace(
                "[System and node architecture](sys)", "System and node architecture"
            )
            .replace("[Juvix types and updates](types)", "Juvix types and updates")
            .replace("[Application documentation](apps)", "Application documentation")
            .replace(
                "[General specification changes](spec)", "General specification changes"
            )
            .replace(
                "[Tutorial and documentation](tutorial)", "Tutorial and documentation"
            )
            .replace("[Python-related changes](python)", "Python-related changes")
        )
