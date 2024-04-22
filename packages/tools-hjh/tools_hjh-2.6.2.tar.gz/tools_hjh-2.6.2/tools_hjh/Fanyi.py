# coding:utf-8
import json
from tools_hjh.HTTPTools import HTTPTools
from tools_hjh import Tools
from tools_hjh.DBConn import DBConn
from tools_hjh.ThreadPool import ThreadPool

headers = {
    'content-type': 'application/json',
    'cookie':'_pk_id.1.88f4=e133b997b9baa0a0.1699604120.; _pk_ref.1.88f4=%5B%22%22%2C%22%22%2C1705329658%2C%22https%3A%2F%2Facg1.xyz%2F%22%5D; b2_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmgteHkubmV0IiwiaWF0IjoxNzA1ODE0NzQ3LCJuYmYiOjE3MDU4MTQ3NDcsImV4cCI6MTcwNzcxNTU0NywiZGF0YSI6eyJ1c2VyIjp7ImlkIjoiMzAyMiJ9fX0.UX60IEj7dLZZmGUFdqL5A-J1DfOgFEiqHiiwCRK7dKs; cf_clearance=rwsFkkA7UMCeLWtw1e2CDky77adK7RvN4E5t5SYFTJQ-1705861563-1-AfyTd9qCAJdI1zqAkvgIWkarB52DdHDcB5GqtEIMbmSeJUe4GD4tGGpcLNuFAaK5FYZ9ElYhUaDA/EtGdDXPuHA=; b2_back_url=https://fh-xy.net/gold',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie':'INGRESSCOOKIE=b5246e97ef5e96bc5abc4247193db243|a6d4ac311669391fc997a6a267dc91c0; userCountry=CN; releaseGroups=3613.WDW-267.2.2_7616.DWFA-777.2.2_8681.AAEXP-7202.2.1_8392.DWFA-813.2.1_8688.AAEXP-7209.1.1_8691.AAEXP-7212.1.1_2345.DM-1001.2.2_6732.DF-3818.2.4_7584.TACO-60.2.1_8041.DM-1581.2.2_8666.AAEXP-7187.1.1_4321.B2B-679.2.2_4854.DM-1255.2.5_6403.TC-996.2.5_6728.TC-1115.2.2_976.DM-667.2.3_3961.B2B-663.2.3_5562.DWFA-732.2.2_7794.B2B-950.2.4_8783.DF-3926.1.1_2274.DM-952.2.2_7617.DWFA-774.1.1_8684.AAEXP-7205.2.1_8689.AAEXP-7210.1.1_8674.AAEXP-7195.1.1_8692.AAEXP-7213.1.1_975.DM-609.2.3_4650.AP-312.2.8_6738.B2B-646.2.1_6739.B2B-606.2.1_4853.DF-3503.1.1_6727.B2B-777.2.2_8253.DWFA-625.1.1_8287.TC-1035.1.2_220.DF-1925.1.9_1571.DM-791.2.4_1997.DM-941.2.3_3283.DWFA-661.2.2_8669.AAEXP-7190.1.1_8675.AAEXP-7196.1.1_8677.AAEXP-7198.1.1_8694.AAEXP-7215.1.1_5707.TACO-104.2.2_6359.DM-1411.2.10_8671.AAEXP-7192.1.1_8682.AAEXP-7203.1.1_2962.DF-3552.2.6_3939.B2B-596.1.1_4121.WDW-356.2.5_5560.DWFA-638.2.2_863.DM-601.2.2_8673.AAEXP-7194.2.1_8690.AAEXP-7211.1.1_8676.AAEXP-7197.1.1_8683.AAEXP-7204.1.1_8685.AAEXP-7206.1.1_8687.AAEXP-7208.1.1_1583.DM-807.2.5_2455.DPAY-2828.2.2_3587.DWFA-653.2.2_8672.AAEXP-7193.1.1_6402.DWFA-716.2.3_7105.TACO-100.2.3_7106.DWFA-790.2.2_7759.DWFA-814.2.2_1119.B2B-251.2.4_1483.DM-821.2.2_2055.DM-814.2.3_4478.SI-606.2.3_1585.DM-900.2.3_2413.DWFA-524.2.4_5376.WDW-360.1.2_8670.AAEXP-7191.1.1_8686.AAEXP-7207.1.1_1577.DM-594.2.3_3586.DF-3635.2.6_3588.TC-864.1.5_4322.DWFA-689.2.2_1780.DM-872.2.2_2373.DM-1113.2.4_2464.DM-1175.2.2_8564.SEO-656.1.1_7758.B2B-949.2.3_8680.AAEXP-7201.1.1_8693.AAEXP-7214.1.1_8695.AAEXP-7216.1.1_866.DM-592.2.2_3127.DM-1032.2.2_4831.WDW-341.2.2_5870.WDW-400.2.2_8667.AAEXP-7188.1.1_8668.AAEXP-7189.2.1_8678.AAEXP-7199.1.1_8679.AAEXP-7200.1.1_2656.DM-1177.2.2_4473.DWFA-667.2.3_5719.DWFA-761.2.2_5914.DWFA-683.2.2; dapUid=53a82fca-d654-4595-a7c2-8cc93d67d8b8; dapVn=1; LMTBID=v2|49584e91-262a-4037-a163-ecda6491e8da|24747890dcd5aae009c3a7435a58a9c1; privacySettings={"v":"1","t":1713744000,"m":"LAX","consent":["NECESSARY","PERFORMANCE","COMFORT","MARKETING"]}; dapSid={"sid":"ef096606-057f-43ab-9d64-0c3f455faf8e","lastUpdate":1713752747}',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.deepl.com',
    'referer': 'https://www.deepl.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def main():
    db = DBConn('sqlite', db='fy.db', poolsize=32)
    m_page = '''
        create table if not exists m_page(
            src text,
            dst text
        )
    '''
    # db.run('drop table m_page')
    db.run(m_page)
    db.run('CREATE INDEX if not exists idx_m_page_src on m_page(src);')
    insert_sql = 'insert into m_page(src) select ? where not exists(select 1 from m_page m where m.src = ?)'
    src_text = Tools.cat('D:/ManualTransFile.json')
    src_json = json.loads(src_text)
    
    params = []
    for key, _ in src_json.items():
        param = (key, key)
        params.append(param)
    rs = db.run(insert_sql, param=params, wait=True)
    print('词条总数：' + str(rs))
    
    def update_one(row):
        try:
            update_sql = 'update m_page set dst = ? where src = ?'
            key = row[0]
            new_value = fy(key, source_lang_computed='JP', target_lang='ZH')
            db.run(update_sql, param=(new_value, key), wait=True)
            print('"' + key + '" : "' + new_value + '"')
        except Exception as _:
            print(key, str(_))
        
    select_sql = 'select src from m_page where dst is null'
    rows = db.run(select_sql).get_rows()
    tp = ThreadPool(32)
    for row in rows:
        tp.run(update_one, (row,))
    tp.wait()
    
    db.close()


def fy(text, source_lang_computed, target_lang):
    url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'
    params = {"jsonrpc":"2.0", "method": "LMT_handle_jobs", "params":{"jobs":[{"kind":"default", "sentences":[{"text":text, "id":1, "prefix":""}], "raw_en_context_before":[], "raw_en_context_after":[], "preferred_num_beams":4, "quality":"fast"}], "lang":{"target_lang":target_lang, "preference":{"weight":{}, "default":"default"}, "source_lang_computed":source_lang_computed}, "priority":-1, "commonJobParams":{"mode":"translate", "textType":"plaintext", "browserType":1}, "timestamp":1713752749442}, "id":41010004}
    mess = HTTPTools.get(url, headers, data=json.dumps(params))
    mess_json = json.loads(mess)
    rs = mess_json['result']['translations'][0]['beams'][0]['sentences'][0]['text']
    # rs = mess_json['result']['translations'][0]['beams'][1]['sentences'][0]['text']
    return rs

    
if __name__ == '__main__':
    main()

