#!/usr/bin/bash

# 実行時に指定された引数の数、つまり変数 $# の値が 3 でなければエラー終了。
if [ $# -ne 5 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo -e "実行するには5個の引数が必要です。\n引数1: foraging のチーム数\n引数2: fishing のチーム数\n引数3: jewel mining のチーム数\n引数4: gold mining のHERO数\n引数5: gardening のHERO数\n " 1>&2
  exit 1
fi

# 既に走っているquestを停止
kill `ps -ef | grep quests.py | grep -v grep | awk '{ print $2 }'`

for i in `seq 0 $(($1 - 1))`; do
  echo "python3 quests.py foraging $i &"
  python3 quests.py foraging $i &
done

for i in `seq 0 $(($2 - 1))`; do
  echo "python3 quests.py fishing $i &"
  python3 quests.py fishing $i &
done

for i in `seq 0 $(($3 - 1))`; do
  echo "python3 quests.py jewel_minning $i &"
  python3 quests.py jewel_minning $i &
done

for i in `seq 0 $(($4 - 1))`; do
  echo "python3 quests.py gold_minning $i &"
  python3 quests.py gold_minning $i &
done

for i in `seq 0 $(($5 - 1))`; do
  echo "python3 quests.py gardening $i &"
  python3 quests.py gardening $i &
done
