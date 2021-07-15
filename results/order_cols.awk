BEGIN{
  nc=split(nw_c,c,"\n")
  printf "pre/post"
  for(i=1;i<=nc;i++) printf "%s%s", OFS, c[i]
  print
}
NR==1{ for (i=1; i<=NF; i++) old_cols[$i] = i }
NR > 1{
  printf $1
  for (i=1; i<=nc;i++)
    printf "%s%s", OFS, $(old_cols[c[i]])
  printf RS
}
