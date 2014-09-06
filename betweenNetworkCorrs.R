betweenNetworkCorr <- function(diag1, diag2){  # R function to correlate network timeseries between two groups
 mainDir = getwd() # define the root directory
 
 # start a log file and write headers
 log <- paste(diag1, diag2, ".gica/betweenNetworkLog.txt", sep="")
 write(paste("# Log of between network correlations for", diag1, diag2), log)
 write(paste("Network1", "Network2", diag1, diag2, "tValue", 
"pValue"), log)
 
 # define the directory containing hte ICA results. This folder should contain the goodness of fit results from GOF.py
 ICADir = paste(diag1, diag2, ".gica", sep="")
 tsEnd = "ts.txt"
 
 # get data frame containing ICA component network indices, eg DMN is component 1, Basal ganglia component 13 etc...
 GOFdF <- read.table(paste(ICADir, "bestGOFs.txt", sep="/"))
 names(GOFdF) <- c("directory", "network", "nvol", "gof")
 GOFdF$network <- as.vector(GOFdF$network)
 
 # create pairwise correlation matrix
 combns = combn(GOFdF$network, 2)
 
 # open timeseries files for all subjects
 for (num in seq(1,length(combns[1,]))){
  combNetworks <-combns[,num] # extract the combination of networks, eg Control, PD
  print (combNetworks)
  
  dF <- data.frame(matrix(nrow=0, ncol=2)) # create an empty dataframe to populate with correlation values
  names(dF) <- c("r", "Diagnosis")
  
  # iterate through diagnoses
  for (diag in c(diag1, diag2)){
   # get a list of the subject directories (assuming each subject has a directory and each directory has a subject)
   subjs = list.dirs(diag, recursive=FALSE)
   
   # iterate through subjects
   for (subj in subjs){
    t1 <- scan(paste(subj, paste(combNetworks[1], tsEnd, sep=""), sep="/")) # timeseries for network 1
    t2 <- scan(paste(subj, paste(combNetworks[2], tsEnd, sep=""), sep="/")) # timeseries for network 2
    
    r = cor(t1, t2) # Pearson correlation coefficient between the two timeseries

    subjdF <- data.frame(r=r, Diagnosis=diag) # write correlation value to temporary dataframe
    dF = rbind(dF, subjdF) # merge results with the main results dataframe
   }
  }
	
  # do t-test between groups
  tsTtest <- t.test(dF[dF$Diagnosis==diag1,1], dF[dF$Diagnosis==diag2,1])
  print(tsTtest) # display t-test results
  
  # write the results to the log file --> this needs updating to make use of the xtable package if possible
  write(paste(combNetworks[1], 
              combNetworks[2], mean(dF[dF$Diagnosis==diag1,1]), 
              mean(dF[dF$Diagnosis==diag2,1]), tsTtest$statistic, 
              tsTtest$p.value, sep = "\t&\t"),
        log, append=TRUE)
  
 } 
}


