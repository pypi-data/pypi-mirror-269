from io import BytesIO
from typing import List, Dict
from urllib.parse import quote

import numpy as np
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from styleframe import StyleFrame


def export_exl(header: List[str], data, file_name='download.xlsx') -> StreamingResponse:
    output = BytesIO()
    df = pd.DataFrame(columns=header)
    for item in data:
        df.loc[len(df.index)] = item

    excel_writer = StyleFrame.ExcelWriter(output)

    sf = StyleFrame(df)
    best_fit, columns_and_rows_to_freeze = header, 'A2'
    if df.shape[0] == 0:
        best_fit, columns_and_rows_to_freeze = None, 'A1'
    sf.to_excel(
        excel_writer=excel_writer,
        best_fit=best_fit,
        columns_and_rows_to_freeze=columns_and_rows_to_freeze,
        row_to_add_filters=0,
    )
    excel_writer.close()
    output.seek(0)
    headers = {"content-type": "application/vnd.ms-excel",
               "content-disposition": 'attachment;filename={}'.format(quote(file_name))}
    return StreamingResponse(output, media_type='xls/xlsx', headers=headers)


def export_csv(data: List, file_name='download.csv') -> StreamingResponse:
    output = BytesIO()
    df = pd.DataFrame(data)
    df.to_csv(output, index=False, encoding='utf-8_sig')
    output.seek(0)
    headers = {"content-type": "application/vnd.ms-excel",
               "content-disposition": 'attachment;filename={}'.format(quote(file_name))}
    return StreamingResponse(output, media_type='text/csv', headers=headers)


class ExcelTools:
    def __init__(self, columns_map=None, order=None):
        """
        :param columns_map: 列名映射 => {"name":"姓名"，"score":"成绩","sex":"性别"}
        :param order: 列排序列表 => ["name","sex","score"]
        """
        self.columns_map = columns_map
        self.order = order

    async def excel_to_df(self, excel: UploadFile, skip_rows=0) -> pd.DataFrame:
        contents = await excel.read()
        buffer = BytesIO(contents)
        df = pd.read_excel(buffer, skiprows=skip_rows)

        df.replace(np.nan, '', inplace=True)

        # 去除所有列数据中的空格
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # 列名映射
        if self.columns_map:
            columns_map = dict(zip(self.columns_map.values(), self.columns_map.keys()))
            df.rename(columns=columns_map, inplace=True)

        return df

    async def excel_to_dict(self, excel: UploadFile, skip_rows=0):
        """
        Excel转Python dict
        :param excel:
        :param skip_rows:
        :return:
        """
        if excel:
            df = await self.excel_to_df(excel, skip_rows=skip_rows)
            return df.to_dict(orient='records')
        return []

    def dict_to_excel(self, datas: List[Dict]):
        """
        :param datas: 数据集 => [{"name":"张三","score":90，"sex":"男"}]
        :return:
        """
        output = BytesIO()
        pf = pd.DataFrame(datas)
        if self.order:
            pf = pf[self.order]
        if self.columns_map:
            pf.rename(columns=self.columns_map, inplace=True)

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pf.fillna(' ', inplace=True)
            pf.to_excel(writer, sheet_name='sheet1', index=False)
            worksheet = writer.sheets['sheet1']

            for i, col in enumerate(pf.columns):
                column_len = pf[col].astype(str).str.len().max()
                column_len = max(column_len, len(col)) + 2
                worksheet.set_column(i, i, column_len)

        output.seek(0)
        return output
