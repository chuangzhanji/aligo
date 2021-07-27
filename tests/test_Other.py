"""..."""

from aligo import *

test_file = '60f927edf4c9f64d3a0c4704b80154cfa3d13c2a'


def test_get_download_url():
    ali = Core()

    file = ali.get_download_url(GetDownloadUrlRequest(file_id=test_file))
    assert isinstance(file, GetDownloadUrlResponse)
    assert file.size == 129465082
    