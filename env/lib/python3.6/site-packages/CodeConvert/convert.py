# -*- coding: utf-8 -*-

import six


# Note:
#   See http://docs.python.org/2/library/codecs.html#standard-encodings


TIPS_UTF8 = {
    'u_contain_utf8': u">>> u 内含 utf8 编码: obj.encode('raw_unicode_escape')",
    'u_contain_gbk': u">>> u 内含 gbk 编码: obj.encode('raw_unicode_escape').decode('gbk').encode('utf8')",
    'unicode': u">>> unicode 编码: obj.encode('utf8')",
    'utf8': u">>> utf8 编码: obj",
    'gbk': u">>> gbk 编码: obj.decode('gbk').encode('utf8')",
    'unicode_without_u': u">>> 无 u 的 unicode 编码: obj.decode('raw_unicode_escape').encode('utf8')",
}


TIPS_UNICODE = {
    'u_contain_utf8': u">>> u 内含 utf8 编码: obj.decode('utf8')",
    'u_contain_gbk': u">>> u 内含 gbk 编码: obj.encode('raw_unicode_escape').decode('gbk') or obj.encode('latin1').decode('gbk')",
    'unicode': u">>> unicode 编码: obj",
    'utf8': u">>> utf8 编码: obj.decode('utf8')",
    'gbk': u">>> gbk 编码: obj.decode('gbk')",
    'unicode_without_u': u">>> 无 u 的 unicode 编码: obj.decode('raw_unicode_escape')",
}


TIPS_ESCAPE = {
    'double_backslash_str': u">>> 双反斜杠字符: obj.decode('string_escape')",
    'double_backslash_unicode': u">>> 双反斜杠 Unicode 字符: obj.decode('raw_unicode_escape')",
    'emoji': u">>> Emoji 字符: obj.decode('raw_unicode_escape')",
}


def print_tip_utf8(k, debug=False):
    six.print_(TIPS_UTF8[k] if debug else '')


def print_tip_unicode(k, debug=False):
    six.print_(TIPS_UNICODE[k] if debug else '')


def print_tip_escape(k, debug=False):
    six.print_(TIPS_ESCAPE[k] if debug else '')


def exec_strip(repr_kw):
    repr_kw = repr_kw.strip('\'').strip('"')
    try:
        return repr_kw[repr_kw.index('\\'):]
    except ValueError:
        return repr_kw


def convert_2_utf8_basestring(kw, debug=False):
    repr_kw = repr(kw)
    if repr_kw.startswith('u'):
        striped_kw = exec_strip(repr_kw[1:])
        if striped_kw.startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
            try:  # 处理 u 内含 utf8 编码
                kw.encode('raw_unicode_escape').decode('utf8')  # 如果是 u 内含 gbk 编码，会出错进入 except
                ret = kw.encode('raw_unicode_escape')
                print_tip_utf8('u_contain_utf8', debug)
            except (UnicodeEncodeError, UnicodeDecodeError):  # 处理 u 内含 gbk 编码
                try:
                    ret = kw.encode('raw_unicode_escape').decode('gbk').encode('utf8')
                    print_tip_utf8('u_contain_gbk', debug)
                except (UnicodeEncodeError, UnicodeDecodeError):  # 处理 unicode 编码
                    ret = kw.encode('utf8')
                    print_tip_utf8('unicode', debug)
        elif isinstance(kw, six.text_type):  # 处理 unicode 编码
            ret = kw.encode('utf8')
            print_tip_utf8('unicode', debug)
        else:
            ret = kw
    else:
        striped_kw = exec_strip(repr_kw)
        if striped_kw.startswith('\\x'):  # 处理 gbk、utf8 编码
            try:  # 处理 utf8 编码
                kw.decode('utf8')
                ret = kw
                print_tip_utf8('utf8', debug)
            except UnicodeDecodeError:  # 处理 gbk 编码
                try:
                    ret = kw.decode('gbk').encode('utf8')
                    print_tip_utf8('gbk', debug)
                except UnicodeDecodeError:  # 处理无 u 的 unicode 编码
                    ret = kw.decode('raw_unicode_escape').encode('utf8')
                    print_tip_utf8('unicode_without_u', debug)
        elif striped_kw.startswith('\\\\u'):  # 处理无 u 的 unicode 编码
            ret = kw.decode('raw_unicode_escape').encode('utf8')
            print_tip_utf8('unicode_without_u', debug)
        else:
            ret = kw
            print_tip_utf8('utf8', debug)
    return ret


