library(data.table)
library(stringr)
library(tm)
library(glmnet)
d <- read.csv("data/comments.csv", stringsAsFactors=F, encoding="UTF-8")


textCleanerRegex <- function(string,
                        gsub.regex="[[:punct:]]|[[:cntrl:]]|[[:digit:]]|„|“|—",
                        conv.tolower=TRUE){
  
  out <- str_trim(
    stripWhitespace(
      gsub(gsub.regex, " ", string)))
  if(conv.tolower) 
    return(tolower(out))
  else
    return(out)
}
cp <- Corpus(VectorSource(textCleanerRegex(d$CommentText),
                          encoding="UTF-8"))
dtm <- removeSparseTerms(DocumentTermMatrix(cp), 0.99)

cv.fit <- 
  cv.glmnet(x=sparseMatrix(i=dtm$i, j=dtm$j, x=dtm$v, dimnames=dtm$dimnames),
            y=d$Upvotes-d$DownVotes,
            family="gaussian")
plot(cv.fit)
sort(cv.fit$glmnet.fit$beta[,cv.fit$lambda==cv.fit$lambda.min])
cv.fit$glmnet.fit$beta

