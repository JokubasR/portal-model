library(data.table)
library(stringr)
library(tm)
library(glmnet)
d <- read.csv("data/comments.csv", stringsAsFactors=F, encoding="UTF-8")
#intToUtf8 some problems with different utf quotes
some.wild.characters <- 
  paste(c(enc2utf8("[[:punct:]]|[[:cntrl:]]|[[:digit:]]"),
        strsplit(intToUtf8(8210:8230),"")[[1]]),collapse="|")
textCleanerRegex <- function(string,
                             gsub.regex=some.wild.characters,
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
write.csv(sort(unique(unlist(lapply(cp, strsplit, " ")))),
          file="dictionary.csv",
          row.names=F, fileEncoding="UTF-8")
dtm <- DocumentTermMatrix(cp)
#russian letters appear in dictionary, but it is not huge problem
colnames(dtm)[1:100]
dtm <- removeSparseTerms(DocumentTermMatrix(cp), 0.99)
grep(intToUtf8(8221), colnames(dtm)[1:100])
cv.fit <- 
  cv.glmnet(x=sparseMatrix(i=dtm$i, j=dtm$j, x=dtm$v, dimnames=dtm$dimnames),
            y=d$Upvotes-d$DownVotes,
            family="gaussian")
plot(cv.fit)
sort(cv.fit$glmnet.fit$beta[,cv.fit$lambda==cv.fit$lambda.min])
cv.fit$glmnet.fit$beta

