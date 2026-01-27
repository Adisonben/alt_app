for pid in $(pidof mpg123); do
kill -9 $pid &> /dev/null
	#echo $?
	#(( $? == 0)) && echo "kill of $pid successful" || echo "kill of $pid failed";
done
#kill -9 $(pgrep omxplayer) > /dev/null