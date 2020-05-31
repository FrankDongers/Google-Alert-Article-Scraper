library(stm)
library(tm)
library(sigmoid)
library(stringr)


article_list <- list("/Users/FrankMAC/Desktop/Google-Alert-Link-Grabber/model/input/input_master.csv")
date_list <- list("2018.09","2018.12","2019.03","2019.06","2019.09")

characterVector <- stopwords("smart")
customList <- c("circular")
finalStopWordList <- append(characterVector, customList)

csv_date <- vector()
csv_region <- vector()
csv_content <- character()
csv_image <- vector()

for (s in article_list) {
  inputLocation <- str_split(s, "/")
  inputLength <- length(inputLocation[[1]])
  inputLocation <- inputLocation[[1]][inputLength]
  
  inputLocation <- str_split(inputLocation, "\\.")
  inputLocation <- inputLocation[[1]][1]
  
  #newsites <- na.omit(newsites)
  #newsites <- newsites[which(newsites$time=='2018.09' | newsites$time=='2018.11' | newsites$time=='2019.01' | newsites$time=='2019.03' | newsites$time=='2019.05' | newsites$time=='2019.07'  | newsites$time=='2019.09'), ]
  for (d in date_list) {
    print(s)
    newsites <- read.csv(s)
    newsites <- newsites[which(newsites$time==d),]
    
    processed <- textProcessor(newsites$text, metadata = newsites, ucp = TRUE, customstopwords = finalStopWordList)
    
    out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
    
    docs <- out$documents
    vocab <- out$vocab
    meta <-out$meta
    
    First_STM <- stm(documents = out$documents, vocab = out$vocab,
                     K = 20, data = out$meta, init.type = "Spectral", verbose = FALSE)
    #summary(First_STM)
    
    dat <- First_STM[["theta"]]
    dat <- sigmoid(dat)
    
    mod.out.corr <- topicCorr(First_STM, method = c("huge"), cutoff = 0.05,
                              verbose = TRUE)
    
    #plot(mod.out.corr)
    #plot(First_STM)
    
    textSummary <- summary(First_STM)
    tempSummary <- textSummary[["prob"]]
    n_topics <- nrow(tempSummary)
    n_words <- ncol(tempSummary)
    
    textSummaryOutput <- ""
    
    for (topic_val in 1:n_topics){
      textSummaryOutput <- paste(textSummaryOutput,"Topic")
      textSummaryOutput <- paste(textSummaryOutput,topic_val)
      textSummaryOutput <- paste(textSummaryOutput,":", sep="")
      for (word_val in 1:n_words){
        print(tempSummary[topic_val,word_val])
        textSummaryOutput <- paste(textSummaryOutput,tempSummary[topic_val,word_val])
        textSummaryOutput <- paste(textSummaryOutput,",", sep="")
      }
      textSummaryOutput <- paste(textSummaryOutput,"\n")
    }
    tempfilenamepng <- paste("/Users/FrankMAC/Desktop/Google-Alert-Link-Grabber/model/output/", inputLocation, "/", d, ".png", sep="")
    tempfilenametxt <- paste("/Users/FrankMAC/Desktop/Google-Alert-Link-Grabber/model/output/", inputLocation, "/", d, ".txt", sep="")
    
    capture.output(textSummaryOutput, file = tempfilenametxt)
    png(filename=tempfilenamepng, width = 750, height = 750, res = 135)
    plot(mod.out.corr)
    dev.off()
    
    tempimgLoc <- paste("https://github.com/FrankDongers/Google-Alert-Article-Scraper/blob/master/model/output/",inputLocation,"/", d, ".png?raw=true", sep="")
    
    
    tempSummaryData <- readChar(tempfilenametxt, file.info(tempfilenametxt)$size)
    print (tempSummaryData)
  
    csv_date <- c(csv_date, d)
    csv_region <- c(csv_region, inputLocation)
    csv_content <- c(csv_content, textSummaryOutput)
    csv_image <- c(csv_image, tempimgLoc)
    
    #labelTopics(First_STM, topics = NULL, n = 5, frexweight = 0.5)
    #rm(newsites,processed,out,docs,vocab,meta,First_STM)
  }
}

csv.data <- data.frame(csv_date, csv_region, csv_content,csv_image)
print(csv.data)
write.csv(csv.data,"/Users/FrankMAC/Desktop/Google-Alert-Link-Grabber/model/output/PowerBI_output.csv", row.names = FALSE)
