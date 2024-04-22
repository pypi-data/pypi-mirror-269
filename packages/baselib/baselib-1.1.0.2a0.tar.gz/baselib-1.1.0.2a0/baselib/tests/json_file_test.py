import os
from baselib.json import JsonFile


class TestJsonFile(object):

    def test_json_file(self):
        filename = "test.json"
        if os.path.isfile(filename):
            os.remove(filename)
        data = JsonFile.read(filename)
        assert data == {}
        JsonFile.write(filename, {"msg": "hello"})
        data = JsonFile.read(filename)
        assert data == {"msg": "hello"}
        JsonFile.update(filename, {"msg": "world"})
        data = JsonFile.read(filename)
        assert data == {"msg": "world"}
        JsonFile.update(filename, {"info": "hello"})
        data = JsonFile.read(filename)
        assert data == {"info": "hello", "msg": "world"}

        # 验证非合法json 读取
        os.remove(filename)
        with open(filename, "w") as fid:
            fid.write("test")
        data = JsonFile.read(filename)
        assert data == {}

        # 验证中文读写
        data = {"msg": "中文", "msg2": u"中文"}
        JsonFile.write(filename, data)
        data = JsonFile.read(filename)
        assert data['msg'] == "中文"
        assert data['msg2'] == "中文"

