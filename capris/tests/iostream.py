from capris.tests import CaprisTest


class IOStreamTest(CaprisTest):
    def test_iostream(self):
        """
        Test that the file-like objects are being read
        from and written to when the runnable is being
        ran.
        """
        stream = self.helpers.stringio('pattern\n') > self.grep('pattern').iostream
        stream > self.helpers.stringio()

        response = stream.run()

        self.helpers.assert_ok(response)
        assert stream.output_file.getvalue() == response.std_out == 'pattern\n'

    def test_callbacks_and_data(self):
        """
        Callbacks should be executed and available
        at the ``callbacks`` property of ``IOStream``
        objects. Also, the ``IOStream`` object shouldn't
        read from the file object if there is data
        available.
        """
        context = []
        def callback(response):
            context.append(response)
            assert response.status_code != 0
            assert response.std_out != 'pattern\n'

        stream = self.helpers.stringio('pattern\n') > self.grep('pattern').iostream & callback
        response = stream.run(data='not even\n')

        assert context
