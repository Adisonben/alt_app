for pid in $(pidof playbeep); do
 kill -9 $pid &> /dev/null
 #echo $?
 #(( $? == 0)) && echo "kill of $pid successful" || echo "kill of $pid failed";
done
