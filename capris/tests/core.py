from capris.tests import CaprisTest
from capris.core import run, run_command

class CoreTest(CaprisTest):
    def test_run_command(self):
        """
        Sanity test for the attributes of a response
        object- they should be set to expected values.
        """
        response = run_command(['echo', 'pattern'])

        assert response.ok()
        assert response.std_out == 'pattern\n'
        assert not response.history

    def test_status_codes(self):
        """
        Check that response.ok accepts positional
        arguments of allowed status codes.
        """
        response = run_command(['grep'])

        assert response.status_code == 2
        assert response.ok(2)

    def test_pipeline(self):
        """
        Test that the pipeline is working properly
        and that commands executed before would not
        have ``std_out`` attributes set.
        """
        response = run([['echo', 'pattern'], ['cat']])

        assert response.ok()
        assert response.std_out == 'pattern\n'

        echo_res = response.history[0]
        assert echo_res.ok()
        assert not echo_res.std_out
