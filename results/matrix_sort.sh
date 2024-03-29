#! /bin/env sh
# Takes the headless matrices and the labels file
# generate header and labeled matrices
# intermediate results in subfolder rather than pipe (might be useful?)
# Obtains matrices sorted by row and column

int="intermediate"
new_cols=$(sort labels.csv)

awk 'BEGIN{printf "%s", "pre/post"}{printf "%s%s" ,",",$1}END{printf "\n"}' labels.csv > header.csv

for f in Chem Gap GapNo15
do
  git rm "$f"_sortR.csv
  echo -n processing $f: " "
  paste -d',' labels.csv "$f"_headless.csv > "$int/$f"_.csv
  sort "$int/$f"_.csv > "$int/$f"_sortR_.csv
  cat header.csv "$int/$f"_sortR_.csv > "$int/$f"_sortR.csv
  awk -F',' -v OFS=',' -v nw_c="$new_cols" -f order_cols.awk "$int/$f"_sortR.csv > "$f"_sortRC.csv

  echo matrices with sorted rows and columns in "$f"_sortRC.csv
done
