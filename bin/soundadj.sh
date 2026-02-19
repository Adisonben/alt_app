amixer scontrols > /dev/null
amixer sset 'PCM' "$1%" | grep 'dB' | sed -s s/\ /-/g | cut -d'-' -f7 | sed -s "s/\[//g" | sed -s "s/\]//g"
