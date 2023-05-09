import cjen


@cjen.operate.xlsx.reader(fpath="test_data.xlsx", cols=["id", "name", "description", "active", "company_id",
                                                        "sponsor_id", "status",	"modify_uid",
                                                        "creator_dt", "modify_dt", "creator_uid",
                                                        "is_delete", "subject_management"])
def test_xlsx_reader_with_col(xlsx_data: list = None):
    assert xlsx_data[2].get("id") == 1200
    assert xlsx_data[2].get("name") == "eclinical_edc_dev_84"
    assert xlsx_data[2].get("description") == None
    assert xlsx_data[2].get("modify_dt") == "2023-04-24 11:08:01"

@cjen.operate.xlsx.reader(fpath="test_data.xlsx", cols=[0,1])
def test_xlsx_reader_with_all(xlsx_data: list = None):
    assert xlsx_data[0][0] == "id"
    assert xlsx_data[0][1] == "name"

@cjen.operate.xlsx.reader(cols=[0,1])
def xlsx_with_fpath(fpath: str = None, xlsx_data: list = None):
    assert xlsx_data[0][0] == "id"
    assert xlsx_data[0][1] == "name"

def test_fpath():
    xlsx_with_fpath(fpath="test_data.xlsx")

