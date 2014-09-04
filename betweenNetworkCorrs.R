betweenNetworkCorr <- function(diag1, diag2){
 mainDir = getwd()
 log <- paste(diag1, diag2, ".gica/betweenNetworkLog.txt", sep="")
 write(paste("# Log of between network correlations for", diag1, diag2), log)
 write(paste("Network1", "Network2", diag1, diag2, "tValue", 
"pValue"), log)
 
 ICADir = paste(diag1, diag2, ".gica", sep="")
 tsEnd = "ts.txt"
 
 # get data frame containing network numbers
 GOFdF <- read.table(paste(ICADir, "bestGOFs.txt", sep="/"))
 names(GOFdF) <- c("directory", "network", "nvol", "gof")
 GOFdF$network <- as.vector(GOFdF$network)
 
 # create pairwise correlation matrix
 combns = combn(GOFdF$network, 2)
 
 # open timeseries files
 for (num in seq(1,length(combns[1,]))){
  combNetworks <-combns[,num]
  print (combNetworks)
  
  dF <- data.frame(matrix(nrow=0, ncol=2))
  names(dF) <- c("r", "Diagnosis")
  
  for (diag in c(diag1, diag2)){
   subjs = list.dirs(diag, recursive=FALSE)
   for (subj in subjs){
    t1 <- scan(paste(subj, paste(combNetworks[1], tsEnd, 
sep=""), sep="/"))
    t2 <- scan(paste(subj, paste(combNetworks[2], tsEnd, 
sep=""), sep="/"))
    
    r = cor(t1, t2)

    subjdF <- data.frame(r=r, Diagnosis=diag)
    dF = rbind(dF, subjdF)
   }
  }
	
  # do t-test
  tsTtest <- t.test(dF[dF$Diagnosis==diag1,1], dF[dF$Diagnosis==diag2,1])
  print(tsTtest)
  write(paste(combNetworks[1], 
combNetworks[2], mean(dF[dF$Diagnosis==diag1,1]), 
 mean(dF[dF$Diagnosis==diag2,1]), tsTtest$statistic, 
tsTtest$p.value, sep = "\t&\t"), log, append=TRUE)
  
 } 
}


