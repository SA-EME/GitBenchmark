from rich import print

from controllers.merge import merge
from utils.git import get_current_branch, main_branch


def merge_arguments(args):

    merged_branch = get_current_branch()

    if merged_branch == main_branch():
        print("[red]You can't merge on the main branch[/red]")
        return
    merge(merged_branch)
