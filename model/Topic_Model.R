library(stm)
library(tm)
library(sigmoid)

poliblogs <- read.csv("/Users/FrankMAC/Desktop/Google-Alert-Link-Grabber/model/input/input_master.csv")

characterVector <- stopwords("smart")
customList <- c("circular")

finalStopWordList <- append(characterVector, customList)

#poliblogs <- na.omit(poliblogs)
#poliblogs <- poliblogs[which(poliblogs$time=='2018.09' | poliblogs$time=='2018.11' | poliblogs$time=='2019.01' | poliblogs$time=='2019.03' | poliblogs$time=='2019.05' | poliblogs$time=='2019.07'  | poliblogs$time=='2019.09'), ]
poliblogs <- poliblogs[which(poliblogs$time=='2018.09'),]

processed <- textProcessor(poliblogs$text, metadata = poliblogs, ucp = TRUE, customstopwords = finalStopWordList)

out <- prepDocuments(processed$documents, processed$vocab, processed$meta)

docs <- out$documents
vocab <- out$vocab
meta <-out$meta

First_STM <- stm(documents = out$documents, vocab = out$vocab,
                 K = 20, data = out$meta, init.type = "Spectral", verbose = FALSE)
summary(First_STM)

dat <- First_STM[["theta"]]
dat <- sigmoid(dat)

mod.out.corr <- topicCorr(First_STM, method = c("huge"), cutoff = 0.05,
                          verbose = TRUE)

plot(mod.out.corr)
summary(First_STM)
plot(First_STM)
#labelTopics(First_STM, topics = NULL, n = 5, frexweight = 0.5)

