import datetime
import shutil
import time
import unittest
from io import BytesIO
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch

import httpx
from PIL import Image
from bson import ObjectId
from bson.tz_util import utc
from fastapi import UploadFile
from starlette.datastructures import Headers

from retk import const, core, config
from retk.controllers.schemas.user import PatchUserRequest
from retk.core.files.importing.async_tasks.utils import update_process
from retk.models import db_ops
from retk.models.client import client
from retk.models.tps import ImportData, AuthedUser, convert_user_dict_to_authed_user
from retk.utils import short_uuid
from . import utils


class LocalModelsTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        utils.set_env(".env.test.local")
        # create a fake image
        tmp_path = Path(__file__).parent / "tmp" / "fake.png"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (100, 100)).save(tmp_path)

    @classmethod
    def tearDownClass(cls) -> None:
        utils.drop_env(".env.test.local")
        shutil.rmtree(Path(__file__).parent / "tmp", ignore_errors=True)

    async def asyncSetUp(self) -> None:
        await client.init()
        u, _ = await core.user.get_by_email(email=const.DEFAULT_USER["email"])
        self.au = AuthedUser(
            u=convert_user_dict_to_authed_user(u),
            request_id="xxx",
            language=u["settings"]["language"],
        )

    async def asyncTearDown(self) -> None:
        await client.drop()
        shutil.rmtree(Path(__file__).parent / "tmp" / ".data" / "files", ignore_errors=True)
        shutil.rmtree(Path(__file__).parent / "tmp" / ".data" / "md", ignore_errors=True)

    async def test_user(self):
        u, code = await core.user.get_by_email(email=const.DEFAULT_USER["email"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("rethink", u["nickname"])
        self.assertIsNotNone(u)

        u, code = await core.user.add(
            account="aaa", source=const.UserSource.EMAIL.value,
            email="aaa", hashed="bbb", nickname="ccc", avatar="ddd", language=const.Language.EN.value)
        self.assertNotEqual("", u["id"])
        self.assertEqual(const.Code.OK, code)
        _uid = u["id"]

        u, code = await core.user.get(_uid)
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("ccc", u["nickname"])

        u, code = await core.user.patch(
            au=AuthedUser(
                u=convert_user_dict_to_authed_user(u),
                request_id="xxx",
                language=const.Language.EN.value,
            ),
            req=PatchUserRequest(
                nickname="2",
                avatar="3",
                lastState=PatchUserRequest.LastState(
                    nodeDisplayMethod=const.NodeDisplayMethod.LIST.value,
                )
            )
        )
        self.assertEqual(const.Code.OK, code)

        u, code = await core.user.get(_uid)
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("bbb", u["hashed"])
        self.assertEqual("2", u["nickname"])
        self.assertEqual("3", u["avatar"])
        self.assertEqual(const.NodeDisplayMethod.LIST.value, u["lastState"]["nodeDisplayMethod"])

        code = await core.account.manager.disable(uid=_uid)
        self.assertEqual(const.Code.OK, code)

        u, code = await core.user.get(uid=_uid)
        self.assertEqual(const.Code.USER_DISABLED, code)
        self.assertIsNone(u)

        code = await core.account.manager.enable(uid=_uid)
        self.assertEqual(const.Code.OK, code)

        code = await core.account.manager.disable(uid="sdwqdqw")
        self.assertEqual(const.Code.OK, code)

        await core.account.manager.delete(uid=_uid)

    async def test_node(self):
        node, code = await core.node.post(
            au=self.au, md="a" * (const.MD_MAX_LENGTH + 1), type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.NOTE_EXCEED_MAX_LENGTH, code)
        self.assertIsNone(node)

        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(const.Code.OK, code)
        used_space = u["usedSpace"]
        node, code = await core.node.post(
            au=self.au, md="[title](/qqq)\nbody", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(used_space + len(node["md"].encode("utf-8")), u["usedSpace"])
        self.assertEqual("modifiedAt", u["lastState"]["nodeDisplaySortKey"])

        n, code = await core.node.get(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("title", n["title"])
        self.assertEqual("body", n["snippet"])

        ns, total = await client.search.search(au=self.au)
        self.assertEqual(3, len(ns))
        self.assertEqual(3, total)

        ns, total = await client.search.search(au=self.au, limit=5, page=12, sort_key="createdAt")
        self.assertEqual(0, len(ns))
        self.assertEqual(3, total)

        u, code = await core.user.patch(
            au=self.au,
            req=PatchUserRequest(
                lastState=PatchUserRequest.LastState(
                    nodeDisplaySortKey="createdAt",
                )
            )
        )

        self.assertEqual(const.Code.OK, code)
        self.assertEqual("createdAt", u["lastState"]["nodeDisplaySortKey"])
        used_space = u["usedSpace"]
        n, _, code = await core.node.update_md(au=self.au, nid=node["id"], md="title2\nbody2")
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("title2", n["title"])
        self.assertEqual("title2\nbody2", n["md"])
        self.assertEqual(const.NodeType.MARKDOWN.value, n["type"])

        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(used_space + (
                len(n["md"].encode("utf-8")) -
                len(node["md"].encode("utf-8"))
        ), u["usedSpace"])

        code = await core.node.disable(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)
        n, code = await core.node.get(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.NODE_NOT_EXIST, code)

        code = await core.node.to_trash(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)

        code = await core.node.delete(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)
        n, code = await core.node.get(au=self.au, nid=node["id"])
        self.assertIsNone(n)
        self.assertEqual(const.Code.NODE_NOT_EXIST, code)

        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(used_space - len(node["md"].encode("utf-8")), u["usedSpace"])

        nodes, total = await core.node.core_nodes(au=self.au, page=0, limit=10)
        self.assertEqual(2, len(nodes))
        self.assertEqual(2, total)

    async def test_parse_at(self):
        nid1, _ = await core.node.post(
            au=self.au, md="c", type_=const.NodeType.MARKDOWN.value,
        )
        nid2, _ = await core.node.post(
            au=self.au, md="我133", type_=const.NodeType.MARKDOWN.value,
        )
        md = dedent(f"""title
        fffqw [@c](/n/{nid1['id']})
        fff
        [@我133](/n/{nid2['id']})
        ffq
        """)
        node, code = await core.node.post(
            au=self.au, md=md, type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        nodes, total = await client.search.search(
            au=self.au,
            query="",
            sort_key="createdAt",
            reverse=True,
            page=0,
            limit=10,
            exclude_nids=[],
        )
        self.assertEqual(5, len(nodes))
        self.assertEqual(5, total)
        found, total = await client.search.search(au=self.au, query="我")
        self.assertEqual(2, len(found), msg=found)
        self.assertEqual(2, total)

        n, code = await core.node.get(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(2, len(n["toNodeIds"]))

        cache = n["md"]
        n, _, code = await core.node.update_md(au=self.au, nid=node["id"], md=f'{cache}xxxx')
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(cache + "xxxx", n["md"])

        n, code = await core.node.get(au=self.au, nid=nid1['id'])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(1, len(n["fromNodeIds"]))

        n, _, code = await core.node.update_md(au=self.au, nid=node["id"], md=n["title"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(0, len(n["toNodeIds"]))

        n, code = await core.node.get(au=self.au, nid=nid1['id'])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(0, len(n["fromNodeIds"]))

    async def test_add_set(self):
        node, code = await core.node.post(
            au=self.au, md="title\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(0, len(node["toNodeIds"]))
        self.assertEqual(const.Code.OK, code)

        res = await db_ops.node_add_to_set(node["id"], "toNodeIds", short_uuid())
        self.assertEqual(1, res.modified_count)
        node, code = await core.node.get(au=self.au, nid=node["id"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(1, len(node["toNodeIds"]))

    async def test_cursor_text(self):
        n1, code = await core.node.post(
            au=self.au, md="title\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        n2, code = await core.node.post(
            au=self.au, md="title2\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)

        recom, total = await core.node.search.at(
            au=self.au,
            nid=n2["id"],
            query="text",
            page=0,
            limit=10,
        )
        self.assertEqual(1, len(recom))
        self.assertEqual(1, total)

        recom, total = await core.node.search.at(
            au=self.au,
            nid=n2["id"],  # exclude the second node
            query="",  # return recent nodes only
            page=0,
            limit=10,
        )
        self.assertEqual(2, len(recom))
        self.assertEqual(2, total)

        code = await core.recent.added_at_node(au=self.au, nid=n1["id"], to_nid=n2["id"])
        self.assertEqual(const.Code.OK, code)

        recom, total = await core.node.search.at(
            au=self.au,
            nid=n1["id"],  # exclude the second node
            query="",
            page=0,
            limit=10,
        )
        self.assertEqual(3, len(recom))
        self.assertEqual(3, total)
        self.assertEqual("Welcome to Rethink", recom[2].title)

    async def test_to_trash(self):
        n1, code = await core.node.post(
            au=self.au, md="title\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        n2, code = await core.node.post(
            au=self.au, md="title2\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)

        code = await core.node.to_trash(au=self.au, nid=n1["id"])
        self.assertEqual(const.Code.OK, code)

        ns, total = await core.node.get_nodes_in_trash(au=self.au, page=0, limit=10)
        self.assertEqual(1, len(ns))
        self.assertEqual(1, total)
        self.assertEqual(n1["id"], ns[0]["id"])

        ns, total = await client.search.search(au=self.au, query="")
        self.assertEqual(3, len(ns))
        self.assertEqual(3, total)

        code = await core.node.restore_from_trash(au=self.au, nid=n1["id"])
        self.assertEqual(const.Code.OK, code)
        nodes, total = await client.search.search(au=self.au, query="")
        self.assertEqual(4, len(nodes))
        self.assertEqual(4, total)

    async def test_search(self):
        code = await core.recent.put_recent_search(au=self.au, query="a")
        self.assertEqual(const.Code.OK, code)
        await core.recent.put_recent_search(au=self.au, query="c")
        await core.recent.put_recent_search(au=self.au, query="b")

        doc = await client.coll.users.find_one({"id": self.au.u.id})
        self.assertIsNotNone(doc)
        self.assertEqual(["b", "c", "a"], doc["lastState"]["recentSearch"])

    async def test_batch(self):
        ns = []
        for i in range(10):
            n, code = await core.node.post(
                au=self.au, md=f"title{i}\ntext", type_=const.NodeType.MARKDOWN.value
            )
            self.assertEqual(const.Code.OK, code)
            ns.append(n)

        base_count = 2

        code = await core.node.batch_to_trash(au=self.au, nids=[n["id"] for n in ns[:4]])
        self.assertEqual(const.Code.OK, code)
        nodes, total = await client.search.search(au=self.au, query="")
        self.assertEqual(6 + base_count, len(nodes))
        self.assertEqual(6 + base_count, total)

        tns, total = await core.node.get_nodes_in_trash(au=self.au, page=0, limit=10)
        self.assertEqual(4, total)
        self.assertEqual(4, len(tns))

        code = await core.node.restore_batch_from_trash(au=self.au, nids=[n["id"] for n in tns[:2]])
        self.assertEqual(const.Code.OK, code)
        nodes, total = await client.search.search(au=self.au)
        self.assertEqual(8 + base_count, len(nodes))
        self.assertEqual(8 + base_count, total)

        code = await core.node.batch_delete(au=self.au, nids=[n["id"] for n in tns[2:4]])
        self.assertEqual(const.Code.OK, code)
        tns, total = await core.node.get_nodes_in_trash(au=self.au, page=0, limit=10)
        self.assertEqual(0, total)
        self.assertEqual(0, len(tns))

    async def test_files_upload_process(self):
        now = datetime.datetime.now(tz=utc)
        doc: ImportData = {
            "_id": ObjectId(),
            "uid": "xxx",
            "process": 0,
            "type": "text",
            "startAt": now,
            "running": True,
            "obsidian": {},
            "msg": "",
            "code": const.Code.OK.value,
        }
        res = await client.coll.import_data.insert_one(doc)
        self.assertTrue(res.acknowledged)

        doc, code = await update_process("xxx", "obsidian", 10)
        self.assertEqual(const.Code.OK, code)

        doc = await core.files.get_upload_process("xxx1213")
        self.assertIsNone(doc)

        doc = await core.files.get_upload_process("xxx")
        self.assertEqual(10, doc["process"])
        self.assertEqual("obsidian", doc["type"])
        self.assertEqual(now, doc["startAt"])
        self.assertTrue(doc["running"])

        await client.coll.import_data.delete_one({"uid": "xxx"})

    async def test_update_title_and_from_nodes_updates(self):
        n1, code = await core.node.post(
            au=self.au, md="title1\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        n2, code = await core.node.post(
            au=self.au, md=f"title2\n[@title1](/n/{n1['id']})", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)

        n1, _, code = await core.node.update_md(au=self.au, nid=n1["id"], md="title1Changed\ntext")
        self.assertEqual(const.Code.OK, code)
        n2, code = await core.node.get(au=self.au, nid=n2["id"])
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(f"title2\n[@title1Changed](/n/{n1['id']})", n2["md"])

    async def test_upload_image_vditor(self):
        u, code = await core.user.get(self.au.u.id)
        used_space = u["usedSpace"]
        p = Path(__file__).parent / "tmp" / "fake.png"

        image = Image.open(p)
        buf = BytesIO()
        image.save(buf, format="png")
        size = buf.tell()
        img_file = UploadFile(
            buf, filename="fake.png", size=size,
            headers=Headers({"content-type": "image/png"})
        )
        res = await core.files.vditor_upload(au=self.au, files=[img_file])
        self.assertIn("fake.png", res["succMap"])
        self.assertTrue(".png" in res["succMap"]["fake.png"])
        local_file = Path(__file__).parent / "tmp" / ".data" / res["succMap"]["fake.png"][1:]
        self.assertTrue(local_file.exists())
        local_file.unlink()
        image.close()
        buf.close()
        await img_file.close()

        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(used_space + size, u["usedSpace"])

    @patch(
        "retk.core.files.upload.httpx.AsyncClient.get",
    )
    async def test_fetch_image_vditor(self, mock_get):
        f = open(Path(__file__).parent / "tmp" / "fake.png", "rb")
        mock_get.return_value = httpx.Response(
            200,
            content=f.read(),
            headers={"content-type": "image/png"}
        )

        u, code = await core.user.get(self.au.u.id)
        used_space = u["usedSpace"]

        url = "https://rethink.run/favicon.png"
        new_url, code = await core.files.fetch_image_vditor(au=self.au, url=url)
        self.assertEqual(const.Code.OK, code)
        self.assertTrue(new_url.endswith(".png"))
        self.assertTrue(new_url.startswith("/"))
        local_file = Path(__file__).parent / "tmp" / ".data" / new_url[1:]
        self.assertTrue(local_file.exists())
        local_file.unlink()

        u, code = await core.user.get(self.au.u.id)
        self.assertEqual(used_space + f.tell(), u["usedSpace"])
        f.close()

    async def test_update_used_space(self):
        u, code = await core.user.get(self.au.u.id)
        base_used_space = u["usedSpace"]
        for delta, value in [
            (100, 100),
            (100, 200),
            (0, 200),
            (-3000, 0),
            (20.1, 20.1),
        ]:
            code = await core.user.update_used_space(uid=self.au.u.id, delta=delta)
            self.assertEqual(const.Code.OK, code)
            u, code = await core.user.get(self.au.u.id)
            self.assertEqual(const.Code.OK, code)
            now = u["usedSpace"] - base_used_space
            if now < 0:
                now = 0
                base_used_space = 0
            self.assertAlmostEqual(value, now, msg=f"delta: {delta}, value: {value}")

    async def test_node_version(self):
        node, code = await core.node.post(
            au=self.au, md="[title](/qqq)\nbody", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        md_path = Path(__file__).parent / "tmp" / ".data" / "md" / (node["id"] + ".md")
        self.assertTrue(md_path.exists())

        time.sleep(1)

        n, _, code = await core.node.update_md(au=self.au, nid=node["id"], md="title2\nbody2")
        self.assertEqual(const.Code.OK, code)
        hist_dir = Path(__file__).parent / "tmp" / ".data" / "md" / "hist" / node["id"]
        self.assertEqual(1, len(list(hist_dir.glob("*.md"))))

        time.sleep(1)

        n, _, code = await core.node.update_md(au=self.au, nid=node["id"], md="title2\nbody3")
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(2, len(list(hist_dir.glob("*.md"))))

    async def test_md_history(self):
        bi = config.get_settings().MD_BACKUP_INTERVAL
        config.get_settings().MD_BACKUP_INTERVAL = 0.0001
        n1, code = await core.node.post(
            au=self.au, md="title\ntext", type_=const.NodeType.MARKDOWN.value
        )
        self.assertEqual(const.Code.OK, code)
        time.sleep(0.001)

        n2, old_n, code = await core.node.update_md(
            au=self.au, nid=n1["id"], md="title2\ntext",
        )
        self.assertEqual(const.Code.OK, code)
        time.sleep(0.001)

        n2, old_n, code = await core.node.update_md(
            au=self.au, nid=n1["id"], md="title3\ntext",
        )
        self.assertEqual(const.Code.OK, code)

        hist, code = await core.node.get_hist_editions(
            au=self.au,
            nid=n1["id"],
        )
        self.assertEqual(const.Code.OK, code)
        self.assertEqual(2, len(hist))

        hist_md, code = await core.node.get_hist_edition_md(
            au=self.au,
            nid=n1["id"],
            version=hist[1],
        )
        self.assertEqual(const.Code.OK, code)
        self.assertEqual("title2\ntext", hist_md)

        config.get_settings().MD_BACKUP_INTERVAL = bi