def convert_2_unicode_basestring(kw, debug=False):
    repr_kw = repr(kw)
    if repr(kw).startswith('u'):
        striped_kw = exec_strip(repr_kw[1:])
        if striped_kw.startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
            try:  # 处理 u 内含 utf8 编码
                kw.encode('latin1').decode('utf8')
                ret = kw.encode('latin1').decode('utf8')
                print_tip_unicode('u_contain_utf8', debug)
            except (UnicodeEncodeError, UnicodeDecodeError):  # 处理 u 内含 gbk 编码
                try:
                    ret = kw.encode('latin1').decode('gbk')
                    print_tip_unicode('u_contain_gbk', debug)
                except (UnicodeEncodeError, UnicodeDecodeError):  # 处理 unicode 编码
                    ret = kw
                    print_tip_unicode('unicode', debug)
        elif isinstance(kw, six.text_type):  # 处理 unicode 编码
            ret = kw
            print_tip_unicode('unicode', debug)
        else:
            ret = kw
    else:
        striped_kw = exec_strip(repr_kw)
        if striped_kw.startswith('\\x'):  # 处理 gbk、utf8 编码
            try:  # 处理 utf8 编码
                ret = kw.decode('utf8')
                print_tip_unicode('utf8', debug)
            except UnicodeDecodeError:  # 处理 gbk 编码
                try:
                    ret = kw.decode('gbk')
                    print_tip_unicode('gbk', debug)
                except UnicodeDecodeError:  # 处理无 u 的 unicode 编码
                    ret = kw.decode('raw_unicode_escape')
                    print_tip_unicode('unicode_without_u', debug)
        elif striped_kw.startswith('\\\\u'):  # 处理无 u 的 unicode 编码
            ret = kw.decode('raw_unicode_escape')
            print_tip_unicode('unicode_without_u', debug)
        else:
            if six.PY2:
                ret = kw.decode('utf8')
                print_tip_unicode('utf8', debug)
            else:
                ret = kw
    return ret


def kw_escape(kw, debug=False):
    ret, repr_kw = kw, repr(kw)
    if repr_kw.startswith('u'):
        striped_kw = exec_strip(repr_kw[1:])
        if striped_kw.startswith('\\\\x'):
            ret = kw.decode('string_escape')
            print_tip_escape('double_backslash_str', debug)
        elif striped_kw.startswith('\\\\u'):
            ret = kw.decode('raw_unicode_escape')
            print_tip_escape('double_backslash_unicode', debug)
        elif striped_kw.startswith('\\\\U'):
            ret = kw.decode('raw_unicode_escape')
            print_tip_escape('emoji', debug)
    else:
        striped_kw = exec_strip(repr_kw)
        if striped_kw.startswith('\\\\x'):
            ret = kw.decode('string_escape')
            print_tip_escape('double_backslash_str', debug)
        elif striped_kw.startswith('\\\\U'):
            ret = kw.decode('raw_unicode_escape')
            print_tip_escape('emoji', debug)
    return ret


def convert_2_utf8(kw):
    if isinstance(kw, six.string_types):
        return convert_2_utf8_basestring(kw_escape(kw))
    elif isinstance(kw, dict):
        return dict((convert_2_utf8(k), convert_2_utf8(v)) for k, v in six.iteritems(kw))
    elif isinstance(kw, list):
        return [convert_2_utf8(k) for k in kw]
    elif isinstance(kw, tuple):
        return tuple([convert_2_utf8(k) for k in kw])
    elif isinstance(kw, set):
        return set([convert_2_utf8(k) for k in kw])
    return kw


def convert_2_unicode(kw):
    if isinstance(kw, six.string_types):
        return convert_2_unicode_basestring(kw_escape(kw))
    elif isinstance(kw, dict):
        return dict((convert_2_unicode(k), convert_2_unicode(v)) for k, v in six.iteritems(kw))
    elif isinstance(kw, list):
        return [convert_2_unicode(k) for k in kw]
    elif isinstance(kw, tuple):
        return tuple([convert_2_unicode(k) for k in kw])
    elif isinstance(kw, set):
        return set([convert_2_unicode(k) for k in kw])
    return kw


class CodeConvert:
    def Convert2Utf8(self, kw):
        return convert_2_utf8(kw)

    def Convert2Unicode(self, kw):
        return convert_2_unicode(kw)

    def Convert2Utf8_test(self, kw):
        return convert_2_utf8_basestring(kw_escape(kw, True), True)

    def Convert2Unicode_test(self, kw):
        return convert_2_unicode_basestring(kw_escape(kw, True), True)


CodeConvert = CodeConvert()
