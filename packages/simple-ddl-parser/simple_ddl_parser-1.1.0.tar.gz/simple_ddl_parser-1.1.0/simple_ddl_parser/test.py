from simple_ddl_parser import DDLParser
import pprint

ddl = """CREATE TABLE ${database_name}.MySchemaName."MyTableName" 
cluster by ("DocProv") (
ID NUMBER(38,0) NOT NULL, 
"DocProv" VARCHAR(2)
);"""

result = DDLParser(ddl).run(output_mode="snowflake")
pprint.pprint(result)


