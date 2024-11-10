import requests


def get_public_repos(org_name):
    repos_url = f"https://api.github.com/orgs/{org_name}/repos?type=public"
    response = requests.get(repos_url)
    response.raise_for_status()
    return response.json()


def repo_to_bibtex(repo):
    return f"""@misc{{github-{repo['name']},
  author = {{{repo['owner']['login']}}},
  title = {{{repo['name']}}},
  year = {{{repo['created_at'][:4]}}},
  publisher = {{GitHub}},
  journal = {{GitHub repository}},
  url = {{https://github.com/{repo['full_name']}}}
}}"""


def write_bibtex_file(repos, fname_prefix=""):
    with open(fname_prefix + "-repos.bib", "w") as bibtex_file:
        for repo in repos:
            bibtex_entry = repo_to_bibtex(repo)
            bibtex_file.write(bibtex_entry + "\n\n")  # Add extra newline for separation


def main():
    org_names = ["anoma"]
    for org_name in org_names:
        repos = get_public_repos(org_name)
        write_bibtex_file(repos, org_name)


if __name__ == "__main__":
    main()
