library(RCurl)
url <- paste0("http://www.sig.lt/linas/lt_form/?uzklausa=",
              "kurmio","&submit=Ie%F0koti")
system.time(o <- getURL(url))
