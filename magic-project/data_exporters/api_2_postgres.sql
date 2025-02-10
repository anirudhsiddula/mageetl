-- Docs: https://docs.mage.ai/guides/sql-blocks
-- select * from {{ df_1 }}

SELECT '{{ block_output(parse=lambda data, _vars: data[1]) }}' AS color