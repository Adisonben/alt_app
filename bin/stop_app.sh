for pid in $(pidof '/usr/lib/chromium-browser/chromium-browser'); do
	kill -9 $pid &> /dev/null
done
