#!/usr/bin/awk

NF==3 {
  if ($2 ~ /^[a-zA-Z\d]+$/) {
    print $2"\t"$1
  } else if ($1 ~ /^[a-zA-Z\d]+$/) {
    print $1"\t"$2
  } else {
    print $1"\t"$2
    print $2"\t"$1
  }
}
