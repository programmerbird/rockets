#!/bin/bash

RM=rm -f 
RMDIR=rmdir --ignore-fail-on-non-empty 

{% if rocket_efiles %}
PACK_EFILE () {
	ls "$1{{extendfile_suffix}}/*" | sort | sed "s/^\(.*\)$/cat \1/g" | sh > "$1"
}
{% endif %}

{% for file in rocket_files %}$RM "{{file}}"
{% endfor %}

{% for dir in rocket_dirs %}$RMDIR "{{dir}}"
{% endfor %}

{% if rocket_efiles %}
# combine efiles
{% for efile in rocket_efiles %}PACK_EFILE "{{efile}}"
{% endfor %}
{% endif %}

{% if rocket_links %}
# symbolic links
{% for source,target in rocket_links %}rm -f "{{target}}"
{% endfor %}
{% endif %}

