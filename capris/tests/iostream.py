from capris.tests import CaprisTest


class IOStreamTest(CaprisTest):
    def test_iostream(self):
        """
        Test that the file-like objects are being read
        from and written to when the runnable is being
        ran.
        """
        stream = self.grep('pattern').iostream
        self.helpers.stringio('pattern\n') > stream
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
            # cat always returns 0...
            self.helpers.assert_ok(response)

            # but the status code for grep is 1
            for item in response.history:
                assert item.status_code != 0

            # cat nothing == nothing
            assert response.std_out == ''
            context.append(response)

        stream = self.helpers.stringio('pattern\n') > \
            (self.grep('pattern') | self.cat).iostream & \
            callback
        response = stream.run(data='not even\n')

        assert context
