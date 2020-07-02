import os
import shutil
import tempfile
import unittest

from mup.path.temp_path import handle_remove_readonly
from mup.proc import CommandRunner
from mup.repo import git


class TestGit(unittest.TestCase):
    temp_dir = None
    repo_dir = None
    commit_id_long = None
    commit_id_short = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()

        cls.repo_dir = os.path.join(cls.temp_dir, "repository")
        os.makedirs(cls.repo_dir)

        # init the repository
        cmd = CommandRunner(cwd=cls.repo_dir)
        cmd.run(("git", "init"), silent=True)

        # create and check-in a file
        with open(os.path.join(cls.repo_dir, "README.md"), "w") as fp:
            fp.write("# Test Repository\n")
        cmd.run(("git", "add", "README.md"), silent=True)
        result = cmd.run(("git", "commit", "-m", "initial commit"), silent=True)
        if result.result != 0:
            raise RuntimeError(f"commit failed ({result.result}): {result.stderr}")

        cls.commit_id_long = git.commit_id(cls.repo_dir)
        cls.commit_id_short = git.commit_id(cls.repo_dir, short=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir, onerror=handle_remove_readonly)

    def test_git(self):
        self.assertIsNotNone(shutil.which("git"), msg="Git is required.")

    def test_git_clone(self):
        clone_path = os.path.join(self.temp_dir, "clone")
        os.makedirs(clone_path)
        repository = git.clone(self.repo_dir, destination=clone_path)
        self.assertTrue(os.path.isfile(os.path.join(repository, "README.md")))

    def test_git_clone_bad_source(self):
        clone_bad_source = os.path.join(self.temp_dir, "clone_bad_source")
        os.makedirs(clone_bad_source)
        fake_repo_path = os.path.join(self.temp_dir, "fake-repo")
        with self.assertRaises(RuntimeError):
            git.clone(fake_repo_path, destination=clone_bad_source)

    def test_git_commit_id(self):
        clone_path = os.path.join(self.temp_dir, "commit_ids")
        os.makedirs(clone_path)
        repository = git.clone(self.repo_dir, destination=clone_path)

        repo_commit_id_long = git.commit_id(repository)
        repo_commit_id_short = git.commit_id(repository, short=True)

        self.assertIsNotNone(self.commit_id_long)
        self.assertIsNotNone(self.commit_id_short)

        self.assertEqual(self.commit_id_long, repo_commit_id_long)
        self.assertEqual(self.commit_id_short, repo_commit_id_short)

    def test_git_commit_id_no_repository(self):
        commit_id_no_repository = os.path.join(self.temp_dir, "commit_id_no_repository")
        os.makedirs(commit_id_no_repository)
        with self.assertRaises(RuntimeError):
            git.commit_id(commit_id_no_repository)

    def test_is_repository(self):
        not_a_repository = os.path.join(self.temp_dir, "not_a_repository")
        os.makedirs(not_a_repository)
        not_a_path = os.path.join(self.temp_dir, "not_a_path")

        self.assertTrue(git.is_path_repository(self.repo_dir))
        self.assertFalse(git.is_path_repository(not_a_repository))
        with self.assertRaises(FileNotFoundError):
            git.is_path_repository(not_a_path)
