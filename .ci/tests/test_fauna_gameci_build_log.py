"""Exercise the CI adapter's success/failure boundary without starting Unity."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ADAPTER = Path(__file__).resolve().parents[1] / 'fauna-gameci-build-log.sh'


class BuildLogAdapterTests(unittest.TestCase):
    def invoke(self, report, exit_code=0, apk=True):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root / 'build/Android/FaunaM2Sandbox.apk'
            if apk:
                output.parent.mkdir(parents=True)
                output.write_bytes(b'APK test fixture, not a game build')
            child = root / 'editor-fixture.sh'
            child.write_text('printf "CHILD_UMASK=%s\\n" "$(umask)"\nprintf "%s\\n" "$FAUNA_TEST_REPORT"\nexit "$FAUNA_TEST_EXIT"\n')
            env = {**os.environ, 'GITHUB_WORKSPACE': folder, 'BUILD_PATH': 'build/Android',
                   'BUILD_FILE': output.name, 'FAUNA_TEST_REPORT': report,
                   'FAUNA_TEST_EXIT': str(exit_code)}
            return subprocess.run(['bash', str(ADAPTER), 'bash', str(child)],
                                  env=env, text=True, capture_output=True, umask=0o022)

    def test_child_keeps_caller_permissions_for_host_readable_build_logs(self):
        result = self.invoke('License-only invocation')
        self.assertEqual(0, result.returncode)
        self.assertIn('CHILD_UMASK=0022', result.stdout)

    def test_success_requires_report_editor_zero_and_apk(self):
        result = self.invoke('QUEST_BUILD_RESULT Succeeded errors=0 warnings=14 size=123 path=build.apk')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('Build succeeded!', result.stdout)
        self.assertRegex(result.stdout, r'# Build results #\nErrors: 0\nSize: \d+ bytes')

    def test_editor_failure_is_not_hidden_by_a_success_report(self):
        result = self.invoke('QUEST_BUILD_RESULT Succeeded errors=0 warnings=0 size=123 path=build.apk', 137)
        self.assertEqual(137, result.returncode)
        self.assertNotIn('Build succeeded!', result.stdout)

    def test_failed_report_is_rejected_even_if_editor_exits_zero(self):
        result = self.invoke('QUEST_BUILD_RESULT Failed errors=0 warnings=0 size=123 path=build.apk')
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn('Build succeeded!', result.stdout)

    def test_nonzero_build_errors_are_rejected(self):
        result = self.invoke('QUEST_BUILD_RESULT Succeeded errors=1 warnings=0 size=123 path=build.apk')
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn('Build succeeded!', result.stdout)

    def test_missing_apk_is_rejected(self):
        result = self.invoke('QUEST_BUILD_RESULT Succeeded errors=0 warnings=0 size=123 path=build.apk', apk=False)
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn('Build succeeded!', result.stdout)

    def test_license_only_invocation_does_not_fabricate_a_build(self):
        result = self.invoke('Successfully returned the entitlement license')
        self.assertEqual(0, result.returncode)
        self.assertNotIn('Build succeeded!', result.stdout)


if __name__ == '__main__':
    unittest.main()
