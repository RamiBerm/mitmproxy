import codecs

import hyperframe


def http2_read_raw_frame(rfile):
    header = rfile.safe_read(9)
    length = int(codecs.encode(header[:3], 'hex_codec'), 16)

    if length == 4740180:
        raise ValueError("Length field looks more like HTTP/1.1: %s" % rfile.peek(20))

    body = rfile.safe_read(length)
    return [header, body]


def http2_read_frame(rfile):
    header, body = http2_read_raw_frame(rfile)
    frame, length = hyperframe.frame.Frame.parse_frame_header(header)
    frame.parse_body(memoryview(body))
    return frame
