# -*- coding:utf-8 -*-

import datetime

import pytz
import screen
import xlwt
from django import http
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils import timezone
from django_six import Support_ValuesQuerySet, ValuesQuerySet


try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO


# Min (Max. Rows) for Widely Used Excel
# http://superuser.com/questions/366468/what-is-the-maximum-allowed-rows-in-a-microsoft-excel-xls-or-xlsx
EXCEL_MAXIMUM_ALLOWED_ROWS = 65536
# Column Width Limit For ``xlwt``
# https://github.com/python-excel/xlwt/blob/master/xlwt/Column.py#L22
EXCEL_MAXIMUM_ALLOWED_COLUMN_WIDTH = 65535


@property
def as_xls(self):
    book = xlwt.Workbook(encoding=self.encoding)
    sheet = book.add_sheet(self.sheet_name)

    styles = {
        'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
        'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
        'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
        'font': xlwt.easyxf('%s %s' % ('font:', self.font)),
        'default': xlwt.Style.default_style,
    }

    widths = {}
    for rowx, row in enumerate(self.data):
        for colx, value in enumerate(row):
            if value is None and self.blanks_for_none:
                value = ''

            if isinstance(value, datetime.datetime):
                if timezone.is_aware(value):
                    value = timezone.make_naive(value, pytz.timezone(settings.TIME_ZONE))
                cell_style = styles['datetime']
            elif isinstance(value, datetime.date):
                cell_style = styles['date']
            elif isinstance(value, datetime.time):
                cell_style = styles['time']
            elif self.font:
                cell_style = styles['font']
            else:
                cell_style = styles['default']

            sheet.write(rowx, colx, value, style=cell_style)

            # Columns have a property for setting the width.
            # The value is an integer specifying the size measured in 1/256
            # of the width of the character '0' as it appears in the sheet's default font.
            # xlwt creates columns with a default width of 2962, roughly equivalent to 11 characters wide.
            #
            # https://github.com/python-excel/xlwt/blob/master/xlwt/BIFFRecords.py#L1675
            # Offset  Size    Contents
            # 4       2       Width of the columns in 1/256 of the width of the zero character, using default font
            #                 (first FONT record in the file)
            #
            # Default Width: https://github.com/python-excel/xlwt/blob/master/xlwt/Column.py#L14
            # self.width = 0x0B92
            if self.auto_adjust_width:
                width = screen.calc_width(value) * 256 if isinstance(value, basestring) else screen.calc_width(str(value)) * 256
                if width > widths.get(colx, 0):
                    width = min(width, self.EXCEL_MAXIMUM_ALLOWED_COLUMN_WIDTH)
                    widths[colx] = width
                    sheet.col(colx).width = width

    book.save(self.output)


@property
def as_csv(self):
    for row in self.data:
        out_row = []
        for value in row:
            if value is None and self.blanks_for_none:
                value = ''
            if not isinstance(value, basestring):
                value = unicode(value)
            value = value.encode(self.encoding)
            out_row.append(value.replace('"', '""'))
        self.output.write('"%s"\n' % '","'.join(out_row))


def __init__(self, data, output_name='excel_data', format='%Y%m%d%H%M%S', headers=None, force_csv=False, encoding='utf8', font='', sheet_name='Sheet 1', blanks_for_none=True, auto_adjust_width=True):

    self.data = data
    self.output_name = output_name
    self.format = format
    self.headers = headers
    self.force_csv = force_csv
    self.encoding = encoding
    self.font = font
    self.sheet_name = sheet_name
    self.blanks_for_none = blanks_for_none
    self.auto_adjust_width = auto_adjust_width

    # Make sure we've got the right type of data to work with
    # ``list index out of range`` if data is ``[]``
    valid_data = False
    if Support_ValuesQuerySet and isinstance(self.data, ValuesQuerySet):
        self.data = list(self.data)
    elif isinstance(self.data, QuerySet):
        self.data = list(self.data.values())
    if hasattr(self.data, '__getitem__'):
        if isinstance(self.data[0], dict):
            if headers is None:
                headers = self.data[0].keys()
            self.data = [[row[col] for col in headers] for row in self.data]
            self.data.insert(0, headers)
        if hasattr(self.data[0], '__getitem__'):
            valid_data = True
    assert valid_data is True, 'ExcelResponse requires a sequence of sequences'

    self.output = StringIO()
    # Excel has a limit on number of rows; if we have more than that, make a csv
    use_xls = True if len(self.data) <= self.EXCEL_MAXIMUM_ALLOWED_ROWS and not self.force_csv else False
    _, content_type, file_ext = (self.as_xls, 'application/vnd.ms-excel', 'xls') if use_xls else (self.as_csv, 'text/csv', 'csv')
    self.output.seek(0)
    super(ExcelResponse, self).__init__(self.output, content_type=content_type)
    file_name_ext = '_{0}'.format(datetime.datetime.now().strftime(self.format)) if self.format else ''
    self['Content-Disposition'] = 'attachment;filename="%s.%s"' % ('{0}{1}'.format(self.output_name, file_name_ext).replace('"', '\"'), file_ext)


names = dir(http)


clsdict = {
    'EXCEL_MAXIMUM_ALLOWED_ROWS': EXCEL_MAXIMUM_ALLOWED_ROWS,
    'EXCEL_MAXIMUM_ALLOWED_COLUMN_WIDTH': EXCEL_MAXIMUM_ALLOWED_COLUMN_WIDTH,
    '__init__': __init__,
    'as_xls': as_xls,
    'as_csv': as_csv,
}


if 'FileResponse' in names:
    ExcelResponse = type('ExcelResponse', (http.FileResponse, ), clsdict)
elif 'StreamingHttpResponse' in names:
    ExcelResponse = type('StreamingHttpResponse', (http.StreamingHttpResponse, ), clsdict)
else:
    ExcelResponse = type('HttpResponse', (http.HttpResponse, ), clsdict)
