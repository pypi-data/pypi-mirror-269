import os
import shutil
from pathlib import Path

from docutils.parsers.rst import directives
from git import Repo
from sphinx.directives.code import CodeBlock
from sphinx.util.docutils import SphinxDirective


def fetch_file_from_repo(repo_addr, file_path, branch="master"):
    tmp_path = "tmp"
    has_error = False
    repo_addr = os.path.expandvars(repo_addr)
    try:
        repo = Repo.clone_from(
            repo_addr,
            to_path=tmp_path,
            depth=1,
            no_checkout=True,
            single_branch=True,
            branch=branch,
        )
    except Exception as e:
        print(f"Error cloning repo {repo_addr}: {e}")
        has_error = True
    try:
        filecontent = repo.git.show(f"{branch}:{file_path}")
    except Exception as e:
        print(f"Error fetching file {branch}:{file_path} from repo {repo_addr}: {e}")
        has_error = True
    finally:
        repo.close()
        shutil.rmtree(tmp_path)
    if has_error:
        raise RuntimeError(
            "Something went wrong while fetching files from remote git repo!!"
        )
    return filecontent


class ExternalLiteralFileDirective(SphinxDirective):
    # this enables content in the directive
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "type": lambda t: directives.choice(t, ("path", "url", "git")),
        "git-branch": directives.unchanged_required,
        "git-url": directives.unchanged_required,
    }

    def run(self):
        patharg = self.arguments[0]
        pathtype = "path"
        if "type" in self.options:
            pathtype = self.options["type"]

        if pathtype == "path":
            this_path = Path(self.env.docname)
            path = this_path.parent / patharg
            with open(path, "r") as f:
                filecontent = f.read()
        elif pathtype == "url":
            import requests

            url = patharg
            r = requests.get(url)
            filecontent = r.text
        elif pathtype == "git":
            repo_addr = self.options["git-url"]
            branch = self.options["git-branch"]
            filecontent = fetch_file_from_repo(repo_addr, patharg, branch=branch)
        else:
            raise ValueError(f"Unknown path type {pathtype}")

        codeblock_directive = CodeBlock(
            name="",
            arguments=[],
            content=filecontent.split("\n"),
            lineno=self.lineno,
            content_offset=0,
            block_text="",
            state=self.state,
            state_machine=self.state_machine,
        )
        return codeblock_directive.run()
