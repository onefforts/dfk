#!/usr/bin/bash

# 実行時に指定された引数の数、つまり変数 $# の値が 3 でなければエラー終了。
if [ $# -ne 4 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo -e "実行するには4個の引数が必要です。\n引数1: foraging のチーム数\n引数2: fishing のチーム数\n引数3: mining のチーム数\n引数4: gardening のHERO数\n " 1>&2
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
  echo "python3 quests.py minning $i &"
  python3 quests.py minning $i &
done

for i in `seq 0 $(($4 - 1))`; do
  echo "python3 quests.py gardening $i &"
  python3 quests.py gardening $i &
done
