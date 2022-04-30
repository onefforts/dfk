#!/usr/bin/bash

# 実行時に指定された引数の数、つまり変数 $# の値が 3 でなければエラー終了。
if [ $# -ne 13 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo -e "実行するには13個の引数が必要です。\n引数1: foraging のチーム数\n引数2: fishing のチーム数\n引数3: alchemist_assistance のチーム数\n引数4: arm_wrestling のチーム数\n引数5: card_gameのチーム数\n引数6: dancing のチーム数\n引数7: dartsのチーム数\n引数8: game_of_ball のチーム数\n引数9: helping_the_farm のチーム数\n引数10: puzzle_solving のチーム数\n引数11: jewel mining のチーム数\n引数12: gold mining のHERO数\n引数13: gardening のHERO数\n " 1>&2
  exit 1
fi

# 既に走っているquestを停止
kill `ps -ef | grep questsV1.py | grep -v grep | awk '{ print $2 }'`
kill `ps -ef | grep questsV2.py | grep -v grep | awk '{ print $2 }'`

V2_QUESTS=(foraging fishing alchemist_assistance arm_wrestling card_game dancing darts game_of_ball helping_the_farm puzzle_solving)
V1_QUESTS=(jewel_mining gold_mining gardening)

N=1
for quest in "${V2_QUESTS[@]}"; do
  for i in `seq 0 $((${!N} - 1))`; do
    echo "python3 questsV2.py $quest $i &"
    python3 questsV2.py $quest $i &
  done
  N=$((++N))
done

for quest in "${V1_QUESTS[@]}"; do
  for i in `seq 0 $((${!N} - 1))`; do
    echo "python3 questsV1.py $quest $i &"
    python3 questsV1.py $quest $i &
  done
  N=$((++N))
done
