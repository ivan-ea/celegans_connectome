#! /bin/env sh

files=(Chem Gap GapNo15)
int="intermediate"

awk 'BEGIN{printf "%s", "pre/post"}{printf "%s%s" ,",",$1}END{printf "\n"}' labels.csv > header.csv

for f in Chem Gap GapNo15
do
  echo -n processing $f: " "
  paste -d',' labels.csv "$f"_headless.csv \
    > "$int/$f"_.csv
  sort "$int/$f"_.csv > "$int/$f"_sortR_.csv
  cat header.csv "$int/$f"_sortR_.csv > "$f"_sortR.csv
  echo matrices with sorted rows in "$f"_sortR.csv
done
