BEGIN{
  nc=split(nw_c,c,"\n")
  #print "nc", nc
  printf "pre/post"
  for(i=1;i<=nc;i++) printf "%s%s", OFS, c[i]
  print
}
NR==1{
  for (i=1; i<=NF; i++) {
    old_cols[$i] = i
    new_cols[c[i]] = i+1
  }
  print "old_cols[ADAL]" ,old_cols["ADAL"]
  print "new_cols[ADAL]", new_cols["ADAL"]
  print "old_cols[IL2DL]" ,old_cols["IL2DL"]
  print "new_cols[IL2DL]", new_cols["IL2DL"]
}
NR > 1{
  printf $1
  for (i=1; i<=nc;i++)
    printf "%s%s", OFS, $(old_cols[c[i]])
  print
}
