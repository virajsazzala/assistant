import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")


class NotionAgenda:
    def __init__(self):
        self.page_id = NOTION_PAGE_ID
        self.notion = Client(auth=NOTION_TOKEN)

    def _get_children(self, block_id):
        response = self.notion.blocks.children.list(block_id)

        return response.get("results", [])

    def _get_text(self, block, block_type):
        rich_text = block[block_type].get("rich_text", [])

        return "".join(text.get("plain_text", "") for text in rich_text).strip()

    def _extract_todos(self, column_blocks):
        todos = []

        for child in column_blocks[1:]:
            if child["type"] != "to_do":
                continue

            task_text = self._get_text(child, "to_do")

            if not task_text:
                continue

            todos.append(
                {"task": task_text, "completed": child["to_do"].get("checked", False)}
            )

        return todos

    def get_day_todos(self, day):
        target_day = day.lower().strip()

        page_blocks = self._get_children(self.page_id)

        for block in page_blocks:
            if block["type"] != "column_list":
                continue

            columns = self._get_children(block["id"])

            for column in columns:
                if column["type"] != "column":
                    continue

                column_blocks = self._get_children(column["id"])

                if not column_blocks:
                    continue

                heading = column_blocks[0]

                if not heading["type"].startswith("heading"):
                    continue

                heading_text = self._get_text(heading, heading["type"]).lower()

                if heading_text != target_day:
                    continue

                return self._extract_todos(column_blocks)

        return []

    def get_week_todos(self):
        week_data = {}

        page_blocks = self._get_children(self.page_id)

        for block in page_blocks:
            if block["type"] != "column_list":
                continue

            columns = self._get_children(block["id"])

            for column in columns:
                if column["type"] != "column":
                    continue

                column_blocks = self._get_children(column["id"])

                if not column_blocks:
                    continue

                heading = column_blocks[0]

                if not heading["type"].startswith("heading"):
                    continue

                day_name = self._get_text(heading, heading["type"])

                if not day_name:
                    continue

                week_data[day_name] = self._extract_todos(column_blocks)

        return week_data
