#! /bin/env sh

files=(Chem Gap GapNo15)


awk 'BEGIN{printf "%s", "pre/post"}{printf "%s%s" ,",",$1}END{printf "\n"}' labels.csv > header.csv

for f in Chem Gap GapNo15
do
  echo -n processing $f: " "
  paste -d',' labels.csv "$f"_headless.csv > "$f"_.csv
  cat header.csv "$f"_.csv > "$f".csv
  sort "$f".csv > "$f"_sortR.csv
  echo sorted rows in "$f"_sortR.csv
done
