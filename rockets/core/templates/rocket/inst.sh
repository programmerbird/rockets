#!/bin/sh

{% if rocket_efiles %}
PRESERVE_EFILE () {
	if [ ! -d "$1{{rocket_efiles_suffix}}" ] 
	then
		mkdir -p "$1{{rocket_efiles_suffix}}" 
		test -f "$1" && mv "$1" "$1{{rocket_efiles_suffix}}/00-original"
	fi
}

PACK_EFILE () {
	ls "$1{{rocket_efiles_suffix}}/*" | sort | sed "s/^\(.*\)$/cat \1/g" | sh > "$1"
}
{% endif %}

{% if rocket_efiles %}
# preserve efiles 
{% for efile in rocket_efiles %}PRESERVE_EFILE "{{efile}}"
{% endfor %}
{% endif %}

{% if rocket_dirs %}
# directories
{% for dir in rocket_dirs %}mkdir -p "{{dir}}"
{% endfor %}
{% endif %}

{% if rocket_files %}
# files
{% for file in rocket_files %}mv "/tmp/rocket-{{rocket_bundle}}{{file}}" "{{file}}"
{% endfor %}
{% endif %}

{% if rocket_efiles %}
# combine efiles
{% for efile in rocket_efiles %}PACK_EFILE "{{efile}}"
{% endfor %}
{% endif %}

{% if rocket_links %}
# symbolic links
{% for source,target in rocket_links %}ln -s "{{source}}" "{{target}}"
{% endfor %}
{% endif %}

