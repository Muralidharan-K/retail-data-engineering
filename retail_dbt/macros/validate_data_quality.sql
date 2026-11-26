{% macro validate_data_quality(source_relation, key_column, check_columns=[]) %}
    {# method 1 to check source relation #}
    {% set relation=source(source_relation.split(".")[0], source_relation.split(".")[1]) %}
    {% set relation_exists=adapter.get_relation(
        database=relation.database,
        schema=relation.schema,
        identifier=relation.identifier
    )  %}
  {% if relation_exists is none %}
        {% do log("Given source relation " ~ source_relation ~ " is not exist",info=true) %}
        {% do exceptions.raise_compiler_error("Given source relation " ~ source_relation ~ " is not exist") %}
    {% else %}
        {% set column_list=adapter.get_columns_in_relation(relation)
                            | map(attribute='name') 
                            | map('lower') 
                            | list
         %}
        {% for col in check_columns %}
            {% if col | lower not in column_list %}
                {% do log("Given column list missing in source table",info=true) %}
                {% do exceptions.raise_compiler_error("Given column list missing in source table") %}
            {% endif %}
        {% endfor %}
        {% set check_data %}
            select
                (select count(*) from {{relation}} where {{key_column}} is not null) - (select count(distinct {{key_column}}) from {{relation}})as dup_count
                {% for col in check_columns %}
                    ,count_if({{col}} is null) as {{col}}_null_count
                {% endfor %}
                ,count(*) as row_count
            from {{relation}}
        {% endset %}
        {% if execute %} -- doubt?
            {% set results=run_query(check_data) %}
            {% set dup_count=results.columns[0].values()[0] %}
            {% set row_count=results.columns[-1].values()[0] %}
            {% if dup_count == 0 and row_count > 0 %}
                {% do log("Duplicate validation PASS: 0 duplicates; Source have "~ row_count~ " count", info=true) %}
            {% else %}
                {% do log("Duplicate validation/Source count FAIL: " ~ dup_count ~ "/" ~ row_count, info=true) %}
                {#{% do exceptions.raise_compiler_error("Duplicate validation/Source count FAIL: " ~ dup_count ~ "/" ~ row_count) %}#}
            {% endif %}                       
            {% for col in check_columns %}
                {% set null_count=results.columns[loop.index].values()[0] %}
                {% if null_count == 0 %}
                    {% do log("NULL validation PASS for " ~ col, info=true) %}
                {% else %}
                    {% do log("NULL validation FAIL for " ~ col ~ ": " ~ null_count ~ " NULL values", info=true) %}
                {% endif %}
            {% endfor %}
        {% endif %} 
    {% endif %}
{% endmacro %}