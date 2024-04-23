import glob
import os
import pprint
import logging
import textwrap
import re
from gd_excelexporter.core.generator import Generator, Table
from gd_excelexporter.config import Configuration

logger = logging.getLogger(__name__)


class ResourceGenerator(Generator):
    # 导出格式
    __extension__ = "tres"
    __datatable_class__ = """
    class_name EEDataTable
    extends Resource

    @export
    var data = {}
    """

    @classmethod
    def generate(cls, table: Table, config: Configuration):
        # 表格数据脚本模板
        abs_output = os.path.abspath(config.output)
        relpath = os.path.relpath(abs_output, config.project_root).replace("\\", "/")
        template = """
        [gd_resource type="Resource" script_class="EEDataTable" load_steps=2 format=3] 

        [ext_resource type="Script" path="res://{relpath}/ee_data_table.gd" id="1"]

        [resource]
        script = ExtResource("1")
        data = {data}
        """  # noqa
        template = textwrap.dedent(template)
        new_table = {}

        for id, row in table.items():
            row_data = {}

            for field, var in row.items():
                field_name: str = field
                row_data[field_name] = var.value

            new_table[id] = row_data

        code = template.format(
            data=pprint.pformat(
                new_table, indent=4, width=1000000000, compact=True, sort_dicts=True
            ),
            relpath=relpath,
        )

        code = textwrap.dedent(code)
        code = re.sub(r"\b(True|False)\b", lambda m: m.group(1).lower(), code)
        code = code.replace("'", '"')
        return code

    @classmethod
    def completed_hook(cls, config: Configuration):
        output = config.output
        settings_file_path = os.path.join(output, "settings.gd")
        data_class_file_path = os.path.join(output, "ee_data_table.gd")
        project_root = config.project_root

        lines = []

        for path in glob.glob(f"{output}/**/*.{cls.__extension__}", recursive=True):
            if path == settings_file_path:
                continue  # 跳过 settings.gd
            if path == data_class_file_path:
                continue  # 跳过数据表类
            basename = os.path.basename(path)
            setting_name = os.path.splitext(basename)[0]
            relpath = os.path.relpath(path, project_root).replace("\\", "/")
            lines.append(f"var {setting_name} = load('res://{relpath}')")

            # 去掉缩进
        code = textwrap.dedent(
            """
        extends Node
        # 这个脚本你需要挂到游戏的Autoload才能全局读表

        {refs_code}
        """
        )
        refs_code = "\n".join(lines)

        code = code.format(refs_code=refs_code)

        with open(settings_file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
            logger.info("创建setting.gd")

        with open(data_class_file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(textwrap.dedent(cls.__datatable_class__))
            logger.info("创建DataTable类")
