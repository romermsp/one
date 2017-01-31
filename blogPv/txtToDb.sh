
getId(){
case $1 in
"54388914")
echo 1
;;
"54388736")
echo 2
;;
"52771205")
echo 3
;;
"51787977")
echo 4
;;
"51365426")
echo 5
;;
"51314116")
echo 6
;;
"51284561")
echo 7
;;
esac
}

doline(){
	i=2
	cmd='mysql -uroot -ppassword -e "use stat;'
	dt=`echo $1|cut -d ';' -f1`
	#while ((1==1));
	while true;
	do
		f=`echo $1|cut -d ';' -f$i`
		if [ "$f" != "" ]
		then
			aid=`echo $f|cut -d ',' -f1`
			id=`getId $aid`
			pv=`echo $f|cut -d ',' -f2`
			sql="insert into blog_pv (dt,id,pv) values ('20$dt',$id,$pv)" 
			((i++))
			#sql='select \* from blog_pv limit 5'
			mysql -uroot -ppassword -e "use stat;${sql}"
		else 
			break
		fi
	done
}

for l in `tail pvbak1.txt`;do
	doline $l
done
